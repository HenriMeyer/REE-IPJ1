import data
import graphics
import simulation
import pandas as pd
import os
from concurrent.futures import ThreadPoolExecutor


def main():
    # Clear screen
    clearScreen()
    # Filenamelists for energyuseage and energyconsumption
    genList = ["Realisierte_Erzeugung_201501010000_201601010000_Viertelstunde.csv",
               "Realisierte_Erzeugung_201601010000_201701010000_Viertelstunde.csv",
               "Realisierte_Erzeugung_201701010000_201801010000_Viertelstunde.csv",
               "Realisierte_Erzeugung_201801010000_201901010000_Viertelstunde.csv",
               "Realisierte_Erzeugung_201901010000_202001010000_Viertelstunde.csv",
               "Realisierte_Erzeugung_202001010000_202101010000_Viertelstunde.csv",
               "Realisierte_Erzeugung_202101010000_202201010000_Viertelstunde.csv",
               "Realisierte_Erzeugung_202201010000_202301010000_Viertelstunde.csv",
               "Realisierte_Erzeugung_202301010000_202401010000_Viertelstunde.csv",
               "Realisierte_Erzeugung_202401010000_202501010000_Viertelstunde.csv"
                ]
    useList = ["Realisierter_Stromverbrauch_201501010000_201601010000_Viertelstunde.csv",
               "Realisierter_Stromverbrauch_201601010000_201701010000_Viertelstunde.csv",
               "Realisierter_Stromverbrauch_201701010000_201801010000_Viertelstunde.csv",
               "Realisierter_Stromverbrauch_201801010000_201901010000_Viertelstunde.csv",
               "Realisierter_Stromverbrauch_201901010000_202001010000_Viertelstunde.csv",
               "Realisierter_Stromverbrauch_202001010000_202101010000_Viertelstunde.csv",
               "Realisierter_Stromverbrauch_202101010000_202201010000_Viertelstunde.csv",
               "Realisierter_Stromverbrauch_202201010000_202301010000_Viertelstunde.csv",
               "Realisierter_Stromverbrauch_202301010000_202401010000_Viertelstunde.csv",
               "Realisierter_Stromverbrauch_202401010000_202501010000_Viertelstunde.csv"
                ]
    
    # Check if lists have the same lengths
    try:
        if len(genList) != len(useList):
            raise ValueError("Sample lists don't have the same length.")
    except ValueError as e:
        print(f"Error: {e}")
    
    loadProfile = data.readLoadProfile()

    # Read file parallel
    dfList = list()
    with ThreadPoolExecutor() as executor:
        futures = []
        for i in range(len(genList)):
            futures.append(executor.submit(data.readSMARD, genList[i], useList[i]))
        for future in futures:
            dfList.append(future.result())
            
    # List for scenarios
    scenarioDict: dict[str, list] = dict()
    
    # Menu
    print("\033[1mSimulationtool (Start: 2024)\033[0m")
    printCommands()
    while True:
        userInput = input("Write your commands (or 'quit' to exit the program): ")
        match userInput.lower():
            case "quit":
                print("Program will be terminated.")
                break
            case "scenarios":
                scenarioDict.update(simulation.scenarios(dfList, loadProfile))
            case "own":
                scenarioDict.update(simulation.ownScenario(dfList, loadProfile))
            case "visualize":
                if len(scenarioDict) > 0:
                    if len(scenarioDict) > 1:
                        while True:
                            for key in scenarioDict.keys():
                                print(f"- {key}")
                            userInput = input("Choose your scenario (or \033[1m'all'\033[0m for all scenarios): ")
                            if userInput == 'all':
                                graphics.visualize_multiple(scenarioDict)
                                break
                            elif userInput not in scenarioDict:
                                print("\033[31mWrong input!\033[0m")
                            else:
                                graphics.visualize({userInput: scenarioDict[userInput]})
                                break
                    elif scenarioDict:
                        key = next(iter(scenarioDict))
                        graphics.visualize({key: scenarioDict[key]})
                    else:
                        print("\033[31mNo simulation has been made!\033[0m")
                else:
                    print("\033[31mNo simulation has been made!\033[0m")
            case "excel":
                if len(scenarioDict) > 0:
                    if len(scenarioDict) > 1:
                        while True:
                            for key in scenarioDict.keys():
                                print(f"- {key}")
                            userInput = input("Choose your scenario (or \033[1m'all'\033[0m for all scenarios): ")
                            if userInput == 'all':
                                with ThreadPoolExecutor() as executor:
                                    futures = []
                                    for key in scenarioDict.keys():
                                        futures.append(executor.submit(data.writeExcel, {key: scenarioDict[key]}))
                                    for future in futures:
                                        future.result()
                                break
                            elif userInput not in scenarioDict:
                                print("\033[31mWrong input!\033[0m")
                            else:
                                data.writeExcel({userInput: scenarioDict[userInput]})
                                break
                    elif scenarioDict:
                        key = next(iter(scenarioDict))
                        data.writeExcel({key: scenarioDict[key]})
                    else:
                        print("\033[31mNo simulation has been made!\033[0m")
                else:
                    print("\033[31mNo simulation has been made!\033[0m")

            case "csv":
                if len(scenarioDict) > 0:
                    if len(scenarioDict) > 1:
                        while True:
                            for key in scenarioDict.keys():
                                print(f"- {key}")
                            userInput = input("Choose your scenario (or \033[1m'all'\033[0m for all scenarios): ")
                            if userInput == 'all':
                                with ThreadPoolExecutor() as executor:
                                    futures = []
                                    for key in scenarioDict.keys():
                                        futures.append(executor.submit(data.writeCSV, {key: scenarioDict[key]}))
                                    for future in futures:
                                        future.result()
                                break
                            elif userInput not in scenarioDict:
                                print("\033[31mWrong input!\033[0m")
                            else:
                                data.writeCSV({userInput: scenarioDict[userInput]})
                                break
                    elif scenarioDict:
                        key = next(iter(scenarioDict))
                        data.writeCSV({key: scenarioDict[key]})
                    else:
                        print("\033[31mNo simulation has been made!\033[0m")
                else:
                    print("\033[31mNo simulation has been made!\033[0m")
            case "delete":
                if len(scenarioDict) > 0:
                    while True:
                        for key in scenarioDict.keys():
                                print(f"- {key}")
                        userInput = input("Choose your scenario (or \033[1m'all'\033[0m for all scenarios), if you want to abort type '-1': ").lower()
                        if userInput == 'all':
                            while True:
                                confirm = input("Are you sure (y/n)? ").lower()
                                if confirm == "y":
                                    scenarioDict = {}
                                    print("All simulations have been deleted!")
                                    break
                                elif confirm == "n":
                                    break
                                else:
                                    print("\033[31mWrong input!\033[0m")
                            break
                        elif userInput == '-1':
                            print("Abort: 'delete'")
                            break
                        elif userInput in scenarioDict:
                            del scenarioDict[userInput]
                            print(userInput + " has been deleted!")
                            break
                        else:
                            print("\033[31mWrong input!\033[0m")
                else:
                    print("\033[31mNo simulation has been made!\033[0m")
            case "owndelete":
                scenarioDict.update(simulation.ownScenario(dfList, loadProfile))
                lastKey = next(reversed(scenarioDict))
                lastDict = scenarioDict[lastKey]
                if (round(lastDict[-1]["Erneuerbare"].sum() / lastDict[-1]["Verbrauch"].sum(), 2)) < 0.8:
                    del scenarioDict[lastKey]
                # elif preis > 1€/kWh
                    # del scenarioDict[lastKey]
            case "help":
                print("Available commands:")
                printCommands()
            case "clear":
                clearScreen()
                print("\033[1mSimulationtool (Start: 2023)\033[0m")
                printCommands()
            case _:
                print(f"\033[31mUnrecognized command: {userInput}\033[0m")

def printCommands() -> None:
    commands = [
        {"command": "quit", "description": "Terminates the program."},
        {"command": "own", "description": "Create an own scenario."},
        {"command": "scenarios", "description": "Runs one of many scenarios."},
        {"command": "excel", "description": "Writes the simulation data to an Excel file."},
        {"command": "visualize", "description": "Visualizes the simulation results."},
        {"command": "csv", "description": "Appends data to a CSV file."},
        {"command": "delete", "description": "Delete one or all simulations."},
        {"command": "clear", "description": "Clear the screen."},
        {"command": "help", "description": "Shows this list of commands."}
    ]
    
    for cmd in commands:
        print(f"- {cmd['command']}: {cmd['description']}")

def clearScreen() -> None:
    if os.name == 'nt':  # Windows (cmd oder PowerShell)
        os.system('cls')
    else:  # Unix/Linux/MacOS
        os.system('clear')


if __name__ == "__main__":
    main()