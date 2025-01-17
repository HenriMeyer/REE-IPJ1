import pandas as pd
import random
import numpy as np
from concurrent.futures import ThreadPoolExecutor

START_YEAR = 2024

generation = {
    'Biomasse': 43431161,
    'Wasserkraft': 15000000,
    'Wind Offshore': 94620000,
    'Wind Onshore': 228060000,
    'Photovoltaik': 157380000,
    'Sonstige Erneuerbare': 1100000,
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
        'min' : 1600000,
        'mid' : 5500000,
        'max' : 6000000
    },
    'Verbrauch in [kWh]' : {
        'min' : 1917,
        'mid' : 3514,
        'max' : 7933
    }
}
eauto = {
    'E-Auto' : {
        'min' : 4590000,
        'mid' : 7590000,
        'max' : 10590000
    },
    'Vehicle to Grid' : {
        'no' : 0,
        'yes' : 9.46
    }
}
start = {
    'Wärmepumpe' : 1600000,
    'E-Auto' : 1590000,
    'E-LKW': 81403,
    'Sattelzug': 741,
    'Photovoltaik': 96000,
    'Wind Onshore': 61000,
    'Wind Offshore': 8500,
}
elkw = {
    'E-LKW' : {
        'min' : 105339,
        'mid' : 761243,
        'max' : 1431907
    },
    'Sattelzug' : {
        'min' : 3936,
        'mid' : 9840,
        'max' : 30504
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
        'batt_cap' : 90000,
        'batt_load' : 15000
    },
    'max' : {
        'pump_cap' : 120000,
        'pump_load' : 30000,
        'batt_cap' : 145000,
        'batt_load' : 25000
    }
    }
}
storageUsage = {
    'pump_cap' : 1,
    'pump_load' : 1,
    'batt_cap' : 1,
    'batt_load' : 1,
    'E-Auto' : 0
}
# Pro Einheit oder MW in Euro(Muss noch überarbeitet werden nur zum testen)
price = {
    'Wind Onshore' : 1600000,
    'Wind Offshore' : 3250000,
    'Photovoltaik' : 833000,
    'E-Auto' : 50000,
    'E-LKW' : 53000,
    'Sattelzug' : 200000,
    'Wärmepumpe' : 25000,
    'Pumpspeicher' : 1000000,
    'Batteriespeicher' : 400000,
}

