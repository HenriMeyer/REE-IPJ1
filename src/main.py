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
    
    print(gen21)
    graphics.plotHeatmap(gen22, 'Wind Onshore', 'Monat', 'Uhrzeit', 'Heatmap % ')
    #plot_data(gen21, con21, '2021')


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


