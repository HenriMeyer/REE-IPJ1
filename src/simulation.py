import pandas as pd
import random
import numpy as np
from concurrent.futures import ThreadPoolExecutor

START_YEAR = 2024
COAL_EXIT = 2038

generation = {
    'Biomasse': 43431161,
    'Wasserkraft': 15000000,
    'Wind Offshore': 94620000,
    'Wind Onshore': 228060000,
    'Photovoltaik': 157380000,
    'Sonstige Erneuerbare': 1100000,
    'Braunkohle': 78000000,
    'Steinkohle': 40000000,
    'Erdgas': 11250, # max power -> Regelbare Kraftwerke
    'Pumpspeicher': 10647000,
    'Sonstige Konventionelle': 11193660,
    'Wärmepumpe': 1,
    'E-Auto': 1,
    'E-LKW': 1,
    'Verbrauch': 685000000
}

# Installierte Leistungen in MW
photovoltaik = {
    'Installierte Leistung [MW]' : {
        'min' : 180000,
        'mid' : 215000,
        'max' : 240000
    },
    'Globalstrahlung [Wh/m^2]' : {
        'min' : 1036,
        'mid' : 1151.5,
        'max' : 1266.6
    }
}

windOffshore = {
    'Installierte Leistung [MW]' : {
        'min' : 8500,
        'mid' : 22000,
        'max' : 30000
    },
    'Volllaststunden [h]' : {
        'min' : 4500,
        'mid' : 5000,
        'max' : 6000
    }
}

windOnshore = {
    'Installierte Leistung [MW]' : {
        'min' : 60000,
        'mid' : 75000,
        'max' : 100000
    },
    'Volllaststunden [h]' : {
        'min' : 2700,
        'mid' : 3000,
        'max' : 3300
    }
}

consumption = {
    'max' : 646198000,#-95250000 von E-Auto/Wärmepumpe -33552000 E-LKW
    'mid' : 597735500,#-69312500 von E-Auto/Wärmepumpe -17952000 E-LKW
    'min' : 557328000#-30200000 von E-Auto/Wärmepumpe -2352000 E-LKW
}

waermepumpe =  {
    'Wärmepumpe' : {
        'min' : 0,
        'mid' : 3900000,
        'max' : 4400000
    },
    'Verbrauch in [kWh]' : {
        'min' : 5130,
        'mid' : 6290,
        'max' : 7850
    }
}
eauto = {
    'E-Auto' : {
        'min' : 6410000,
        'mid' : 9660000,
        'max' : 19410000
    }
}
start = {
    'Wärmepumpe' : 1600000,
    'E-Auto' : 1590000,
    'E-LKW': 2000,
    'Photovoltaik': 96000,
    'Wind Onshore': 61000,
    'Wind Offshore': 8500,
}
elkw = {
    'E-LKW' : {
        'min' : 98000,
        'mid' : 748000,
        'max' : 1398000
    }
}
storage = {
    'Speicher' : {
    'min' : {
        'pump_cap' : 45000,
        'pump_load' : 9700,
        'batt_cap' : 1924,
        'batt_load' : 1500
    },
    'mid' : {
        'pump_cap' : 70000,
        'pump_load' : 15000,
        'batt_cap' : 60000,
        'batt_load' : 15000
    },
    'max' : {
        'pump_cap' : 120000,
        'pump_load' : 30000,
        'batt_cap' : 100000,
        'batt_load' : 25000
    }
    }
}
storageUsage = {
    'pump_cap' : 1,
    'pump_load' : 1,
    'batt_cap' : 1,
    'batt_load' : 1
}
# Pro Einheit oder MW in Euro(Muss noch überarbeitet werden nur zum testen)
price = {
    'Wind Onshore' : 1600000,
    'Wind Offshore' : 3250000,
    'Photovoltaik' : 833000,
    'E-Auto' : 50000,
    'E-LKW' : 300000,
    'Wärmepumpe' : 25000
}

