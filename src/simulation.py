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
    'Wärmepumpe': 1,
    'E-Auto': 1,
    'E-LKW': 1,
    'Verbrauch': 685000000
}

# Installierte Leistungen in MW
photovoltaik = {
    'Installierte Leistung [MW]' : {
        'worst' : 180000,
        'mean' : 215000,
        'best' : 240000
    },
    'Globalstrahlung [Wh/m^2]' : {
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
    'worst' : 679750000,#-95250000 von E-Auto/Wärmepumpe
    'mean' : 615687500,#-69312500 von E-Auto/Wärmepumpe
    'best' : 559680000#-30200000 von E-Auto/Wärmepumpe
}

waermepumpe =  {
    'Wärmepumpe' : {
        'worst' : 0,
        'mean' : 3900000,
        'best' : 4400000
    }
}
eauto = {
    'E-Auto' : {
        'worst' : 6410000,
        'mean' : 9660000,
        'best' : 19410000
    }
}
start = {
    'Wärmepumpe' : 1600000,
    'E-Auto' : 1590000,
    'E-LKW': 2000
}
elkw = {
    'E-LKW' : {
        'worst' : 2280000,
        'mean' :17100000,
        'best' : 31920000
    }
}
speicher = {
    'Speicher' : {
    'worst' : {
        'pump_cap' : 45000,
        'pump_load' : 9700,
        'batt_cap' : 1924,
        'batt_load' : 1500
    },
    'mean' : {
        'pump_cap' : 70000,
        'pump_load' : 15000,
        'batt_cap' : 60000,
        'batt_load' : 15000
    },
    'best' : {
        'pump_cap' : 120000,
        'pump_load' : 30000,
        'batt_cap' : 100000,
        'batt_load' : 25000
    }
    }
}
speicher_use = {
    'pump_cap' : 1,
    'pump_load' : 1,
    'batt_cap' : 1,
    'batt_load' : 1
}


def scenarioOverall(dfList: list[pd.DataFrame], loadProfile: list[pd.DataFrame]) -> list[pd.DataFrame]:
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
        'Verbrauch': consumption,
        'Wärmepumpe' : waermepumpe,
        'E-Auto' : eauto,
        'E-LKW': elkw,
        'Speicher' : speicher
    }
    global generation
    global speicher_use
    generation.update({'Photovoltaik': 1, 'Wind Offshore': 1, 'Wind Onshore': 1, 'Verbrauch': 1})

    for category, subdict in choices.items():
        if category == 'Speicher':
            speicher_use['pump_cap'] = speicher['Speicher'][userInput]['pump_cap']
            speicher_use['pump_load'] = speicher['Speicher'][userInput]['pump_load']
            speicher_use['batt_cap'] = speicher['Speicher'][userInput]['batt_cap']
            speicher_use['batt_load'] = speicher['Speicher'][userInput]['batt_load']
        
        elif category != 'Verbrauch':
            for key, scenarios in subdict.items():
                if userInput in scenarios:
                    generation[category] *= scenarios[userInput]
        elif category == 'Verbrauch':
            if userInput in subdict:
                generation[category] *= subdict[userInput]
        else:
            print("\033[31mError in szenario.\033[0m")

    generation['Photovoltaik']*=0.8 # loss factor := 0.8
        
    return simulation(dfList, 2030, loadProfile)
                
        

