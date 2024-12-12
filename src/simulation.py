import pandas as pd
import random
from concurrent.futures import ThreadPoolExecutor

START_YEAR = 2023
COAL_EXIT = 2038

generation = {
    'Biomasse': 37826000,
    'Wasserkraft': 15000000,
    'Wind Offshore': 94620000,
    'Wind Onshore': 228060000,
    'Photovoltaik': 157380000,
    'Sonstige Erneuerbare': 1100000,
    'Braunkohle': 78000000,
    'Steinkohle': 40000000,
    'Erdgas': 50143000,
    'Pumpspeicher': 10647000,
    'Sonstige Konventionelle': 12000000,
    'Verbrauch': 685000000
}

# Installierte Leistungen in MW
photovoltaik = {
    'Installierte Leistung [MW]' : {
        'worst' : 180000,
        'mean' : 215000,
        'best' : 240000
    },
    'Globalstrahlung [W/m^2]' : {
        'worst' : 1036,
        'mean' : 1151.5,
        'best' : 1266.6
    }
}

windOffshore = {
    'Installierte Leistung [MW]' : {
        'worst' : 8500,
        'mean' : 22000,
        'best' : 30000
    },
    'Volllaststunden [h]' : {
        'worst' : 4500,
        'mean' : 5000,
        'best' : 6000
    }
}

windOnshore = {
    'Installierte Leistung [MW]' : {
        'worst' : 60000,
        'mean' : 75000,
        'best' : 100000
    },
    'Volllaststunden [h]' : {
        'worst' : 2700,
        'mean' : 3000,
        'best' : 3300
    }
}

consumption = {
    'worst' : 775000000,
    'mean' : 685000000,
    'best' : 587000000
}


def scenarioOverall(dfList: list[pd.DataFrame]) -> list[pd.DataFrame]:
    while True:
        userInput = input("What scenario do you want, you may choose between 'best', 'mean' and 'worst': ")
        print()
        if userInput not in ['best', 'mean', 'worst']:
            print("\033[31mWrong input! Please enter 'best', 'mean', or 'worst'.\033[0m")
        else:
            break

    choices = {
        'Photovoltaik': photovoltaik,
        'Wind Offshore': windOffshore,
        'Wind Onshore': windOnshore,
        'Verbrauch': consumption
    }
    global generation
    generation.update({'Photovoltaik': 1, 'Wind Offshore': 1, 'Wind Onshore': 1, 'Verbrauch': 1})

    for category, subdict in choices.items():
        if category != 'Verbrauch':
            for key, scenarios in subdict.items():
                if userInput in scenarios:
                    generation[category] *= scenarios[userInput]
        elif category == 'Verbrauch':
            if userInput in subdict:
                generation[category] *= subdict[userInput]
        else:
            print("\033[31mError in szenario.\033[0m")

    generation['Photovoltaik']*=0.8 # loss factor := 0.8
        
    return simulation(dfList, 2030)
                
        

def scenarioEach(dfList: list[pd.DataFrame]) -> list[pd.DataFrame]:
    choices = {
        'Photovoltaik': photovoltaik,
        'Wind Offshore': windOffshore,
        'Wind Onshore': windOnshore,
        'Verbrauch': consumption
    }
    global generation
    generation.update({'Photovoltaik': 1, 'Wind Offshore': 1, 'Wind Onshore': 1, 'Verbrauch': 1})
    
    for category, subdict in choices.items():
        if category != 'Verbrauch':
            for key, scenarios in subdict.items():
                print(f"Kategorie: {category}")
                print(f"\tUnterkategorie: {key}")
                for scenario, value in scenarios.items():
                    print(f"\t\tSzenario: {scenario} -> {value}")
                while True:
                    userInput = input("Choose between 'best', 'mean' and 'worst': ")
                    print()
                    if userInput not in ['best', 'mean', 'worst']:
                        print("\033[31mWrong input! Please enter 'best', 'mean', or 'worst'.\033[0m")
                    else:
                        break
                if category in generation:
                    generation[category] *= scenarios[userInput]
                else:
                    print("\033[31mError category wasn't found in generation dictonary.\033[0m")
        elif category == 'Verbrauch':
            print(f"Kategorie: {category}[MWh]")
            for scenario, value in subdict.items():
                print(f"\t\tSzenario: {scenario} -> {value}")
            while True:
                userInput = input("Choose between 'best', 'mean' and 'worst': ")
                print()
                
                if userInput not in ['best', 'mean', 'worst']:
                    print("\033[31mWrong input! Please enter 'best', 'mean', or 'worst'.\033[0m")
                else:
                    break
            generation[category] *= subdict[userInput]
                
        else:
            print("\033[31mError in szenario.\033[0m")
            
    generation['Photovoltaik']*=0.8 # loss factor := 0.8
    
    return simulation(dfList, 2030)