def scenarios(dfList: list[pd.DataFrame], loadProfile: list[pd.DataFrame]) -> dict[str, list]:
    choicesSzenarios = ["retention", "imbalance", "no storage", "light breeze", "confidence", "cold winter", "smard"]

    while True:
        print(f"Available scenarios:")
        for szenario in choicesSzenarios:
            print(f"- {szenario}")
        print("You may also write \033[1m'all'\033[0m to write all szenarios!")
        userInput = input("Type in one of the mentioned scenarios: ").lower()
        if userInput not in choicesSzenarios and userInput != "all":
            print("\033[31mWrong input!\033[0m")
        else:
            break
    
    global generation
    results = []
    install_values = {
        'Photovoltaik': start['Photovoltaik'],
        'Wind Onshore': start['Wind Onshore'],
        'Wind Offshore': start['Wind Offshore'],
        'E-Auto': start['E-Auto'],
        'E-LKW': start['E-LKW'],
        'Wärmepumpe': start['Wärmepumpe']
    }

    def defineSzenario(scenario: str):
        match scenario:
            case "retention":
                install_values.update({
                    'Photovoltaik': photovoltaik['Installierte Leistung [MW]']['min'],
                    'Wind Onshore': windOnshore['Installierte Leistung [MW]']['min'],
                    'Wind Offshore': windOffshore['Installierte Leistung [MW]']['min'],
                    'E-Auto': eauto['E-Auto']['min'],
                    'E-LKW': elkw['E-LKW']['min'],
                    'Wärmepumpe': waermepumpe['Wärmepumpe']['mid']
                })
                generation['Photovoltaik'] = install_values['Photovoltaik'] * photovoltaik['Globalstrahlung [Wh/m^2]']['mid'] * 0.8
                generation['Wind Onshore'] = install_values['Wind Onshore'] * windOnshore['Volllaststunden [h]']['mid']
                generation['Wind Offshore'] = install_values['Wind Offshore'] * windOffshore['Volllaststunden [h]']['mid']
                generation['Verbrauch'] = consumption['mid']
                generation['E-Auto'] = install_values['E-Auto']
                generation['E-LKW'] = install_values['E-LKW']
                generation['Wärmepumpe'] = install_values['Wärmepumpe'] * waermepumpe['Verbrauch in [kWh]']['mid']
                for storageItem in ["pump_cap", "pump_load", "batt_cap", "batt_load"]:
                    storageUsage[storageItem] = storage['Speicher']['min'][storageItem]
            case "imbalance":
                install_values.update({
                    'Photovoltaik': photovoltaik['Installierte Leistung [MW]']['min'],
                    'Wind Onshore': windOnshore['Installierte Leistung [MW]']['min'],
                    'Wind Offshore': windOffshore['Installierte Leistung [MW]']['min'],
                    'E-Auto': eauto['E-Auto']['max'],
                    'E-LKW': elkw['E-LKW']['max'],
                    'Wärmepumpe': waermepumpe['Wärmepumpe']['max']
                })
                generation['Photovoltaik'] = install_values['Photovoltaik'] * photovoltaik['Globalstrahlung [Wh/m^2]']['mid'] * 0.8
                generation['Wind Onshore'] = install_values['Wind Onshore'] * windOnshore['Volllaststunden [h]']['mid']
                generation['Wind Offshore'] = install_values['Wind Offshore'] * windOffshore['Volllaststunden [h]']['mid']
                generation['Verbrauch'] = consumption['max']
                generation['E-Auto'] = install_values['E-Auto']
                generation['E-LKW'] = install_values['E-LKW']
                generation['Wärmepumpe'] = install_values['Wärmepumpe'] * waermepumpe['Verbrauch in [kWh]']['mid']
                for storageItem in ["pump_cap", "pump_load", "batt_cap", "batt_load"]:
                    storageUsage[storageItem] = storage['Speicher']['min'][storageItem]
            case "no storage":
                install_values.update({
                    'Photovoltaik': photovoltaik['Installierte Leistung [MW]']['mid'],
                    'Wind Onshore': windOnshore['Installierte Leistung [MW]']['mid'],
                    'Wind Offshore': windOffshore['Installierte Leistung [MW]']['mid'],
                    'E-Auto': eauto['E-Auto']['max'],
                    'E-LKW': elkw['E-LKW']['mid'],
                    'Wärmepumpe': waermepumpe['Wärmepumpe']['max']
                })
                generation['Photovoltaik'] = install_values['Photovoltaik'] * photovoltaik['Globalstrahlung [Wh/m^2]']['mid'] * 0.8
                generation['Wind Onshore'] = install_values['Wind Onshore'] * windOnshore['Volllaststunden [h]']['mid']
                generation['Wind Offshore'] = install_values['Wind Offshore'] * windOffshore['Volllaststunden [h]']['mid']
                generation['Verbrauch'] = consumption['mid']
                generation['E-Auto'] = install_values['E-Auto']
                generation['E-LKW'] = install_values['E-LKW']
                generation['Wärmepumpe'] = install_values['Wärmepumpe'] * waermepumpe['Verbrauch in [kWh]']['mid']
                for storageItem in ["pump_cap", "pump_load", "batt_cap", "batt_load"]:
                    storageUsage[storageItem] = storage['Speicher']['min'][storageItem]
            case "light breeze":
                install_values.update({
                    'Photovoltaik': photovoltaik['Installierte Leistung [MW]']['mid'],
                    'Wind Onshore': windOnshore['Installierte Leistung [MW]']['mid'],
                    'Wind Offshore': windOffshore['Installierte Leistung [MW]']['mid'],
                    'E-Auto': eauto['E-Auto']['mid'],
                    'E-LKW': elkw['E-LKW']['mid'],
                    'Wärmepumpe': waermepumpe['Wärmepumpe']['mid']
                })
                generation['Photovoltaik'] = install_values['Photovoltaik'] * photovoltaik['Globalstrahlung [Wh/m^2]']['min'] * 0.8
                generation['Wind Onshore'] = install_values['Wind Onshore'] * windOnshore['Volllaststunden [h]']['min']
                generation['Wind Offshore'] = install_values['Wind Offshore'] * windOffshore['Volllaststunden [h]']['min']
                generation['Verbrauch'] = consumption['mid']
                generation['E-Auto'] = install_values['E-Auto']
                generation['E-LKW'] = install_values['E-LKW']
                generation['Wärmepumpe'] = install_values['Wärmepumpe'] * waermepumpe['Verbrauch in [kWh]']['mid']
                for storageItem in ["pump_cap", "pump_load", "batt_cap", "batt_load"]:
                    storageUsage[storageItem] = storage['Speicher']['min'][storageItem]
            case "confidence":
                install_values.update({
                    'Photovoltaik': photovoltaik['Installierte Leistung [MW]']['max'],
                    'Wind Onshore': windOnshore['Installierte Leistung [MW]']['max'],
                    'Wind Offshore': windOffshore['Installierte Leistung [MW]']['max'],
                    'E-Auto': eauto['E-Auto']['max'],
                    'E-LKW': elkw['E-LKW']['max'],
                    'Wärmepumpe': waermepumpe['Wärmepumpe']['max']
                })
                generation['Photovoltaik'] = install_values['Photovoltaik'] * photovoltaik['Globalstrahlung [Wh/m^2]']['max'] * 0.8
                generation['Wind Onshore'] = install_values['Wind Onshore'] * windOnshore['Volllaststunden [h]']['max']
                generation['Wind Offshore'] = install_values['Wind Offshore'] * windOffshore['Volllaststunden [h]']['max']
                generation['Verbrauch'] = consumption['min']
                generation['E-Auto'] = install_values['E-Auto']
                generation['E-LKW'] = install_values['E-LKW']
                generation['Wärmepumpe'] = install_values['Wärmepumpe'] * waermepumpe['Verbrauch in [kWh]']['mid']
                for storageItem in ["pump_cap", "pump_load", "batt_cap", "batt_load"]:
                    storageUsage[storageItem] = storage['Speicher']['max'][storageItem]
            case "cold winter":
                install_values.update({
                    'Photovoltaik': photovoltaik['Installierte Leistung [MW]']['max'],
                    'Wind Onshore': windOnshore['Installierte Leistung [MW]']['max'],
                    'Wind Offshore': windOffshore['Installierte Leistung [MW]']['max'],
                    'E-Auto': eauto['E-Auto']['max'],
                    'E-LKW': elkw['E-LKW']['max'],
                    'Wärmepumpe': waermepumpe['Wärmepumpe']['max']
                })
                generation['Photovoltaik'] = install_values['Photovoltaik'] * photovoltaik['Globalstrahlung [Wh/m^2]']['mid'] * 0.8
                generation['Wind Onshore'] = install_values['Wind Onshore'] * windOnshore['Volllaststunden [h]']['mid']
                generation['Wind Offshore'] = install_values['Wind Offshore'] * windOffshore['Volllaststunden [h]']['mid']
                generation['Verbrauch'] = consumption['mid']
                generation['E-Auto'] = install_values['E-Auto']
                generation['E-LKW'] = install_values['E-LKW']
                generation['Wärmepumpe'] = install_values['Wärmepumpe'] * waermepumpe['Verbrauch in [kWh]']['min']
                for storageItem in ["pump_cap", "pump_load", "batt_cap", "batt_load"]:
                    storageUsage[storageItem] = storage['Speicher']['max'][storageItem]
            case "smard":
                startSMARD = int(dfList[0]['Datum von'].dt.year.iloc[0])
                for column in dfList[0].columns:
                    if column in ['Datum von', 'Datum bis']:
                        continue
                    buffer = list()
                    for i in range(len(dfList) - 1):
                        buffer.append(dfList[i + 1][column].sum() - dfList[i][column].sum())
                    generation[column] = dfList[0][column].sum() + sum(buffer) / len(buffer) * (START_YEAR - startSMARD)
                    print(column + ": " + str(generation[column]))
                generation['E-Auto'] = eauto['E-Auto']['mid']
                generation['E-LKW'] = elkw['E-LKW']['mid']
                generation['Wärmepumpe'] = waermepumpe['Wärmepumpe']['max']*waermepumpe['Verbrauch in [kWh]']['min']
                for storageItem in ["pump_cap", "pump_load", "batt_cap", "batt_load"]:
                    storageUsage[storageItem] = storage['Speicher']['mid'][storageItem]
                    

    if userInput == "all":
        with ThreadPoolExecutor() as executor:
            futures = []
            for scenario in choicesSzenarios:
                defineSzenario(scenario)
                futures.append(executor.submit(simulation, dfList, 2030, loadProfile, scenario))
            for future in futures:
                results.append(future.result())
        szenarioDict = dict()
        for dictonary in results:
            szenarioDict.update(dictonary)
        return szenarioDict
    else:
        defineSzenario(userInput)
        return simulation(dfList, 2030, loadProfile, userInput, install_values)    


