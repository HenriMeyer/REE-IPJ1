import pandas as pd
from concurrent.futures import ThreadPoolExecutor

generation = {
    'Biomasse': 40000000,
    'Wasserkraft': 40000000,
    'Wind Offshore': 40000000,
    'Wind Onshore': 40000000,
    'Photovoltaik': 40000000,
    'Sonstige Erneuerbare': 40000000,
    'Braunkohle': 40000000,
    'Steinkohle': 40000000,
    'Erdgas': 40000000,
    'Pumpspeicher': 40000000,
    'Sonstige Konventionelle': 40000000,
    'Verbrauch': 40000000
}

def ownData(df: pd.DataFrame) -> list:
    startYear = int(df['Datum von'].dt.year.iloc[0])
    while True:
        generationYear = input("Year for forecast: ")
        if generationYear.isdigit() and int(generationYear) > startYear:
                break
        else:
            print(f"\033[31m{generationYear} is an invalid input, it has to be bigger than {startYear} and a digit!\033[0m")
    for key in generation:
        while True:
            try:
                generation[key] = float(input(f"Value for {key}: "))
                break
            except ValueError:
                print("\033[31mInvalid input! Please enter a numeric value.\033[0m")
    return simulation(df, generationYear)

def szenario(df: pd.DataFrame) -> list:
    userInput = input("Choose between 'best','mean' and 'worst': ")
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
    return simulation(df, 2030)

def simulation(df: pd.DataFrame, generationYear: int) -> list:
    startYear = int(df['Datum von'].dt.year.iloc[0])
    dfList = []
    print("Running the simulation...")
    with ThreadPoolExecutor() as executor:
        futures = []
        for currentYear in range(startYear + 1, int(generationYear) + 1):
            futures.append(executor.submit(calculationSimulation, df.copy(), currentYear, generationYear, startYear))
        for future in futures:
            dfList.append(future.result())
    
    return dfList

def calculationSimulation(dfOriginal: pd.DataFrame, currentYear: int, generationYear: int, startYear: int) -> pd.DataFrame:
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
            dfCurrent[column] = round(dfOriginal[column] * (((generation[column] / dfOriginal[column].sum() - 1) / (int(generationYear) - startYear)) * (currentYear - startYear) + 1), 2)
        else:
            print(column + " wasn't simulated.")
    return dfCurrent.copy()