def scenarioEach(dfList: list[pd.DataFrame], loadProfile: list[pd.DataFrame]) -> list[pd.DataFrame]:
    choices = {
        'Photovoltaik': photovoltaik,
        'Wind Offshore': windOffshore,
        'Wind Onshore': windOnshore,
        'Verbrauch': consumption,
        'Wärmepumpe' : waermepumpe,
        'E-Auto' : eauto,
        'E-LKW' : elkw,
        'Speicher' : speicher
    }
    global generation
    global speicher_use
    generation.update({'Photovoltaik': 1, 'Wind Offshore': 1, 'Wind Onshore': 1, 'Verbrauch': 1})
    
    for category, subdict in choices.items():
        if category == 'Speicher':
            print(f"Kategorie: {category}")
            while True:
                    userInput = input("Choose between 'best', 'mean' and 'worst': ")
                    print()
                    if userInput not in ['best', 'mean', 'worst']:
                        print("\033[31mWrong input! Please enter 'best', 'mean', or 'worst'.\033[0m")
                    else:
                        speicher_use['pump_cap'] = speicher['Speicher'][userInput]['pump_cap']
                        speicher_use['pump_load'] = speicher['Speicher'][userInput]['pump_load']
                        speicher_use['batt_cap'] = speicher['Speicher'][userInput]['batt_cap']
                        speicher_use['batt_load'] = speicher['Speicher'][userInput]['batt_load']
                        break
        elif category != 'Verbrauch':
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
    
    return simulation(dfList, 2030, loadProfile)



def simulation(dfOriginalList: list[pd.DataFrame], generationYear: int, loadProfile: list[pd.DataFrame]) -> list[pd.DataFrame]:
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
                futures.append(executor.submit(calculationSimulation, dfOriginalList[random.choice(leapYear)].copy(), currentYear, generationYear, loadProfile['leap']))
            else:
                futures.append(executor.submit(calculationSimulation, dfOriginalList[random.choice(commonYear)].copy(), currentYear, generationYear, loadProfile['normal']))
        for future in futures:
            dfList.append(future.result())
    
    dfList = linearBeginning(dfList)
    with ThreadPoolExecutor() as executor:
        futures = []
        for df in dfList:
            futures.append(executor.submit(storage_sim, df, int(df['Datum von'].dt.year.iloc[0]), generationYear))
        for future in futures:
            dfList.append(future.result())

    return insertionSort(dfList)

def calculationSimulation(dfOriginal: pd.DataFrame, currentYear: int, generationYear: int, loadProfile: pd.DataFrame) -> pd.DataFrame:
    dfCurrent = dfOriginal.copy()
    # Replace years
    dfCurrent['Datum von'] = dfCurrent['Datum von'].map(lambda x: x.replace(year=currentYear))
    dfCurrent['Datum bis'] = dfCurrent['Datum bis'].map(lambda x: x.replace(year=currentYear))

    # Replace last year
    dfCurrent.iloc[-1, dfCurrent.columns.get_loc('Datum bis')] = dfCurrent.iloc[-1]['Datum bis'].replace(year=currentYear + 1)
    
    dfOriginal['E-Auto'] = 0
    dfOriginal['Wärmepumpe'] = 0
    dfOriginal['E-LKW'] = 0

    for column in (dfOriginal.columns):
        if column in ['Datum von', 'Datum bis']:
            continue
        if column in generation:
            # For year 2023 coal
            if column in ['Braunkohle','Steinkohle']:
                dfCurrent[column] = round(dfOriginal[column] * ((-1 / (COAL_EXIT-START_YEAR)) * (currentYear - START_YEAR) + 1), 2)
            elif column in ['E-Auto', 'E-LKW', 'Wärmepumpe']:
                dfCurrent[column] = round((loadProfile[column]*(generation[column]/(int(generationYear) - START_YEAR) * (currentYear - START_YEAR) + start[column])),2)
            else:
                dfCurrent[column] = round(dfOriginal[column] * (((generation[column] / dfOriginal[column].sum() - 1) / (int(generationYear) - START_YEAR)) * (currentYear - START_YEAR) + 1), 2)
        else:
            print(column + " wasn't simulated.")

    dfCurrent['Verbrauch'] += dfCurrent['E-Auto'] + dfCurrent['Wärmepumpe']
    
    return dfCurrent.copy()