def scenarios(dfList: list[pd.DataFrame], loadProfile: list[pd.DataFrame]) -> dict[str, list]:
    choicesscenarios = ["retention", "imbalance", "no storage", "light breeze", "confidence", "cold winter", "smard"]

    while True:
        print(f"Available scenarios:")
        for scenario in choicesscenarios:
            print(f"- {scenario}")
        print("You may also write \033[1m'all'\033[0m to write all scenarios!")
        userInput = input("Type in one of the mentioned scenarios: ").lower()
        if userInput not in choicesscenarios and userInput != "all":
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
        'Sattelzug': start['Sattelzug'],
        'Wärmepumpe': start['Wärmepumpe']
    }

    def definescenario(scenario: str):
        storageUsage['E-Auto'] = eauto['Vehicle to Grid']['no']
        match scenario:
            case "retention":
                install_values.update({
                    'Photovoltaik': photovoltaik['Installierte Leistung [MW]']['min'],
                    'Wind Onshore': windOnshore['Installierte Leistung [MW]']['min'],
                    'Wind Offshore': windOffshore['Installierte Leistung [MW]']['min'],
                    'E-Auto': eauto['E-Auto']['min'],
                    'E-LKW': elkw['E-LKW']['min'],
                    'Sattelzug': elkw['Sattelzug']['min'],
                    'Wärmepumpe': waermepumpe['Wärmepumpe']['mid']
                })
                generation['Photovoltaik'] = install_values['Photovoltaik'] * photovoltaik['Globalstrahlung [Wh/m^2]']['mid'] * 0.8
                generation['Wind Onshore'] = install_values['Wind Onshore'] * windOnshore['Volllaststunden [h]']['mid']
                generation['Wind Offshore'] = install_values['Wind Offshore'] * windOffshore['Volllaststunden [h]']['mid']
                generation['Verbrauch'] = consumption['mid']
                generation['E-Auto'] = install_values['E-Auto']
                generation['E-LKW'] = install_values['E-LKW']
                generation['Sattelzug'] = install_values['Sattelzug']
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
                    'Sattelzug': elkw['Sattelzug']['max'],
                    'Wärmepumpe': waermepumpe['Wärmepumpe']['max']
                })
                generation['Photovoltaik'] = install_values['Photovoltaik'] * photovoltaik['Globalstrahlung [Wh/m^2]']['mid'] * 0.8
                generation['Wind Onshore'] = install_values['Wind Onshore'] * windOnshore['Volllaststunden [h]']['mid']
                generation['Wind Offshore'] = install_values['Wind Offshore'] * windOffshore['Volllaststunden [h]']['mid']
                generation['Verbrauch'] = consumption['max']
                generation['E-Auto'] = install_values['E-Auto']
                generation['E-LKW'] = install_values['E-LKW']
                generation['Sattelzug'] = install_values['Sattelzug']
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
                    'Sattelzug': elkw['Sattelzug']['mid'],
                    'Wärmepumpe': waermepumpe['Wärmepumpe']['max']
                })
                generation['Photovoltaik'] = install_values['Photovoltaik'] * photovoltaik['Globalstrahlung [Wh/m^2]']['mid'] * 0.8
                generation['Wind Onshore'] = install_values['Wind Onshore'] * windOnshore['Volllaststunden [h]']['mid']
                generation['Wind Offshore'] = install_values['Wind Offshore'] * windOffshore['Volllaststunden [h]']['mid']
                generation['Verbrauch'] = consumption['mid']
                generation['E-Auto'] = install_values['E-Auto']
                generation['E-LKW'] = install_values['E-LKW']
                generation['Sattelzug'] = install_values['Sattelzug']
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
                    'Sattelzug': elkw['Sattelzug']['mid'],
                    'Wärmepumpe': waermepumpe['Wärmepumpe']['mid']
                })
                generation['Photovoltaik'] = install_values['Photovoltaik'] * photovoltaik['Globalstrahlung [Wh/m^2]']['min'] * 0.8
                generation['Wind Onshore'] = install_values['Wind Onshore'] * windOnshore['Volllaststunden [h]']['min']
                generation['Wind Offshore'] = install_values['Wind Offshore'] * windOffshore['Volllaststunden [h]']['min']
                generation['Verbrauch'] = consumption['mid']
                generation['E-Auto'] = install_values['E-Auto']
                generation['E-LKW'] = install_values['E-LKW']
                generation['Sattelzug'] = install_values['Sattelzug']
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
                    'Sattelzug': elkw['Sattelzug']['max'],
                    'Wärmepumpe': waermepumpe['Wärmepumpe']['max']
                })
                generation['Photovoltaik'] = install_values['Photovoltaik'] * photovoltaik['Globalstrahlung [Wh/m^2]']['max'] * 0.8
                generation['Wind Onshore'] = install_values['Wind Onshore'] * windOnshore['Volllaststunden [h]']['max']
                generation['Wind Offshore'] = install_values['Wind Offshore'] * windOffshore['Volllaststunden [h]']['max']
                generation['Verbrauch'] = consumption['min']
                generation['E-Auto'] = install_values['E-Auto']
                generation['E-LKW'] = install_values['E-LKW']
                generation['Sattelzug'] = install_values['Sattelzug']
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
                    'Sattelzug': elkw['Sattelzug']['max'],
                    'Wärmepumpe': waermepumpe['Wärmepumpe']['max']
                })
                generation['Photovoltaik'] = install_values['Photovoltaik'] * photovoltaik['Globalstrahlung [Wh/m^2]']['mid'] * 0.8
                generation['Wind Onshore'] = install_values['Wind Onshore'] * windOnshore['Volllaststunden [h]']['mid']
                generation['Wind Offshore'] = install_values['Wind Offshore'] * windOffshore['Volllaststunden [h]']['mid']
                generation['Verbrauch'] = consumption['mid']
                generation['E-Auto'] = install_values['E-Auto']
                generation['E-LKW'] = install_values['E-LKW']
                generation['Sattelzug'] = install_values['Sattelzug']
                generation['Wärmepumpe'] = install_values['Wärmepumpe'] * waermepumpe['Verbrauch in [kWh]']['min']
                for storageItem in ["pump_cap", "pump_load", "batt_cap", "batt_load"]:
                    storageUsage[storageItem] = storage['Speicher']['max'][storageItem]
            case "smard":
                install_values.update({
                    'Photovoltaik': 107191,
                    'Wind Onshore': 77061,
                    'Wind Offshore': 14260,
                    'E-Auto': start['E-Auto'],
                    'E-LKW': start['E-LKW'],
                    'Sattelzug': start['Sattelzug'],
                    'Wärmepumpe': start['Wärmepumpe']
                })
                startSMARD = int(dfList[0]['Datum von'].dt.year.iloc[0])
                for column in dfList[0].columns:
                    if column in ['Datum von', 'Datum bis']:
                        continue
                    buffer = list()
                    for i in range(len(dfList) - 1):
                        buffer.append(dfList[i + 1][column].sum() - dfList[i][column].sum())
                    generation[column] = dfList[0][column].sum() + sum(buffer) / len(buffer) * (START_YEAR - startSMARD)
                generation['Photovoltaik'] = install_values['Photovoltaik'] * photovoltaik['Globalstrahlung [Wh/m^2]']['mid'] * 0.8
                generation['Wind Onshore'] = install_values['Wind Onshore'] * windOnshore['Volllaststunden [h]']['mid']
                generation['Wind Offshore'] = install_values['Wind Offshore'] * windOffshore['Volllaststunden [h]']['mid']
                generation['Verbrauch'] = consumption['mid']
                generation['E-Auto'] = install_values['E-Auto']
                generation['E-LKW'] = install_values['E-LKW']
                generation['Sattelzug'] = install_values['Sattelzug']
                generation['Wärmepumpe'] = install_values['Wärmepumpe'] * waermepumpe['Verbrauch in [kWh]']['min']
                for storageItem in ["pump_cap", "pump_load", "batt_cap", "batt_load"]:
                    storageUsage[storageItem] = storage['Speicher']['mid'][storageItem]
                    

    if userInput == "all":
        results = []
        scenarioDict = dict()

        for scenario in choicesscenarios:
            definescenario(scenario)
            result = simulation(dfList, 2030, loadProfile, scenario, install_values)
            results.append(result)

        for dictonary in results:
            scenarioDict.update(dictonary)

        for key, dfList in scenarioDict.items():
            howMuchStorageNeed(str(key), dfList[-1])

        return scenarioDict

    else:
        definescenario(userInput)
        scenarioDict = simulation(dfList, 2030, loadProfile, userInput, install_values)
        for key, dfList in scenarioDict.items():
            howMuchStorageNeed(str(key), dfList[-1])
        return scenarioDict