# def ownSzenario(dfList: list[pd.DataFrame], loadProfile: list[pd.DataFrame]) -> list[pd.DataFrame]:
#     choices = {
#         'Photovoltaik': photovoltaik,
#         'Wind Offshore': windOffshore,
#         'Wind Onshore': windOnshore,
#         'Verbrauch': consumption,
#         'Wärmepumpe' : waermepumpe,
#         'E-Auto' : eauto,
#         'E-LKW' : elkw,
#         'Speicher' : speicher
#     }
#     global generation
#     global storageUsage
#     generation.update({'Photovoltaik': 1, 'Wind Offshore': 1, 'Wind Onshore': 1, 'Verbrauch': 1})
    
#     for category, subdict in choices.items():
#         if category == 'Speicher':
#             print(f"Kategorie: {category}")
#             while True:
#                     userInput = input("Choose between 'max', 'mid' and 'min': ")
#                     print()
#                     if userInput not in ['max', 'mid', 'min']:
#                         print("\033[31mWrong input! Please enter 'max', 'mid', or 'min'.\033[0m")
#                     else:
#                         storageUsage['pump_cap'] = speicher['Speicher'][userInput]['pump_cap']
#                         storageUsage['pump_load'] = speicher['Speicher'][userInput]['pump_load']
#                         storageUsage['batt_cap'] = speicher['Speicher'][userInput]['batt_cap']
#                         storageUsage['batt_load'] = speicher['Speicher'][userInput]['batt_load']
#                         break
#         elif category != 'Verbrauch':
#             for key, scenarios in subdict.items():
#                 print(f"Kategorie: {category}")
#                 print(f"\tUnterkategorie: {key}")
#                 for scenario, value in scenarios.items():
#                     print(f"\t\tSzenario: {scenario} -> {value}")
#                 while True:
#                     userInput = input("Choose between 'max', 'mid' and 'min': ")
#                     print()
#                     if userInput not in ['max', 'mid', 'min']:
#                         print("\033[31mWrong input! Please enter 'max', 'mid', or 'min'.\033[0m")
#                     else:
#                         break
#                 if category in generation:
#                     generation[category] *= scenarios[userInput]
#                 else:
#                     print("\033[31mError category wasn't found in generation dictonary.\033[0m")
#         elif category == 'Verbrauch':
#             print(f"Kategorie: {category}[MWh]")
#             for scenario, value in subdict.items():
#                 print(f"\t\tSzenario: {scenario} -> {value}")
#             while True:
#                 userInput = input("Choose between 'max', 'mid' and 'min': ")
#                 print()
                
