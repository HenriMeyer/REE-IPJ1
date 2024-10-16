import pandas as pd



# Get data and input is filename of the source, don't forget '.csv'
def read_SMARD(filename):
    # Path -> move up a directory
    path = "../data/" + filename
    
    # Try block
    try:
        # Read file
        df = pd.read_csv(
            path,
            sep=';',
            decimal=',',
            thousands='.',
            na_values=['-'],
            parse_dates=[0,1],
            dayfirst=True
        )
        
        # Change names
        df = df.rename(
        columns={
            'Biomasse [MWh] Originalauflösungen': 'Biomasse',
            'Wasserkraft [MWh] Originalauflösungen' : 'Wasserkraft',
            'Wind Offshore [MWh] Originalauflösungen':'Wind Offshore',
            'Wind Onshore [MWh] Originalauflösungen':'Wind Onshore',
            'Photovoltaik [MWh] Originalauflösungen':'Photovoltaik',
            'Sonstige Erneuerbare [MWh] Originalauflösungen':'Sonstige Erneuerbare',
            'Kernenergie [MWh] Originalauflösungen':'Kernenergie',
            'Braunkohle [MWh] Originalauflösungen':'Braunkohle',
            'Steinkohle [MWh] Originalauflösungen':'Steinkohle',
            'Erdgas [MWh] Originalauflösungen':'Erdgas',
            'Pumpspeicher [MWh] Originalauflösungen':'Pumpspeicher',
            'Sonstige Konventionelle [MWh] Originalauflösungen':'Sonstige Konventionelle'
            }
        )
        return df
        
        # # Remove dots and exchange ',' with '.'
        # df.iloc[:, 2:] = df.iloc[:, 2:].replace({r'\.': '', ',': '.'}, regex=True)
        # df[2:].replace({r'\.': '', ',': '.'}, regex=True, inplace=True)
        
        
        # # Konvertiere die relevanten Spalten in numerische Werte und ignoriere Fehler
        # numeric_columns = df.columns[2:]  # Ab der 3. Spalte beginnen die Zahlen
        # df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')
        
        
        # # Setup for data
        # date_time = df.columns[2:]
        # renewable = df.iloc[:, list(range(2, 7)) + [11]]
        # konventional = df.iloc[:, list(range(9, 11)) + [13]]
        # print(date_time)
        
        
        # column_sums = df[numeric_columns].sum()
        
        # total_sum = column_sums.sum()
        # # timestamps = df.iloc[:,0]
        # # # print(timestamps.iloc[:,0])
        
        
        # renewable_sum = 0
        # # Erneuerbare
        # for i in range(7):
        #     renewable_sum += column_sums[i]
        # renewable_sum+=column_sums[11]
        
        # for i in range(11):
        #     print("Die Summe der " + str(i) + ". Spalte: " + str(column_sums[i]))
        
        # print("Summe Gesamt: " + str(total_sum))
        # print("Summe der Erneruabren: " + str(renewable_sum))
        # print("Anteil der Erneubaren: " + str(renewable_sum/total_sum*100)[:5] + "%")
        # print(df.iloc[:, 0])
        
        # # Ausgabe der Summen für jede Spalte
        # print("Summen der Spalten:")
        # print(column_sums)
    
    # Error handling
    except FileNotFoundError:
        print(f"File '{filename}' has not been found at path: {path}")
        
        
if __name__ == "__main__":
    read_SMARD("Realisierte_Erzeugung_202410050000_202410160000_Viertelstunde.csv")