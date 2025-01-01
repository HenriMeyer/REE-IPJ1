import pandas as pd
import numpy as np
import os
from concurrent.futures import ThreadPoolExecutor

pd.options.mode.copy_on_write = True


# Get data and input is filename of the source, don't forget '.csv'
def readSMARD(filenameGen, filenameUse) -> pd.DataFrame:
    # Path -> move up a directory
    pathGen = "../data/" + filenameGen
    pathUse = "../data/" + filenameUse
    
    try:
        # Read file
        dfGen = pd.read_csv(
            pathGen,
            sep = ';',
            decimal = ',',
            thousands = '.',
            na_values = ['-'],
            parse_dates = [0,1],
            dayfirst = True
        )
    except FileNotFoundError:
        print(f"File '{filenameGen}' has not been found at path: {pathGen}")

    try:
        dfUse = pd.read_csv(
            pathUse,
            sep = ';',
            decimal = ',',
            thousands = '.',
            na_values = ['-'],
            parse_dates = [0,1],
            dayfirst = True
        )
    except FileNotFoundError:
        print(f"File '{filenameUse}' has not been found at path: {pathUse}")

    # Change names and drop obsolete
    dfGen = dfGen.drop(columns = ['Kernenergie [MWh] Originalauflösungen'])
    dfGen = dfGen.rename(columns = {
            'Biomasse [MWh] Originalauflösungen': 'Biomasse',
            'Wasserkraft [MWh] Originalauflösungen' : 'Wasserkraft',
            'Wind Offshore [MWh] Originalauflösungen':'Wind Offshore',
            'Wind Onshore [MWh] Originalauflösungen':'Wind Onshore',
            'Photovoltaik [MWh] Originalauflösungen':'Photovoltaik',
            'Sonstige Erneuerbare [MWh] Originalauflösungen':'Sonstige Erneuerbare',
            'Braunkohle [MWh] Originalauflösungen':'Braunkohle',
            'Steinkohle [MWh] Originalauflösungen':'Steinkohle',
            'Erdgas [MWh] Originalauflösungen':'Erdgas',
            'Pumpspeicher [MWh] Originalauflösungen':'Pumpspeicher',
            'Sonstige Konventionelle [MWh] Originalauflösungen':'Sonstige Konventionelle'
        }
    )

    dfUse = dfUse.drop(columns = ['Residuallast [MWh] Originalauflösungen', 'Pumpspeicher [MWh] Originalauflösungen', 'Datum von', 'Datum bis'])
    dfUse = dfUse.rename(columns = {'Gesamt (Netzlast) [MWh] Originalauflösungen': 'Verbrauch'})
    
    df = pd.concat([dfGen, dfUse], axis = 1)

    # Reorder the columns
    df = df[
        [
            'Datum von', 'Datum bis','Biomasse', 'Wasserkraft', 'Wind Onshore',
            'Wind Offshore', 'Photovoltaik', 'Sonstige Erneuerbare', 'Pumpspeicher',
            'Braunkohle', 'Steinkohle', 'Erdgas', 'Sonstige Konventionelle', 'Verbrauch'
        ]
    ]

    return df

def readLoadProfile() -> dict:
    # Read data
    dfleap = pd.read_csv("../data/loadprofile_leapyear.csv", sep = ';', encoding = 'latin-1', decimal = ',')
    dfnormal = pd.read_csv("../data/loadprofile_normal.csv", sep = ';', encoding = 'latin-1', decimal = ',')

    for df in (dfleap, dfnormal):
        # Remove timestamps
        df.drop(columns=['Jahr_von', 'Zeit_von'], inplace=True)

        # Calculation
        for column in ['Waermepumpe[in kWh]', 'Elektroauto[Tagesnormiert]']:
            df[column] = pd.to_numeric(df[column], errors='coerce')
            df[column] /= 1000

        df['Elektroauto[Tagesnormiert]'] = df['Elektroauto[Tagesnormiert]'] * 6.14
        df['E-LKW'] = df['Elektroauto[Tagesnormiert]']
        # Spalten umbenennen
        df.rename(
            columns = {
                'Waermepumpe[in kWh]': 'Wärmepumpe',
                'Elektroauto[Tagesnormiert]': 'E-Auto'
            },
            inplace = True
        )
        df['Wärmepumpe'] = df['Wärmepumpe']/3*5

    return {'leap': dfleap, 'normal': dfnormal}

# Add further information
def addInformation(df) -> pd.DataFrame:
    #df = formatTime(df)
    df = addPercentageRenewableLast(df)
    return df

def formatTime(df) -> pd.DataFrame:
    # Extract year, month, day, hour, minute from 'Datum von'
    df['Jahr'] = df['Datum von'].dt.year
    df['Monat'] = df['Datum von'].dt.month
    df['Tag'] = df['Datum von'].dt.day
    df['Uhrzeit'] = df['Datum von'].dt.time
    df['Monat Tag'] = df['Datum von'].dt.strftime('%m %d')
    
    return df

def addPercentageRenewableLast(df) -> pd.DataFrame:
    df['Konventionell'] = np.maximum(df['Verbrauch']-df.loc[:,['Biomasse','Wasserkraft','Wind Offshore','Wind Onshore','Photovoltaik','Sonstige Erneuerbare','Pumpspeicher Produktion',
        'Batteriespeicher Produktion']].sum(axis=1), 0)
    df['Anteil Erneuerbar [%]'] = (df.loc[:,['Biomasse','Wasserkraft','Wind Offshore','Wind Onshore','Photovoltaik','Sonstige Erneuerbare','Pumpspeicher Produktion',
        'Batteriespeicher Produktion']].sum(axis=1)/df['Verbrauch']*100).round(2)
    return df


# Renewable portion for each row excluding already counted
def countPercentageRenewableExclude(df) -> list:
    renewable_percentage = df['Anteil Erneuerbar [%]'].to_numpy()
    vector = np.zeros(11, dtype=int)
    
    for i in range(0, 10):
        vector[i] = np.sum((renewable_percentage >= 10 * i) & (renewable_percentage < 10 * (i+1)))
    vector[10] = np.sum((renewable_percentage >= 100))
        
    return vector.tolist()


# Write to CSV
def writeCSV(dfDict: dict) -> None:
    print("Writing data to csv...")
    key = str(next(iter(dfDict)))
    keyStr = str(key)
    folder = "../output/" + keyStr +"/CSV"
    if not os.path.exists(folder):
        os.makedirs(folder)
    with ThreadPoolExecutor() as executor:
        futures = []
        for df in dfDict[key]:
            csvFilename = f"{folder}/{str(df['Datum von'].dt.year.iloc[0])}.csv"
            futures.append(executor.submit(df.to_csv, csvFilename, index = False, sep = ";"))
        for future in futures:
            future.result()
    print(f"CSV-files have been created succesfully ('{folder}')")
    
# Write to excel
def writeExcel(dfDict: dict) -> None:
    print("Writing data to excel...")
    key = next(iter(dfDict))
    keyStr = str(key)
    folder = "../output/" + keyStr + "/Excel"
    if not os.path.exists(folder):
        os.makedirs(folder)
    excelFilename = folder + "/Simulation.xlsx"
    with pd.ExcelWriter(excelFilename, engine="openpyxl") as writer:
        for df in dfDict[key]:
            df.to_excel(writer, sheet_name=str(df['Datum von'].dt.year.iloc[0]), index = False, header = True)
    print(f"Die Excel-Datei '{excelFilename}' wurde erfolgreich erstellt.")
    
# Sum of one column
def sumColumn(df, columnName: str) -> np.float64:
    return df.loc[:,columnName].sum(axis=0)