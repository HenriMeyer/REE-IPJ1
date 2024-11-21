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
    simulationList = list()
    # generation = [gen21, gen22, gen23]
    # consumption = [con21, con22, con23]
    # graphics.plotHeatmap(gen22, 'Wind Onshore', 'Monat', 'Uhrzeit', 'Heatmap % ')
    
    print("Simulationtool")
    print("'simulation' -> simulationtool")
    while True:
        user_input = input("Write your commands (or 'quit' to exit the program): ")
        # print(commands) ==> print commands
        # 'System.clear()' ==> something like that to clear cmd/powershell
        match user_input.lower():
            case "quit":
                print("Program will be terminated.")
                exit()
            case "simulation":
                print("Running the simulation...")
                simulationList = simulation.simulation(gen23)
                # 40000000 ==> standardinput strg + c
            case "appendcsv":
                    continue
                    # code follows
            case "writeexcel":
                print("Writing data to excel...")
                data.writeExcel(simulationList, "Simulation")
            case "help":
                continue
                # code follows
            case _:
                print(f"\033[31mUnrecognized command: {user_input}\033[0m")

def plot_data(dfe, dfv, time):
    graphics.plot_pie_conv(dfe, 'Anteilige Erzeugung Konventioneller '+ time)
    graphics.plot_pie_rene(dfe, 'Anteilige Erzeugung Erneuerbarer '+ time)
    graphics.plot_pie_usage(dfv, dfe, 'Erneuerbare vs. Konventionelle Energie Verbrauch '+ time)
    graphics.plot_pie_prod(dfe, 'Erneuerbare vs. Konventionelle Energie '+ time)
    graphics.plot_balk_rene(dfe, 'Anteil der einzelnen Erzeuger an den erneuerbaren Energien '+ time)
    graphics.plot_balk_all(dfe, 'Erzeugte Leistung der einzelnen Energieträger ' + time)
    graphics.plotHistogramPercent(dfe, 'Histogramm Abdeckung der Viertelstunden ' +time)
    graphics.plotHeatmap(dfe, 'Anteil Erneuerbar [%]', 'Monat', 'Tag', 'Heatmap % ' + time)


def heatmaps(df):
    graphics.plotHeatmap(df, "Heatmap", "Residual", "Tag", "Uhrzeit")

def histogramPercent(df, df2, time: str):
    df = data.addPercentageRenewableLast(df, df2)
    vec = data.countPercentageRenewable(df)
    #vec = data.countPercentageRenewableExclude(df)
    graphics.plotHistogramPercent(df, 'Histogramm Abdeckung der Viertelstunden ' +time)
    graphics.plotHistogramPercent(vec, 'Anzahl der Viertelstunden mit prozentualer Abdeckung für ' +time)
    graphics.plotHeatmap(df, 'Anteil Erneuerbar [%]', 'Monat', 'Tag', 'Heatmap % ' + time)


if __name__ == "__main__":
    main()


