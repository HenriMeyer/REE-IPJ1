import data
import gui
import graphics

def main():
    #df = data.read_SMARD("Realisierte_Erzeugung_202410050000_202410160000_Viertelstunde.csv")
    df = data.read_SMARD("Realisierte_Erzeugung_202301010000_202401010000_Viertelstunde.csv")
    print(df)
    #heatmaps(df)
    histograms(df)


def heatmaps(df):
    graphics.plotHeatmap(df, "Heatmap", "Residual", "Tag", "Uhrzeit")

def histograms(df):
    vec = data.countPercentageRenewable(df)
    print(vec)
    graphics.plotHistogram(vec)

if __name__ == "__main__":
    main()


