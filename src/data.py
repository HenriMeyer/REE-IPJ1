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
    dfGen = dfGen.drop(columns = ['Kernenergie [MWh] Originalauflösungen', 'Braunkohle [MWh] Originalauflösungen', 'Steinkohle [MWh] Originalauflösungen', 'Erdgas [MWh] Originalauflösungen'])
    dfGen = dfGen.rename(columns = {
            'Biomasse [MWh] Originalauflösungen': 'Biomasse',
            'Wasserkraft [MWh] Originalauflösungen' : 'Wasserkraft',
            'Wind Offshore [MWh] Originalauflösungen':'Wind Offshore',
            'Wind Onshore [MWh] Originalauflösungen':'Wind Onshore',
            'Photovoltaik [MWh] Originalauflösungen':'Photovoltaik',
            'Sonstige Erneuerbare [MWh] Originalauflösungen':'Sonstige Erneuerbare',
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
            'Sonstige Konventionelle', 'Verbrauch'
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

        # 'Wärmepumpe' normalization
        df['Waermepumpe[in kWh]'] /= df['Waermepumpe[in kWh]'].sum()

        # Calculation of columns for later use in MWh
        for column in ['Waermepumpe[in kWh]', 'Elektroauto[Tagesnormiert]', 'ELKW[Tagesnormiert]']:
            df[column] = pd.to_numeric(df[column], errors='coerce')
            df[column] /= 1000

        # Renaming columns
        df.rename(
            columns = {
                'Waermepumpe[in kWh]': 'Wärmepumpe',
                'Elektroauto[Tagesnormiert]': 'E-Auto',
                #'ELKW[Tagesnormiert]': 'E-LKW'
            },
            inplace = True
        )
        df['E-LKW'] = df['E-Auto']
        # Average consumption per day and unit
        df['E-Auto'] *= 6.14
        df['E-LKW'] *= 65.75

    return {'leap': dfleap, 'normal': dfnormal}

# Add further information
def addInformation(df) -> pd.DataFrame:
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
    folder = "../output/" + keyStr + "/CSV"
    
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    for df in dfDict[key]:
        csvFilename = f"{folder}/{str(df['Datum von'].dt.year.iloc[0])}.csv"
        df.to_csv(csvFilename, index=False, sep=";")
    
    print(f"CSV-files have been created successfully ('{folder}')")

    
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