def ownScenario(dfList: list[pd.DataFrame], loadProfile: list[pd.DataFrame]) -> dict[str, list]:    
    def casesScenario() -> None:
        # Photovoltaik
        while True:
            userInput = input("Installed Power for photovoltaik: ").lower()
            if userInput in ["min", "mid", "max"]:
                install_values.update({'Photovoltaik': photovoltaik['Installierte Leistung [MW]'][userInput]})
                break
            else:
                print("\033[31mWrong input!\033[0m")
        while True:
            userInput = input("Global solar radiation: ").lower()
            if userInput in ["min", "mid", "max"]:
                generation['Photovoltaik'] = install_values['Photovoltaik'] * photovoltaik['Globalstrahlung [Wh/m^2]'][userInput] * 0.8
                break
            else:
                print("\033[31mWrong input!\033[0m")
        
        # Wind
        while True:
            userInput = input("Installed Power for wind onshore: ").lower()
            if userInput in ["min", "mid", "max"]:
                install_values.update({'Wind Onshore': windOnshore['Installierte Leistung [MW]'][userInput]})
                break
            else:
                print("\033[31mWrong input!\033[0m")
        while True:
            userInput = input("Installed Power for wind offshore: ").lower()
            if userInput in ["min", "mid", "max"]:
                install_values.update({'Wind Offshore': windOffshore['Installierte Leistung [MW]'][userInput]})
                break
            else:
                print("\033[31mWrong input!\033[0m")
        while True:
            userInput = input("Full-load hours for wind: ").lower()
            if userInput in ["min", "mid", "max"]:
                generation['Wind Onshore'] = install_values['Wind Onshore'] * windOnshore['Volllaststunden [h]'][userInput]
                generation['Wind Offshore'] = install_values['Wind Offshore'] * windOffshore['Volllaststunden [h]'][userInput]
                break
            else:
                print("\033[31mWrong input!\033[0m")
        
        # Consumption
        while True:
            userInput = input("Consumption: ").lower()
            if userInput in ["min", "mid", "max"]:
                generation['Verbrauch'] = consumption[userInput]
                break
            else:
                print("\033[31mWrong input!\033[0m")
        
        # Electro
        while True:
            userInput = input("Electric cars: ").lower()
            if userInput in ["min", "mid", "max"]:
                install_values.update({'E-Auto': eauto['E-Auto'][userInput]})
                generation['E-Auto'] = install_values['E-Auto']
                break
            else:
                print("\033[31mWrong input!\033[0m")
        
        while True:
            userInput = input("Electric truck: ").lower()
            if userInput in ["min", "mid", "max"]:
                install_values.update({'E-LKW': elkw['E-LKW'][userInput]})
                generation['E-LKW'] = install_values['E-LKW']
                break
            else:
                print("\033[31mWrong input!\033[0m")
        
        while True:
            userInput = input("Sattelzug: ").lower()
            if userInput in ["min", "mid", "max"]:
                install_values.update({'Sattelzug': elkw['Sattelzug'][userInput]})
                generation['Sattelzug'] = install_values['Sattelzug']
                break
            else:
                print("\033[31mWrong input!\033[0m")
        
        # Heat pump
        while True:
            userInput = input("Heat pumps: ").lower()
            if userInput in ["min", "mid", "max"]:
                install_values.update({'Wärmepumpe': waermepumpe['Wärmepumpe'][userInput]})
                break
            else:
                print("\033[31mWrong input!\033[0m")
        while True:
            userInput = input("Heat pumps consumption: ").lower()
            if userInput in ["min", "mid", "max"]:
                generation['Wärmepumpe'] = install_values['Wärmepumpe'] * waermepumpe['Verbrauch in [kWh]'][userInput]
                break
            else:
                print("\033[31mWrong input!\033[0m")
        
        # Storage
        while True:
            userInput = input("Storage: ").lower()
            if userInput in ["min", "mid", "max"]:
                for storageItem in ["pump_cap", "pump_load", "batt_cap", "batt_load"]:
                    storageUsage[storageItem] = storage['Speicher'][userInput][storageItem]
                break
            else:
                print("\033[31mWrong input!\033[0m")
        # Vehicle to Grid
        while True:
            userInput = input("Vehicle to Grid (yes/no): ").lower()
            if userInput in ["yes", "no"]:
                storageUsage['E-Auto'] = eauto['Vehicle to Grid'][userInput]
                break
            else:
                print("\033[31mWrong input!\033[0m")
    
    def valuesScenario() -> None:
        # Photovoltaik
        while True:
            userInput = input("Installed Power for photovoltaik [MW]: ")
            if userInput.replace('.', '', 1).isdigit() and float(userInput) > 0:
                install_values.update({'Photovoltaik': float(userInput)})
                break
            else:
                print("\033[31mPlease enter a valid positive number!\033[0m")

        while True:
            userInput = input("Global solar radiation [Wh/m^2]: ")
            if userInput.replace('.', '', 1).isdigit() and float(userInput) > 0:
                generation['Photovoltaik'] = install_values['Photovoltaik'] * float(userInput) * 0.8
                break
            else:
                print("\033[31mPlease enter a valid positive number!\033[0m")

        # Wind
        while True:
            userInput = input("Installed Power for wind onshore [MW]: ")
            if userInput.replace('.', '', 1).isdigit() and float(userInput) > 0:
                install_values.update({'Wind Onshore': float(userInput)})
                break
            else:
                print("\033[31mPlease enter a valid positive number!\033[0m")

        while True:
            userInput = input("Installed Power for wind offshore [MW]: ")
            if userInput.replace('.', '', 1).isdigit() and float(userInput) > 0:
                install_values.update({'Wind Offshore': float(userInput)})
                break
            else:
                print("\033[31mPlease enter a valid positive number!\033[0m")

        while True:
            userInput = input("Full-load hours for wind [h]: ")
            if userInput.replace('.', '', 1).isdigit() and float(userInput) > 0:
                generation['Wind Onshore'] = install_values['Wind Onshore'] * float(userInput)
                generation['Wind Offshore'] = install_values['Wind Offshore'] * float(userInput)
                break
            else:
                print("\033[31mPlease enter a valid positive number!\033[0m")

        # Consumption
        while True:
            userInput = input("Consumption [kWh]: ")
            if userInput.replace('.', '', 1).isdigit() and float(userInput) > 0:
                generation['Verbrauch'] = float(userInput)
                break
            else:
                print("\033[31mPlease enter a valid positive number!\033[0m")

        # Electro
        while True:
            userInput = input("Electric cars units: ")
            if userInput.replace('.', '', 1).isdigit() and float(userInput) > 0:
                install_values.update({'E-Auto': float(userInput)})
                generation['E-Auto'] = install_values['E-Auto']
                break
            else:
                print("\033[31mPlease enter a valid positive number!\033[0m")
        
        while True:
            userInput = input("Vehicle to Grid (yes/no): ").lower()
            if userInput in ["yes", "no"]:
                storageUsage['E-Auto'] = eauto['Vehicle to Grid'][userInput]
                break
            else:
                print("\033[31mWrong input!\033[0m")

        while True:
            userInput = input("Electric truck units: ")
            if userInput.replace('.', '', 1).isdigit() and float(userInput) > 0:
                install_values.update({'E-LKW': float(userInput)})
                generation['E-LKW'] = install_values['E-LKW']
                break
            else:
                print("\033[31mPlease enter a valid positive number!\033[0m")

        while True:
            userInput = input("Sattelzug truck units: ")
            if userInput.replace('.', '', 1).isdigit() and float(userInput) > 0:
                install_values.update({'Sattelzug': float(userInput)})
                generation['Sattelzug'] = install_values['Sattelzug']
                break
            else:
                print("\033[31mPlease enter a valid positive number!\033[0m")
        # Heat pump
        while True:
            userInput = input("Heat pumps [kWh]: ")
            if userInput.replace('.', '', 1).isdigit() and float(userInput) > 0:
                install_values.update({'Wärmepumpe': float(userInput)})
                break
            else:
                print("\033[31mPlease enter a valid positive number!\033[0m")

        while True:
            userInput = input("Heat pumps consumption [kWh]: ")
            if userInput.replace('.', '', 1).isdigit() and float(userInput) > 0:
                generation['Wärmepumpe'] = install_values['Wärmepumpe'] * float(userInput)
                break
            else:
                print("\033[31mPlease enter a valid positive number!\033[0m")

        # Storage
        while True:
            userInput = input("Storage pump capacity [kWh]: ")
            if userInput.replace('.', '', 1).isdigit() and float(userInput) > 0:
                storageUsage["pump_cap"] = float(userInput)
                break
            else:
                print("\033[31mPlease enter a valid positive number!\033[0m")

        while True:
            userInput = input("Storage pump load [kWh]: ")
            if userInput.replace('.', '', 1).isdigit() and float(userInput) > 0:
                storageUsage["pump_load"] = float(userInput)
                break
            else:
                print("\033[31mPlease enter a valid positive number!\033[0m")

        while True:
            userInput = input("Storage battery capacity [kWh]: ")
            if userInput.replace('.', '', 1).isdigit() and float(userInput) > 0:
                storageUsage["batt_cap"] = float(userInput)
                break
            else:
                print("\033[31mPlease enter a valid positive number!\033[0m")

        while True:
            userInput = input("Storage battery load [kWh]: ")
            if userInput.replace('.', '', 1).isdigit() and float(userInput) > 0:
                storageUsage["batt_load"] = float(userInput)
                break
            else:
                print("\033[31mPlease enter a valid positive number!\033[0m")


    install_values = {
        'Photovoltaik': start['Photovoltaik'],
        'Wind Onshore': start['Wind Onshore'],
        'Wind Offshore': start['Wind Offshore'],
        'E-Auto': start['E-Auto'],
        'E-LKW': start['E-LKW'],
        'Sattelzug': start['Sattelzug'],
        'Wärmepumpe': start['Wärmepumpe']
    }
    while True:
        print("Do you want to use own values or defined cases ('min', 'mid' & 'max')?")
        userInput = input("'values'/'cases'\nInput: ").lower()
        if userInput == "values":
            valuesScenario()
            break
        elif userInput == "cases":
            casesScenario()
            break
        else:
            print("\033[31mWrong input!\033[0m")

    # Name of scenario
    while True:
        userInput = input("Name of scenario: ").lower()
        confirm = input("Confirm (y/n): ").lower()
        if confirm == 'y':
            break
        elif confirm == 'n':
            continue
        else:
            print("\033[31mWrong input!\033[0m")

    scenarioDict = simulation(dfList, 2030, loadProfile, userInput, install_values)
    for key, dfList in scenarioDict.items():
        howMuchStorageNeed(str(key), dfList[-1])
    return scenarioDict
    
    

