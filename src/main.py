import data
import gui
import graphics

def main():
    df = data.read_SMARD("Realisierte_Erzeugung_202410050000_202410160000_Viertelstunde.csv")
    print(df)
    graphics.plotWeekdayHeatmap(df)

if __name__ == "__main__":
    main()
