import data
import gui
import graphics
import simulation
import pandas as pd

prognose = {
    'Biomasse': 1340000.0, 
    'Wasserkraft': 890000.0, 
    'Wind Offshore': 1770000.0, 
    'Wind Onshore': 1230000.0, 
    'Photovoltaik': 950000.0, 
    'Sonstige Erneuerbare': 1520000.0, 
    'Kernenergie': 1080000.0, 
    'Braunkohle': 670000.0, 
    'Steinkohle': 1450000.0, 
    'Erdgas': 880000.0, 
    'Pumpspeicher': 1910000.0, 
    'sonstige Konventionelle': 1110000.0
}

def main():
    # Read in data and save in df
    # gen21 = data.read_SMARD("Realisierte_Erzeugung_202101010000_202201010000_Viertelstunde.csv")
    # gen22 = data.read_SMARD("Realisierte_Erzeugung_202201010000_202301010000_Viertelstunde.csv")
    gen23 = data.read_SMARD("Realisierte_Erzeugung_202301010000_202401010000_Viertelstunde.csv")
    # con21 = data.read_SMARD("Realisierter_Stromverbrauch_202101010000_202201010000_Viertelstunde.csv", False)
    # con22 = data.read_SMARD("Realisierter_Stromverbrauch_202201010000_202301010000_Viertelstunde.csv", False)
    # con23 = data.read_SMARD("Realisierter_Stromverbrauch_202301010000_202401010000_Viertelstunde.csv", False)
    # generation = [gen21, gen22, gen23]
    # consumption = [con21, con22, con23]
    simulationList = list()
    
    # print(gen23)
    # print(simulation.simulation(gen23, prognose))
    
    # graphics.plotHistogramStorage(gen23, "Storage")
    
    # print(gen21)
    # graphics.plotHeatmap(gen21, "Heatmap", "Residual", "Tag", "Uhrzeit","Heatmap2021")
    # histogramPercent(gen21)
    
    print("Simulationtool")
    print("'simulation' -> simulationtool")
    while True:
        user_input = input("Write your commands (or 'quit' to exit the program): ")
        match user_input.lower():
            case "quit":
                print("Program will be terminated.")
                exit()
            case "simulation":
                print("Running the simulation...")
                simulationList = simulation.simulation(gen23)
            case "appendcsv":
                # Testen: 'pd.concat([gen23, currentSimulation.copy()], ignore_index=True)' <---> 'currentSimulation.copy()'
                # => Dann werden Spalten wie 'Total' mit ausgegeben -> Nicht gut
                # data.appendYearlyCSV(currentSimulation.copy(), "Simulation")
                for df in simulationList:
                    data.appendMinutesCSV(df, "Simulation")
            # case "help":
            # 40000000
            case _:
                print(f"{'\033[31m'}Unrecognized command: {user_input}{'\033[0m'}")
                
# def commands():
#     return "Valid commands"


def heatmaps(df):
    graphics.plotHeatmap(df, "Heatmap", "Residual", "Tag", "Uhrzeit")

def histogramPercent(df):
    vec = data.countPercentageRenewable(df)
    graphics.plotHistogramPercent(vec, "Histogram2021")
    vec = data.countPercentageRenewableExclude(df)
    print(vec)
    graphics.plotPiePercent(vec, "Pie_chart2021")

if __name__ == "__main__":
    main()


