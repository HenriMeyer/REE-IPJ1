import data
import gui
import graphics

def main():
    #df = data.read_SMARD("Realisierte_Erzeugung_202410050000_202410160000_Viertelstunde.csv")
    df = data.read_SMARD("Realisierte_Erzeugung_202301010000_202401010000_Viertelstunde.csv")
    print(df)
    graphics.plotWeekdayHeatmap(df, "Heatmap", "residual", "Tag_von", "Uhrzeit_von")

if __name__ == "__main__":
    main()