def simulation(dfOriginalList: list[pd.DataFrame], generationYear: int, loadProfile: list[pd.DataFrame], namescenario: str, install_values: list) -> dict[str, list]:
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
            futures.append(executor.submit(storage_sim, df, int(df['Datum von'].dt.year.iloc[0]), generationYear, install_values))
        for future in futures:
            dfList.append(future.result())
    dfDict = dict()
    dfDict[namescenario] = insertionSort(dfList)
    
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
            if column == 'E-LKW':
                dfCurrent[column] = round((loadProfile[column]*((generation[column]-start[column])/(int(generationYear) - START_YEAR) * (currentYear - START_YEAR) + start[column]))
                                          +(loadProfile['Sattelzug']*((generation['Sattelzug']-start['Sattelzug'])/(int(generationYear) - START_YEAR) * (currentYear - START_YEAR) + start['Sattelzug'])),2)
            if column in ['E-Auto', 'E-LKW', 'Wärmepumpe']:
                dfCurrent[column] = round((loadProfile[column]*((generation[column]-start[column])/(int(generationYear) - START_YEAR) * (currentYear - START_YEAR) + start[column])),2)
            else:
                dfCurrent[column] = round(dfOriginal[column] * (((generation[column] / dfOriginal[column].sum() - 1) / (int(generationYear) - START_YEAR)) * (currentYear - START_YEAR) + 1), 2)
        else:
            print(column + " wasn't simulated.")

    
    dfCurrent['Price'] = 0
    dfCurrent.at[0, 'Price'] = int(sum((install_values[tech] - start[tech]) / (generationYear - START_YEAR) * (currentYear - START_YEAR) * price[tech] for tech in ['Wind Onshore', 'Wind Offshore', 'Photovoltaik']))

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