#                 if userInput not in ['max', 'mid', 'min']:
#                     print("\033[31mWrong input! Please enter 'max', 'mid', or 'min'.\033[0m")
#                 else:
#                     break
#             generation[category] *= subdict[userInput]
#         else:
#             print("\033[31mError in szenario.\033[0m")
            
#     generation['Photovoltaik']*=0.8 # loss factor := 0.8
    
#     return simulation(dfList, 2030, loadProfile)



def simulation(dfOriginalList: list[pd.DataFrame], generationYear: int, loadProfile: list[pd.DataFrame], nameSzenario: str, install_values: list) -> dict[str, list]:
    dfList = list()
    # Indices for list
    leapYear = [1,5,9]
    commonYear = [0,2,3,4,6,7,8]
    
    print("Running the simulation...")
    with ThreadPoolExecutor() as executor:
        futures = []
        for currentYear in range(START_YEAR + 1, generationYear + 1):
            # Check if currentYear is a leap year
            if (currentYear % 4 == 0 and (currentYear % 100 != 0 or currentYear % 400 == 0)):
                futures.append(executor.submit(calculationSimulation, dfOriginalList[random.choice(leapYear)].copy(), currentYear, generationYear, loadProfile['leap'], install_values))
            else:
                futures.append(executor.submit(calculationSimulation, dfOriginalList[random.choice(commonYear)].copy(), currentYear, generationYear, loadProfile['normal'], install_values))
        for future in futures:
            dfList.append(future.result())
    
    dfList = linearBeginning(dfList)
    with ThreadPoolExecutor() as executor:
        futures = []
        for df in dfList:
            futures.append(executor.submit(storage_sim, df, int(df['Datum von'].dt.year.iloc[0]), generationYear))
        for future in futures:
            dfList.append(future.result()) 
    dfDict = dict()
    dfDict[nameSzenario] = insertionSort(dfList)
    return dfDict