def simulation(dfOriginalList: list[pd.DataFrame], generationYear: int) -> list[pd.DataFrame]:
    dfList = list()
    # Indices for list
    leapYear = [1,5]
    commonYear = [0,2,3,4,6,7,8]
    
    print("Running the simulation...")
    with ThreadPoolExecutor() as executor:
        futures = []
        for currentYear in range(START_YEAR + 1, generationYear + 1):
            # Check if currentYear is a leap year
            if (currentYear % 4 == 0 and (currentYear % 100 != 0 or currentYear % 400 == 0)):
                futures.append(executor.submit(calculationSimulation, dfOriginalList[random.choice(leapYear)].copy(), currentYear, generationYear))
            else:
                futures.append(executor.submit(calculationSimulation, dfOriginalList[random.choice(commonYear)].copy(), currentYear, generationYear))
        for future in futures:
            dfList.append(future.result())
            
    return insertionSort(dfList)

def calculationSimulation(dfOriginal: pd.DataFrame, currentYear: int, generationYear: int) -> pd.DataFrame:
    dfCurrent = dfOriginal.copy()
    # Replace years
    dfCurrent['Datum von'] = dfCurrent['Datum von'].map(lambda x: x.replace(year=currentYear))
    dfCurrent['Datum bis'] = dfCurrent['Datum bis'].map(lambda x: x.replace(year=currentYear))

    # Replace last year
    dfCurrent.iloc[-1, dfCurrent.columns.get_loc('Datum bis')] = dfCurrent.iloc[-1]['Datum bis'].replace(year=currentYear + 1)
    
    for column in dfOriginal.columns:
        if column in ['Datum von', 'Datum bis']:
            continue
        if column in generation:
            # For year 2023 coal
            if column in ['Braunkohle','Steinkohle']:
                dfCurrent[column] = round(dfOriginal[column] * ((-1 / (COAL_EXIT-START_YEAR)) * (currentYear - START_YEAR) + 1), 2)
            else:
                dfCurrent[column] = round(dfOriginal[column] * (((generation[column] / dfOriginal[column].sum() - 1) / (int(generationYear) - START_YEAR)) * (currentYear - START_YEAR) + 1), 2)
        else:
            print(column + " wasn't simulated.")

    
    return storage_sim(dfCurrent.copy())

# Inseriontionsort for right order of dfList
def insertionSort(dfList: list[pd.DataFrame]) -> list[pd.DataFrame]:
    for i in range(1, len(dfList)):
        currentDf = dfList[i]
        currentYear = currentDf['Datum von'].iloc[0].year
        j = i - 1
        while j >= 0 and dfList[j]['Datum von'].iloc[0].year > currentYear:
            dfList[j + 1] = dfList[j]  
            j -= 1
        
        dfList[j + 1] = currentDf

    return dfList

def storage_sim(df: pd.DataFrame) -> pd.DataFrame:

    ren_sum = df.loc[:, 'Biomasse':'Sonstige Erneuerbare'].sum(axis=1)
    df['Überschuss'] = ren_sum - df['Verbrauch']

    df['Speicher'] = 0.0
    df['Speicher Produktion'] = 0.0
    df['Ungenutzte Energie'] = 0.0

    eff = 0.8
    storage = 0.0
    max_fill = 2000
    max_un = 2000
    cap = 1000000

    speicher = []
    speicher_produktion = []
    ungenutzte_energie = []

    for ueberschuss in df['Überschuss']:
        speicherzuwachs = max(ueberschuss, 0) * eff
        speicherzuwachs = min(speicherzuwachs, max_fill)
        speicherzuwachs = min(speicherzuwachs, cap - storage)
        storage += speicherzuwachs

        bedarf = max(-ueberschuss, 0)
        deckung = min(storage, bedarf, max_un)
        storage -= deckung

        ungenutzte_energie.append(max(ueberschuss - speicherzuwachs / eff, 0))
        speicher_produktion.append(deckung)
        speicher.append(storage)


    df['Speicher'] = speicher
    df['Speicher Produktion'] = speicher_produktion
    df['Ungenutzte Energie'] = ungenutzte_energie

    return df