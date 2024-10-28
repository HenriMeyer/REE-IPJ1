import data
import gui
import graphics

def main():
    #df = data.read_SMARD("Realisierte_Erzeugung_202410050000_202410160000_Viertelstunde.csv")
    df = data.read_SMARD("Realisierte_Erzeugung_202301010000_202401010000_Viertelstunde.csv")
    print(df)
    #heatmaps(df)
    histogramPercent(df)


def heatmaps(df):
    graphics.plotHeatmap(df, "Heatmap", "Residual", "Tag", "Uhrzeit")

def histogramPercent(df):
    vec = data.countPercentageRenewable(df)
    graphics.plotHistogramPercent(vec)
    vec = data.countPercentageRenewableExclude(df)
    print(vec)
    graphics.plotPiePercent(vec)

if __name__ == "__main__":
    main()


