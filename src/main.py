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
    #histogramErzeuger(gen21, '2021')
    #histogramErzeuger(gen22, '2022')
    #histogramErzeuger(gen23, '2023')
    histogramPercent(con21, gen21, '2021')
    histogramPercent(con22, gen22, '2022')
    histogramPercent(con23, gen23, '2023')
    graphics.plotBalken(gen21, 'Alle Energieträger 2021')
    graphics.plotBalken(gen22, 'Alle Energieträger 2022')
    graphics.plotBalken(gen23, 'Alle Energieträger 2023')
    #data.appendCSV(gen21, gen22, gen23, con21, con22, con23)


def heatmaps(df):
    graphics.plotHeatmap(df, "Heatmap", "Residual", "Tag", "Uhrzeit")

def histogramPercent(df, df2, time: str):
    df = data.addPercentageRenewableLast(df, df2)
    vec = data.countPercentageRenewable(df)
    #vec = data.countPercentageRenewableExclude(df)
    graphics.plotHistogramPercent2(df, 'Histogramm Abdeckung der Viertelstunden ' +time)
    graphics.plotHistogramPercent(vec, 'Anzahl der Viertelstunden mit prozentualer Abdeckung für ' +time)
    #graphics.plotHeatmap(df, 'Anteil Erneuerbar [%]', 'Monat', 'Tag', 'Heatmap % ' + time)
    graphics.plotPieChartVer(df, df2, 'Erneuerbare vs. Konventionelle Energie Verbrauch '+time)
    #graphics.plotPiePercent(vec, "Pie_chart2021")

def histogramErzeuger(df, time: str):
    graphics.plotHistogramErzeuger(df, 'Anteil der einzelnen Erzeuger an den erneuerbaren Energien '+ time)
    graphics.plotPieChart(df, 'Erneuerbare vs. Konventionelle Energie '+ time)
    graphics.plotPieErzeugerNeu(df, 'Anteilige Erzeugung Erneuerbarer '+ time)
    graphics.plotPieErzeugerKonv(df, 'Anteilige Erzeugung Konventioneller '+ time)


if __name__ == "__main__":
    main()


