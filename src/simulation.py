import pandas as pd
import random
from concurrent.futures import ThreadPoolExecutor

START_YEAR = 2023

generation = {
    'Biomasse': 40000000,
    'Wasserkraft': 40000000,
    'Wind Offshore': 40000000, # kommt raus
    'Wind Onshore': 40000000, # kommt raus
    'Photovoltaik': 40000000, # kommt raus
    'Sonstige Erneuerbare': 40000000,
    'Braunkohle': 40000000,
    'Steinkohle': 40000000,
    'Erdgas': 40000000,
    'Pumpspeicher': 40000000,
    'Sonstige Konventionelle': 40000000,
    'Verbrauch': 40000000
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
    while True:
        userInput = input("Choose between 'best','mean' and 'worst': ")
        if userInput not in ['best', 'mean', 'worst']:
            print("\033[31mWrong input!\033[0m")
        else:
            break
        global generation
    match userInput.lower():
            case "best":
                generation = {
                    'Biomasse': 37826000,
                    'Wasserkraft': 15000000,
                    'Wind Offshore': 93100000,
                    'Wind Onshore': 282000000,
                    'Photovoltaik': 210000000,
                    'Sonstige Erneuerbare': 1100000,
                    'Braunkohle': 78000000,
                    'Steinkohle': 40000000,
                    'Erdgas': 50143000,
                    'Pumpspeicher': 10647000,
                    'Sonstige Konventionelle': 12000000,
                    'Verbrauch': 587000000
                }
            case "mean":
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
            case "worst":
                generation = {
                    'Biomasse': 37826000,
                    'Wasserkraft': 15000000,
                    'Wind Offshore': 74000000,
                    'Wind Onshore': 144000000,
                    'Photovoltaik': 93000000,
                    'Sonstige Erneuerbare': 1100000,
                    'Braunkohle': 78000000,
                    'Steinkohle': 40000000,
                    'Erdgas': 50143000,
                    'Pumpspeicher': 10647000,
                    'Sonstige Konventionelle': 12000000,
                    'Verbrauch': 775000000
                }
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