def linearBeginning(dfList: list[pd.DataFrame]) -> list[pd.DataFrame]:
    maxIndex = 8 # Until which index shall it be linearised -> 2:00 o'clock
    for i in range(1,len(dfList)):
        dfCurrent = dfList[i]
        dfBefore = dfList[i-1]
        for column in dfCurrent.columns:
            if column not in ["Datum von", "Datum bis", "Photovoltaik", "Verbrauch", "Pumpspeicher"]:
                if column in dfBefore.columns:
                    sumCurrentColumnBuffer = dfCurrent[column].sum()
                    valueCurrent = dfCurrent.at[maxIndex - 1, column]
                    valueBefore = dfBefore.iloc[-1][column]
                    for i in range(0, maxIndex):
                        dfCurrent.at[i, column] = valueBefore + (valueCurrent - valueBefore) * ((i + 1) / maxIndex)
                    dfCurrent[column] = round(dfCurrent[column] * (dfCurrent[column].sum() / sumCurrentColumnBuffer), 2)
                else:
                    print(f"Column '{column}' not found in the previous DataFrame!")
    return dfList.copy()
            

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

    return dfList.copy()


def storage_sim(df: pd.DataFrame, currentYear, generationYear) -> pd.DataFrame:
    df.drop(columns = ['Pumpspeicher'])

    ren_sum = df.loc[:, 'Biomasse':'Sonstige Erneuerbare'].sum(axis=1)
    df['Überschuss'] = ren_sum - df['Verbrauch']

    df['Pumpspeicher'] = 0.0
    df['Batteriespeicher'] = 0.0
    df['Pumpspeicher Produktion'] = 0.0
    df['Batteriespeicher Produktion'] = 0.0
    df['Ungenutzte Energie'] = 0.0

    #Pumpspeicher-Parameter
    pump_cap = round((speicher_use['pump_cap']-speicher['Speicher']['worst']['pump_cap']/(int(generationYear) - START_YEAR) * (currentYear - START_YEAR) + speicher['Speicher']['worst']['pump_cap']),2)
    pump_eff = 0.80
    pump_stor = 0.0
    pump_load = round((speicher_use['pump_load']-speicher['Speicher']['worst']['pump_load']/(int(generationYear) - START_YEAR) * (currentYear - START_YEAR) + speicher['Speicher']['worst']['pump_load']),2)
    pump_unload = pump_load

    #Batteriespeicher-Parameter
    batt_cap = round((speicher_use['batt_cap']-speicher['Speicher']['worst']['batt_cap']/(int(generationYear) - START_YEAR) * (currentYear - START_YEAR) + speicher['Speicher']['worst']['batt_cap']),2)
    batt_eff = 0.95
    batt_stor = 0.0
    batt_load = round((speicher_use['batt_load']-speicher['Speicher']['worst']['batt_load']/(int(generationYear) - START_YEAR) * (currentYear - START_YEAR) + speicher['Speicher']['worst']['batt_load']),2)
    batt_unload = pump_load

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
        pump_prod.append(round(pump_use, 2))
        batt_prod.append(round(batt_use, 2))
        pump.append(round(pump_stor, 2))
        batt.append(round(batt_stor, 2))

    df['Pumpspeicher'] = pump
    df['Batteriespeicher'] = batt
    df['Pumpspeicher Produktion'] = pump_prod
    df['Batteriespeicher Produktion'] = batt_prod
    df['Ungenutzte Energie'] = unused_en

    new_order = [
        'Datum von', 'Datum bis',
        'Biomasse', 'Wasserkraft', 'Wind Offshore', 'Wind Onshore',
        'Photovoltaik', 'Sonstige Erneuerbare', 'Pumpspeicher Produktion',
        'Batteriespeicher Produktion','Braunkohle', 'Steinkohle', 'Erdgas',
        'Sonstige Konventionelle','Wärmepumpe','E-Auto', 'E-LKW', 'Verbrauch',
        'Batteriespeicher', 'Pumpspeicher', 'Überschuss', 'Ungenutzte Energie'
    ]
    df = df[new_order]
    return df