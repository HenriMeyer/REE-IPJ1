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


def ownData(dfList: list[pd.DataFrame]) -> list[pd.DataFrame]:
    while True:
        generationYear = input("Year for forecast: ")
        if generationYear.isdigit() and int(generationYear) > START_YEAR:
                break
        else:
            print(f"\033[31m{generationYear} is an invalid input, it has to be bigger than {START_YEAR} and a digit!\033[0m")
    for key in generation:
        while True:
            try:
                generation[key] = float(input(f"Value for {key}: "))
                break
            except ValueError:
                print("\033[31mInvalid input! Please enter a numeric value.\033[0m")
    return simulation(dfList, generationYear)

def szenario(dfList: list[pd.DataFrame]) -> list[pd.DataFrame]:
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
    
    for key,value in generation.items():
        print(f"{key}:{value}")
    
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

    
    return storage_sim(dfCurrent.copy(), 37000, 50000)

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


def storage_sim(df: pd.DataFrame, pump_cap: float, batt_cap: float) -> pd.DataFrame:
    df.drop(columns = ['Pumpspeicher'])

    ren_sum = df.loc[:, 'Biomasse':'Sonstige Erneuerbare'].sum(axis=1)
    df['Überschuss'] = ren_sum - df['Verbrauch']

    df['Pumpspeicher'] = 0.0
    df['Batteriespeicher'] = 0.0
    df['Pumpspeicher Produktion'] = 0.0
    df['Batteriespeicher Produktion'] = 0.0
    df['Ungenutzte Energie'] = 0.0

    #Pumpspeicher-Parameter
    pump_eff = 0.80
    pump_stor = 0.0
    pump_load = pump_cap/7
    pump_unload = pump_cap/6

    #Batteriespeicher-Parameter
    batt_eff = 0.95
    batt_stor = 0.0
    batt_load = batt_cap/1.5
    batt_unload = batt_cap/1.5

    pump = []
    batt = []
    pump_prod = []
    batt_prod = []
    unused_en = []

    for ueberschuss in df['Überschuss']:
        #Pumpspeicher
        pump_plus = max(ueberschuss, 0) * pump_eff
        pump_plus = min(pump_plus, pump_load)
        pump_plus = min(pump_plus, pump_cap - pump_stor)
        pump_stor += pump_plus

        pump_need = max(-ueberschuss, 0)
        pump_use = min(pump_stor, pump_need, pump_unload)
        pump_stor -= pump_use

        #Batteriespeicher
        batt_plus = max(ueberschuss - pump_plus / pump_eff, 0) * batt_eff
        batt_plus = min(batt_plus, batt_load)
        batt_plus = min(batt_plus, batt_cap - batt_stor)
        batt_stor += batt_plus

        batt_need = max(-ueberschuss - pump_use, 0)
        batt_use = min(batt_stor, batt_need, batt_unload)
        batt_stor -= batt_use

        #Ungenutzte Energie
        verbleibender_ueberschuss = max(ueberschuss - pump_plus / pump_eff - batt_plus / batt_eff, 0)
        unused_en.append(verbleibender_ueberschuss)

        #Speicherung der Werte
        pump_prod.append(pump_use)
        batt_prod.append(batt_use)
        pump.append(pump_stor)
        batt.append(batt_stor)

    df['Pumpspeicher'] = pump
    df['Batteriespeicher'] = batt
    df['Pumpspeicher Produktion'] = pump_prod
    df['Batteriespeicher Produktion'] = batt_prod
    df['Ungenutzte Energie'] = unused_en

    return df

