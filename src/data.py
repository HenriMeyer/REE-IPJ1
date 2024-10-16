import pandas as pd

def get_data(filename):
    path = "../data/" + filename
    
    try:
        # CSV-Datei einlesen
        df = pd.read_csv(path, sep=';', decimal=',', na_values=['-'])
        
        # Entferne Punkte aus den Zahlen (ersetze ',' mit '.')
        df.replace({r'\.': '', ',': '.'}, regex=True, inplace=True)
        
        # Konvertiere die relevanten Spalten in numerische Werte und ignoriere Fehler
        numeric_columns = df.columns[2:]  # Ab der 3. Spalte beginnen die Zahlen
        df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

        #Datum in brauchbare Form umwandeln
        df['Datum von'] = pd.to_datetime(df['Datum von'], format='%d%m%Y %H:%M')
        df['Datum bis'] = pd.to_datetime(df['Datum bis'], format='%d%m%Y %H:%M')
        
        df = addTimeInformation(df)

        # Summiere die Werte für jede Spalte
        column_sums = df[numeric_columns].sum()
        
        total_sum = column_sums.sum()
        

        renewable_sum = 0
        # Erneuerbare
        for i in range(7):
            renewable_sum += column_sums[i]
        renewable_sum+=column_sums[10]
        
        for i in range(12):
            print("Die Summe der " + str(i) + ". Spalte: " + str(column_sums[i]))
        
        print("Summe Gesamt: " + str(total_sum))
        print("Summe der Erneruabren: " + str(renewable_sum))
        print("Anteil der Erneubaren: " + str(renewable_sum/total_sum*100)[:5] + "%")
        
        # Ausgabe der Summen für jede Spalte
        # print("Summen der Spalten:")
        # print(column_sums)
        return df
    
    except FileNotFoundError:
        print("File has not been found.")

def addTimeInformation(df):
    df['Time'] = df['Datum von'].dt.time
    df['Month'] = df['Datum von'].dt.strftime('%b')
    df['Year Month'] = df['Datum von'].dt.strftime('%Y %m')
    df['Year Month Day'] = df['Datum von'].dt.strftime('%Y %m %d')
    df['Day'] = df['Datum von'].dt.strftime('%d')
    df['Year'] = df['Datum von'].dt.strftime('%Y')
    df['Weekday'] = df['Datum von'].dt.strftime('%u')
    df['Week'] = df['Datum von'].dt.strftime('%W')
    return df
        
if __name__ == "__main__":
    get_data("Realisierte_Erzeugung_202410050000_202410160000_Viertelstunde.csv")