import pandas as pd
import numpy as np
import os


# Get data and input is filename of the source, don't forget '.csv'
def read_SMARD(filename, generation:bool = True) -> pd.DataFrame:
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
        
        # Format time
        df = formatTime(df)
        
        if(generation):
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
            
            # Add further information to dataframe
            df = addDataInformation(df)
            df = addPercantageRenewable(df)
        
            # Reorder the columns
            new_order = [
                'Jahr', 'Monat', 'Tag', 'Uhrzeit', 'Monat Tag',
                'Biomasse', 'Wasserkraft', 'Wind Offshore', 'Wind Onshore',
                'Photovoltaik', 'Sonstige Erneuerbare', 'Pumpspeicher',
                'Kernenergie', 'Braunkohle', 'Steinkohle', 'Erdgas',
                'Sonstige Konventionelle','Erneuerbar','Anteil Erneuerbar [%]', 'Total'
            ]
            df = df[new_order]
        else:
            df = df.rename(
            columns={'Gesamt (Netzlast) [MWh] Originalauflösungen': 'Gesamt',
                     'Residuallast [MWh] Originalauflösungen': 'Residuallast',
                     'Pumpspeicher [MWh] Originalauflösungen': 'Pumpspeicher'
                }
            )
            new_order = ['Jahr', 'Monat', 'Tag', 'Uhrzeit', 'Monat Tag', 'Gesamt', 'Residuallast', 'Pumpspeicher']
            df = df[new_order]
        return df
        
    # Error handling
    except FileNotFoundError:
        print(f"File '{filename}' has not been found at path: {path}")


# General
# Add further information
def formatTime(df) -> pd.DataFrame:
    # Extract year, month, day, hour, minute from 'Datum von'
    df['Jahr'] = df['Datum von'].dt.year
    df['Monat'] = df['Datum von'].dt.month
    df['Tag'] = df['Datum von'].dt.day
    df['Uhrzeit'] = df['Datum von'].dt.time
    df['Monat Tag'] = df['Datum von'].dt.strftime('%m %d')
    
    # Remove the original date columns
    df = df.drop(columns=['Datum von', 'Datum bis'])
    return df

# Sum of one column
def sumColumn(df, columnName: str) -> np.float64:
    return df.loc[:,columnName].sum(axis=0)


# Generation
# Add further information
def addDataInformation(df) -> pd.DataFrame:
    df['Erneuerbar'] = df.loc[:,['Biomasse','Wasserkraft','Wind Offshore','Wind Onshore','Photovoltaik','Sonstige Erneuerbare','Pumpspeicher']].sum(axis=1)
    df['Total'] = df.loc[:,'Biomasse':'Sonstige Konventionelle'].sum(axis=1)
    return df

def addPercantageRenewable(df):
    df['Anteil Erneuerbar [%]'] = (df.loc[:,['Biomasse','Wasserkraft','Wind Offshore','Wind Onshore','Photovoltaik','Sonstige Erneuerbare','Pumpspeicher']].sum(axis=1)/df.loc[:,'Biomasse':'Sonstige Konventionelle'].sum(axis=1)*100).round(2)
    return df

def addPercentageRenewableLast(df, df2):
    df['Anteil Erneuerbar [%]'] = (df2.loc[:,['Biomasse','Wasserkraft','Wind Offshore','Wind Onshore','Photovoltaik','Sonstige Erneuerbare']].sum(axis=1)/df['Gesamt']*100).round(2)
    return df

# Renewable portion for each row
def countPercentageRenewable(df) -> list:
    renewable_percentage = df['Anteil Erneuerbar [%]'].to_numpy()
    vector = np.zeros(11, dtype=int)
    
    for i in range(1, 11):
        vector[i] = np.sum(renewable_percentage >= 10 * i)
    vector[0] = len(df)
    
    return vector.tolist()

# Renewable portion for each row excluding already counted
def countPercentageRenewableExclude(df) -> list:
    renewable_percentage = df['Anteil Erneuerbar [%]'].to_numpy()
    vector = np.zeros(11, dtype=int)
    
    for i in range(0, 10):
        vector[i] = np.sum((renewable_percentage >= 10 * i) & (renewable_percentage < 10 * (i+1)))
    vector[10] = np.sum((renewable_percentage >= 100))
        
    return vector.tolist()

# Append to CSV
def appendYearlyCSV(dfList: list, filename: str):
    # Kombiniere alle DataFrames in der Liste zu einem einzigen DataFrame
    combined_df = pd.concat(dfList, ignore_index=True)

    # Sicherstellen, dass die Spalte 'Jahr' numerisch ist
    combined_df['Jahr'] = pd.to_numeric(combined_df['Jahr'], errors='coerce', downcast='integer')

    # Liste aller numerischen Spalten, die summiert werden sollen
    numeric_columns_to_sum = combined_df.select_dtypes(include='number').columns.tolist()

    # Sicherstellen, dass 'Jahr' in den Spalten enthalten ist (sollte an erster Stelle stehen)
    if 'Jahr' not in numeric_columns_to_sum:
        numeric_columns_to_sum.insert(0, 'Jahr')

    # Header-Zeile mit den Spaltennamen
    header = ['Jahr'] + [col for col in numeric_columns_to_sum if col != 'Jahr']

    # Dateiname mit dem Jahrbereich aus dem kombinierten DataFrame erstellen
    csvFilename = "../Output/" + filename + "_" + str(combined_df['Jahr'].min()) + "_" + str(combined_df['Jahr'].max()) + ".csv"

    # Überschreiben oder Neu-Erstellen der Datei mit der Header-Zeile
    with open(csvFilename, 'w', encoding='utf-8') as f:
        f.write(';'.join(header) + '\n')  # Header schreiben

    # Iteriere durch die eindeutigen Jahre im kombinierten DataFrame
    unique_years = sorted(combined_df['Jahr'].dropna().unique())  # Eindeutige, sortierte Jahre
    for year in unique_years:
        yearly_data = combined_df[combined_df['Jahr'] == year]  # Filter Daten für das Jahr

        # Berechne die Summen der numerischen Spalten
        sum_row = [year]  # Beginne mit dem Jahr
        for col in numeric_columns_to_sum:
            if col != 'Jahr':
                sum_value = yearly_data[col].sum()  # Summe der Spalte
                sum_row.append(str(round(sum_value, 2)).replace('.', ','))  # Dezimaltrenner ersetzen (Excel-konform)

        # Füge die Zeile in die CSV-Datei ein
        with open(csvFilename, 'a', encoding='utf-8') as f:
            f.write(';'.join(map(str, sum_row)) + '\n')

    print(f"{csvFilename} has been created.")

    
# Write simulation to excel
def writeExcel(dfList: pd.DataFrame, filename: str) -> None:
    excelFilename = "../Output/" + filename + ".xlsx"

    # Schreiben in die Excel-Datei
    with pd.ExcelWriter(excelFilename, engine="openpyxl") as writer:
        for df in dfList:
            df.to_excel(writer, sheet_name=str(df['Datum von'].dt.year.iloc[0]), index=False, header=True)

    print(f"Die Excel-Datei '{excelFilename}' wurde erfolgreich erstellt.")



# For Testing
if __name__ == "__main__":
    df = read_SMARD("Realisierte_Erzeugung_202301010000_202401010000_Viertelstunde.csv")
    # df = read_SMARD("Realisierter_Stromverbrauch_202101010000_202201010000_Viertelstunde.csv", False)
    print(df)
    # print(sumColumn(df,"Photovoltaik"))