import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor


# Get data and input is filename of the source, don't forget '.csv'
def read_SMARD(filenameGen, filenameUse) -> pd.DataFrame:
    # Path -> move up a directory
    pathGen = "../data/" + filenameGen
    pathUse = "../data/" + filenameUse
    
    try:
        # Read file
        dfGen = pd.read_csv(
            pathGen,
            sep=';',
            decimal=',',
            thousands='.',
            na_values=['-'],
            parse_dates=[0,1],
            dayfirst=True
        )
    except FileNotFoundError:
        print(f"File '{filenameGen}' has not been found at path: {pathGen}")

    try:
        dfUse = pd.read_csv(
            pathUse,
            sep=';',
            decimal=',',
            thousands='.',
            na_values=['-'],
            parse_dates=[0,1],
            dayfirst=True
        )
    except FileNotFoundError:
        print(f"File '{filenameUse}' has not been found at path: {pathUse}")

    # Change names and drop obsolete
    dfGen = dfGen.rename(
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

    dfGen = dfGen.drop(columns = ['Kernenergie'])
        
    dfUse = dfUse.rename(
    columns={'Gesamt (Netzlast) [MWh] Originalauflösungen': 'Verbrauch',
              'Residuallast [MWh] Originalauflösungen': 'Residuallast',
             'Pumpspeicher [MWh] Originalauflösungen': 'Pumpspeicher'
        }
    )

    dfUse = dfUse.drop(columns = ['Residuallast', 'Pumpspeicher', 'Datum von', 'Datum bis'])
        
    df = pd.concat([dfGen, dfUse], axis = 1)

    # Reorder the columns
    new_order = [
        'Datum von', 'Datum bis',
        'Biomasse', 'Wasserkraft', 'Wind Offshore', 'Wind Onshore',
        'Photovoltaik', 'Sonstige Erneuerbare', 'Pumpspeicher',
        'Braunkohle', 'Steinkohle', 'Erdgas',
        'Sonstige Konventionelle','Verbrauch'
    ]
    df = df[new_order]

    return df

def readLoadProfile():
    # Gemeinsame Optionen für das Einlesen
    read_options = {
        'sep': ';',                  # Trennzeichen
        'encoding': 'latin-1',       # Encoding
        'decimal': ','              # Dezimaltrennzeichen (falls notwendig)
    }

    # Dateien einlesen
    dfleap = pd.read_csv("..\data\loadprofile_leapyear.csv", **read_options)
    dfnormal = pd.read_csv("..\data\loadprofile_normal.csv", **read_options)

    for df in (dfleap, dfnormal):
        # Entfernen von Zeitdaten
        df.drop(columns=['Jahr_von', 'Zeit_von'], inplace=True)

        # Zahlen als Float konvertieren, falls nötig
        for column in ['Waermepumpe[in kWh]', 'Elektroauto[Tagesnormiert]']:
            df[column] = pd.to_numeric(df[column], errors='coerce')
            df[column] /= 1000

        # Berechnung durchführen
        df['Elektroauto[Tagesnormiert]'] = df['Elektroauto[Tagesnormiert]'] * 6.14

        # Spalten umbenennen
        df.rename(
            columns={
                'Waermepumpe[in kWh]': 'Wärmepumpe',
                'Elektroauto[Tagesnormiert]': 'E-Auto'
            },
            inplace=True
        )

    return {'leap': dfleap, 'normal': dfnormal}

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
    #df = df.drop(columns=['Datum von', 'Datum bis'])
    return df

# Sum of one column
def sumColumn(df, columnName: str) -> np.float64:
    return df.loc[:,columnName].sum(axis=0)


# Generation
# Add further information
def addPercentageRenewableLast(df):
    df['Anteil Erneuerbar [%]'] = (df.loc[:,['Biomasse','Wasserkraft','Wind Offshore','Wind Onshore','Photovoltaik','Sonstige Erneuerbare']].sum(axis=1)/df['Verbrauch']*100).round(2)
    return df

def addInformation(df) -> pd.DataFrame:
    df = formatTime(df)
    df = addPercentageRenewableLast(df)
    return df

# Renewable portion for each row excluding already counted
def countPercentageRenewableExclude(df) -> list:
    renewable_percentage = df['Anteil Erneuerbar [%]'].to_numpy()
    vector = np.zeros(11, dtype=int)
    
    for i in range(0, 10):
        vector[i] = np.sum((renewable_percentage >= 10 * i) & (renewable_percentage < 10 * (i+1)))
    vector[10] = np.sum((renewable_percentage >= 100))
        
    return vector.tolist()

# Append to CSV
def appendCSV(dfList: list) -> None:
    folder = "../Output/CSV/Simulation"
    with ThreadPoolExecutor() as executor:
        futures = []
        for df in dfList:
            csvFilename = folder + str(df['Datum von'].dt.year.iloc[0]) + ".csv"
            futures.append(executor.submit(df.to_csv,csvFilename, index=False, sep=";"))
        for future in futures:
            future.result()
    print(f"CSV-files have been created succesfully ('{folder}')")  
    
# Write simulation to excel
def writeExcel(dfList: pd.DataFrame) -> None:
    excelFilename = "../Output/Excel/Simulation.xlsx"
    with pd.ExcelWriter(excelFilename, engine="openpyxl") as writer:
        for df in dfList:
            df.to_excel(writer, sheet_name=str(df['Datum von'].dt.year.iloc[0]), index=False, header=True)
    print(f"Die Excel-Datei '{excelFilename}' wurde erfolgreich erstellt.")


# For Testing
# if __name__ == "__main__":