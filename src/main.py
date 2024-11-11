import data
import gui
import graphics

def main():
    # Read in data and save in df
    gen21 = data.read_SMARD("Realisierte_Erzeugung_202101010000_202201010000_Viertelstunde.csv")
    gen22 = data.read_SMARD("Realisierte_Erzeugung_202201010000_202301010000_Viertelstunde.csv")
    gen23 = data.read_SMARD("Realisierte_Erzeugung_202301010000_202401010000_Viertelstunde.csv")
    con21 = data.read_SMARD("Realisierter_Stromverbrauch_202101010000_202201010000_Viertelstunde.csv", False)
    con22 = data.read_SMARD("Realisierter_Stromverbrauch_202201010000_202301010000_Viertelstunde.csv", False)
    con23 = data.read_SMARD("Realisierter_Stromverbrauch_202301010000_202401010000_Viertelstunde.csv", False)
    generation = [gen21, gen22, gen23]
    consumption = [con21, con22, con23]
    
    graphics.plotHistogramStorage(gen23, "Storage")
    
    # print(gen21)
    # graphics.plotHeatmap(gen21, "Heatmap", "Residual", "Tag", "Uhrzeit","Heatmap2021")
    # histogramPercent(gen21)
    # data.appendCSV(generation, consumption)
    # data.pdfAnalysis(generation, consumption)


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