def storage_sim(df: pd.DataFrame, currentYear, generationYear, install_values: list) -> pd.DataFrame:
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
    pump_load = round((storageUsage['pump_load'] - storage['Speicher']['min']['pump_load']/(int(generationYear) - START_YEAR) * (currentYear - START_YEAR) + storage['Speicher']['min']['pump_load'])/4,2)
    pump_unload = pump_load

    #Möglicher E-AutoSpeicher
    speicher_eauto = round(((install_values['E-Auto'] - start['E-Auto']) / (generationYear - START_YEAR) * (currentYear - START_YEAR) + start['E-Auto'])* storageUsage['E-Auto'] /1e3,2)
    #Batteriespeicher-Parameter
    batt_cap = round((storageUsage['batt_cap'] - storage['Speicher']['min']['batt_cap']/(int(generationYear) - START_YEAR) * (currentYear - START_YEAR) + storage['Speicher']['min']['batt_cap']),2) + speicher_eauto
    batt_eff = 0.95
    batt_stor = 0.0
    batt_load = round((storageUsage['batt_load'] - storage['Speicher']['min']['batt_load']/(int(generationYear) - START_YEAR) * (currentYear - START_YEAR) + storage['Speicher']['min']['batt_load'])/4,2)
    batt_unload = pump_load

    df.at[0, 'Price'] += round((storageUsage['pump_cap'] - storage['Speicher']['min']['pump_cap'])/(int(generationYear) - START_YEAR) * (currentYear - START_YEAR),2)* price['Pumpspeicher']
    df.at[0, 'Price'] += round((storageUsage['batt_cap'] - storage['Speicher']['min']['batt_cap'])/(int(generationYear) - START_YEAR) * (currentYear - START_YEAR),2)* price['Batteriespeicher']

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
    df['Speicher'] = df[['Batteriespeicher Produktion', 'Pumpspeicher Produktion']].sum(axis=1)
    df['Erneuerbare'] = df[['Biomasse', 'Wasserkraft', 'Wind Offshore', 'Wind Onshore', 'Photovoltaik', 'Sonstige Erneuerbare']].sum(axis=1)
    df['Regelbare Kraftwerke'] = np.minimum(df['Konventionell'], 60000/4)
    df['Lücke'] = np.maximum(df['Konventionell'] - df['Regelbare Kraftwerke'], 0)
    
    df['Anteil Erneuerbar [%]'] = (df.loc[:,['Biomasse','Wasserkraft','Wind Offshore','Wind Onshore','Photovoltaik','Sonstige Erneuerbare','Pumpspeicher Produktion',
        'Batteriespeicher Produktion']].sum(axis=1)/df['Verbrauch']*100)
    
    df['Anteil Erneuerbar [%] ohne Speicher'] = (df.loc[:,['Biomasse','Wasserkraft','Wind Offshore','Wind Onshore','Photovoltaik','Sonstige Erneuerbare']].sum(axis=1)/df['Verbrauch']*100)
    
    columns_to_round = [
        'Pumpspeicher', 'Batteriespeicher',
        'Pumpspeicher Produktion', 'Batteriespeicher Produktion',
        'Überschuss', 'Ungenutzte Energie', 'Konventionell', 'Regelbare Kraftwerke', 'Lücke', 'Anteil Erneuerbar [%]', 
        'Anteil Erneuerbar [%] ohne Speicher', 'Speicher', 'Erneuerbare'
    ]
    df[columns_to_round] = df[columns_to_round].round(2)
    
    new_order = [
        'Datum von', 'Datum bis',
        'Biomasse', 'Wasserkraft', 'Wind Offshore', 'Wind Onshore',
        'Photovoltaik', 'Sonstige Erneuerbare', 'Pumpspeicher Produktion',
        'Batteriespeicher Produktion',
        'Sonstige Konventionelle','Wärmepumpe','E-Auto', 'E-LKW', 'Verbrauch',
        'Batteriespeicher', 'Pumpspeicher', 'Überschuss', 'Ungenutzte Energie',
        'Konventionell', 'Regelbare Kraftwerke', 'Lücke', 'Speicher', 'Erneuerbare',
        'Anteil Erneuerbar [%]', 'Anteil Erneuerbar [%] ohne Speicher', 'Price'
    ]
    df = df[new_order]
    
    return df