def calculationSimulation(dfOriginal: pd.DataFrame, currentYear: int, generationYear: int, loadProfile: pd.DataFrame, install_values: list) -> pd.DataFrame:
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

    
    dfCurrent['Price'] = 0
    dfCurrent.at[0, 'Price'] = sum((install_values[tech] - start[tech]) / (generationYear - START_YEAR) * (currentYear - START_YEAR) * price[tech] for tech in install_values)

    dfCurrent['Verbrauch'] += dfCurrent['E-Auto'] + dfCurrent['Wärmepumpe'] + dfCurrent['E-LKW']
    dfCurrent['Verbrauch'] = dfCurrent['Verbrauch'].round(2)
    
    return dfCurrent.copy()

def linearBeginning(dfList: list[pd.DataFrame]) -> list[pd.DataFrame]:
    maxIndex = 8 # Until which index shall it be linearised -> 2:00 o'clock
    for i in range(1,len(dfList)):
        dfCurrent = dfList[i]
        dfBefore = dfList[i-1]
        for column in dfCurrent.columns:
            if column not in ["Datum von", "Datum bis", "Photovoltaik", "Verbrauch", "Pumpspeicher", "Price"]:
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
    pump_cap = round((storageUsage['pump_cap'] - storage['Speicher']['min']['pump_cap']/(int(generationYear) - START_YEAR) * (currentYear - START_YEAR) + storage['Speicher']['min']['pump_cap']),2)
    pump_eff = 0.80
    pump_stor = 0.0
    pump_load = round((storageUsage['pump_load'] - storage['Speicher']['min']['pump_load']/(int(generationYear) - START_YEAR) * (currentYear - START_YEAR) + storage['Speicher']['min']['pump_load']),2)
    pump_unload = pump_load

    #Batteriespeicher-Parameter
    batt_cap = round((storageUsage['batt_cap'] - storage['Speicher']['min']['batt_cap']/(int(generationYear) - START_YEAR) * (currentYear - START_YEAR) + storage['Speicher']['min']['batt_cap']),2)
    batt_eff = 0.95
    batt_stor = 0.0
    batt_load = round((storageUsage['batt_load'] - storage['Speicher']['min']['batt_load']/(int(generationYear) - START_YEAR) * (currentYear - START_YEAR) + storage['Speicher']['min']['batt_load']),2)
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
    df['Konventionell'] = np.maximum(df['Verbrauch']-df.loc[:,['Biomasse','Wasserkraft','Wind Offshore','Wind Onshore','Photovoltaik','Sonstige Erneuerbare','Pumpspeicher Produktion',
        'Batteriespeicher Produktion']].sum(axis=1), 0)
    df['Anteil Erneuerbar [%]'] = (df.loc[:,['Biomasse','Wasserkraft','Wind Offshore','Wind Onshore','Photovoltaik','Sonstige Erneuerbare','Pumpspeicher Produktion',
        'Batteriespeicher Produktion']].sum(axis=1)/df['Verbrauch']*100)
    
    columns_to_round = [
        'Pumpspeicher', 'Batteriespeicher',
        'Pumpspeicher Produktion', 'Batteriespeicher Produktion',
        'Überschuss', 'Ungenutzte Energie', 'Konventionell', 'Anteil Erneuerbar [%]'
    ]
    df[columns_to_round] = df[columns_to_round].round(2)
    
    new_order = [
        'Datum von', 'Datum bis',
        'Biomasse', 'Wasserkraft', 'Wind Offshore', 'Wind Onshore',
        'Photovoltaik', 'Sonstige Erneuerbare', 'Pumpspeicher Produktion',
        'Batteriespeicher Produktion','Braunkohle', 'Steinkohle', 'Erdgas',
        'Sonstige Konventionelle','Wärmepumpe','E-Auto', 'E-LKW', 'Verbrauch',
        'Batteriespeicher', 'Pumpspeicher', 'Überschuss', 'Ungenutzte Energie',
        'Konventionell', 'Anteil Erneuerbar [%]','Price'
    ]
    df = df[new_order]
    
    return df

def howMuchStorageNeed(szenarioName: str, simulationYears: list) -> float:
    availableStorageYear = list()
    with ThreadPoolExecutor() as executor:
        futures = []
        for df in range(simulationYears):
            futures.append(executor.submit(calculationMinStorage, df))
        for future in futures:
            availableStorageYear.append(future.result())
    
    return

def calculationMinStorage(df: pd.DataFrame) -> float:
    return

# def howMuchCost(szenarioList: list[dict]) -> None/np.float64:
    