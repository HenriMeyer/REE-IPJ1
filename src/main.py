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
               "Realisierte_Erzeugung_202301010000_202401010000_Viertelstunde.csv"
                ]
    useList = ["Realisierter_Stromverbrauch_201501010000_201601010000_Viertelstunde.csv",
               "Realisierter_Stromverbrauch_201601010000_201701010000_Viertelstunde.csv",
               "Realisierter_Stromverbrauch_201701010000_201801010000_Viertelstunde.csv",
               "Realisierter_Stromverbrauch_201801010000_201901010000_Viertelstunde.csv",
               "Realisierter_Stromverbrauch_201901010000_202001010000_Viertelstunde.csv",
               "Realisierter_Stromverbrauch_202001010000_202101010000_Viertelstunde.csv",
               "Realisierter_Stromverbrauch_202101010000_202201010000_Viertelstunde.csv",
               "Realisierter_Stromverbrauch_202201010000_202301010000_Viertelstunde.csv",
               "Realisierter_Stromverbrauch_202301010000_202401010000_Viertelstunde.csv"
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
            
    # List for szenarios
    szenarioDict: dict[str, list] = dict()
    
    # Menu
    print("\033[1mSimulationtool (Start: 2023)\033[0m")
    printCommands()
    while True:
        userInput = input("Write your commands (or 'quit' to exit the program): ")
        match userInput.lower():
            case "quit":
                print("Program will be terminated.")
                break
            case "szenarios":
                szenarioDict.update(simulation.scenarios(dfList, loadProfile))
            # case "szenario":
            #     simulationDict = simulation.ownScenario(dfList, loadProfile)
            #     # szenarioDict.append({"TEST": simulationDict})
            case "visualize":
                if len(szenarioDict) > 0:
                    while True:
                        for key in szenarioDict.keys():
                            print(f"- {key}")
                        userInput = input("Choose your szenario: ")
                        if userInput not in szenarioDict:
                            print("\033[31mWrong input!\033[0m")
                        else:
                            visualize({userInput: szenarioDict[userInput]})
                            break
                else:
                    print("\033[31mNo simulation has been made!\033[0m")
            case "excel":
                if len(szenarioDict) > 0:
                    while True:
                        printAll = input("Do you want all szenarios to be written in excel? (y/n) ").lower()
                        if printAll == 'y':
                            with ThreadPoolExecutor() as executor:
                                futures = []
                                for key in szenarioDict.keys():
                                    futures.append(executor.submit(data.writeExcel, {key: szenarioDict[key]}))
                                for future in futures:
                                    future.result()
                            break
                        elif printAll == 'n':
                            break
                        else:
                            print("\033[31mWrong input!\033[0m")
                    if printAll == 'n':
                        while True:
                            for key in szenarioDict.keys():
                                print(f"- {key}")
                            userInput = input("Choose your szenario: ")
                            if userInput not in szenarioDict:
                                print("\033[31mWrong input!\033[0m")
                            else:
                                data.writeExcel({userInput: szenarioDict[userInput]})
                                break
                else:
                    print("\033[31mNo simulation has been made!\033[0m")
            case "csv":
                if len(szenarioDict) > 0:
                    while True:
                        printAll = input("Do you want all szenarios to be written in csv? (y/n) ").lower()
                        if printAll == 'y':
                            with ThreadPoolExecutor() as executor:
                                futures = []
                                for key in szenarioDict.keys():
                                    futures.append(executor.submit(data.writeCSV, {key: szenarioDict[key]}))
                                for future in futures:
                                    future.result()
                            break
                        elif printAll == 'n':
                            break
                        else:
                            print("\033[31mWrong input!\033[0m")
                    if printAll == 'n':
                        while True:
                            for key in szenarioDict.keys():
                                print(f"- {key}")
                            userInput = input("Choose your szenario: ")
                            if userInput not in szenarioDict:
                                print("\033[31mWrong input!\033[0m")
                            else:
                                data.writeCSV({userInput: szenarioDict[userInput]})
                                break
                else:
                    print("\033[31mNo simulation has been made!\033[0m")
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
        {"command": "simulation", "description": "Runs a simulation using the given data."},
        {"command": "szenarios", "description": "Runs one of many scenarios."},
        {"command": "excel", "description": "Writes the simulation data to an Excel file."},
        {"command": "visualize", "description": "Visualizes the simulation results."},
        {"command": "csv", "description": "Appends data to a CSV file."},
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





























#_______________________________________________________________________________________________________________________________________________________________
#Visualizations
def visualize(simulationDict: dict[str, list]):
    key = str(next(iter(simulationDict)))
    keyStr = str(key)
    dfList = list(simulationDict[key])

    while True:
        visualizationYear = input("Year to visualize: ")
        if visualizationYear.isdigit():
            for df in dfList:
                if int(visualizationYear) == int(df['Datum von'].dt.year.iloc[0]):
                    dfv = df
            break
        else:
            print(f"\033[31m{visualizationYear} is an invalid input!\033[0m")


    dfv = data.addInformation(dfv)
    # graphics.plot_pie_conv(dfv, 'Anteilige Erzeugung Konventioneller '+ visualizationYear)
    # graphics.plotHistogramPercent(dfv, 'Histogramm Abdeckung der Viertelstunden ' + visualizationYear)
    # graphics.plot_pie_rene(dfv, 'Anteilige Erzeugung Erneuerbarer '+ visualizationYear)
    # #graphics.plotHeatmap(dfv , 'Ungenutzte Energie', 'Monat', 'Tag', 'Heatmap')
    # graphics.plot_energy_data_from_df(dfv, 'Stromverbrauch und Produktion '+ visualizationYear)
    # clearScreen()

    graphics.aggregate_and_plot(dfList, keyStr)


def plot_data(dfe, dfv, time):
    graphics.plot_pie_conv(dfe, 'Anteilige Erzeugung Konventioneller '+ time)
    graphics.plot_pie_rene(dfe, 'Anteilige Erzeugung Erneuerbarer '+ time)
    #graphics.plot_pie_usage(dfv, dfe, 'Erneuerbare vs. Konventionelle Energie Verbrauch '+ time)
    graphics.plot_pie_prod(dfe, 'Erneuerbare vs. Konventionelle Energie '+ time)
    graphics.plot_balk_rene(dfe, 'Anteil der einzelnen Erzeuger an den erneuerbaren Energien '+ time)
    graphics.plot_balk_all(dfe, 'Erzeugte Leistung der einzelnen Energieträger ' + time)
    graphics.plotHistogramPercent(dfe, 'Histogramm Abdeckung der Viertelstunden ' +time)
    #graphics.plotHeatmap(dfe, 'Anteil Erneuerbar [%]', 'Monat', 'Tag', 'Heatmap % ' + time)


def heatmaps(df):
    graphics.plotHeatmap(df, "Heatmap", "Residual", "Tag", "Uhrzeit")

def histogramPercent(df, df2, time: str):
    df = data.addPercentageRenewableLast(df, df2)
    vec = data.countPercentageRenewable(df)
    #vec = data.countPercentageRenewableExclude(df)
    graphics.plotHistogramPercent(df, 'Histogramm Abdeckung der Viertelstunden ' +time)
    graphics.plotHistogramPercent(vec, 'Anzahl der Viertelstunden mit prozentualer Abdeckung für ' +time)
    graphics.plotHeatmap(df, 'Anteil Erneuerbar [%]', 'Monat', 'Tag', 'Heatmap % ' + time)
#_______________________________________________________________________________________________________________________________________________________________


if __name__ == "__main__":
    main()