def howMuchStorageNeed(scenarioName: str, df2030: pd.DataFrame) -> None:

    consumption = df2030["Verbrauch"].sum()
    needStorage = round(df2030['Konventionell'].sum() - (consumption - consumption * 0.8) , 2)

    if needStorage <= 0:
        print(scenarioName + " wouldn't need any further storage.")
        return
    else:
        
        storageList = calculationStoragePossible(df2030)
        if len(storageList) == 0:
            print(scenarioName + " doesn't have renewable surplus.")
            return
        
        storageAvg = round(sum(storageList) / len(storageList), 2) if storageList else 0
        needStorageAvg = round(needStorage / len(storageList), 2)
        
        if max(storageList) / len(storageList) < needStorageAvg:
            print(scenarioName + " doesn't have the capacity to become 80% renewable.")
            return
        elif storageAvg >= needStorageAvg:
            print(scenarioName + " would need " + str(needStorageAvg) + " MWh more storage.")
            return
        else:
            print(scenarioName + " would need between " + str(storageAvg) + " - " + str(max(storageList)) + " MWh more storage... inefficient")
            return

def calculationStoragePossible(df: pd.DataFrame) -> list:
    buffer: float = 0
    counting = False
    appendBuffer = False
    values = list()
    for idx in df.index:
        value = df.loc[idx, "Ungenutzte Energie"]
        if value > 0:
            buffer += value
            counting = True
        if value == 0:
            appendBuffer = True
        if counting == True and appendBuffer == True:
            values.append(buffer)
            buffer = 0
            appendBuffer = False
            counting = False
            
    return values.copy()
