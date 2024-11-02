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
    
    
    #print(gen21)
    #heatmaps(df)
    histogramPercent(con21)
    histogramPercent(con22)
    histogramPercent(con23)
    data.appendCSV(gen21, gen22, gen23, con21, con22, con23)

def heatmaps(df):
    graphics.plotHeatmap(df, "Heatmap", "Residual", "Tag", "Uhrzeit")

def histogramPercent(df):
    df = data.addPercentageRenewableLast(df)
    print(df)
    vec = data.countPercentageRenewableExclude(df)
    #vec = data.countPercentageRenewable(df)
    print(vec)
    graphics.plotHistogramPercent(vec)
    vec = data.countPercentageRenewable(df)
    graphics.plotHistogramPercent(vec)
    #graphics.plotPiePercent(vec)

if __name__ == "__main__":
    main()


