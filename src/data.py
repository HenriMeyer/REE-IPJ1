import pandas as pd
import numpy as np


# Get data and input is filename of the source, don't forget '.csv'
def read_SMARD(filename, generation:bool = True):
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
                'Sonstige Konventionelle','Erneuerbar','Anteil Erneuerbar [%]', 'Total', 'Residual'
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
def formatTime(df):
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
def sumColumn(df, columnName: str):
    return df.loc[:,columnName].sum(axis=0)


# Generation
# Add further information
def addDataInformation(df):
    df['Erneuerbar'] = df.loc[:,['Biomasse','Wasserkraft','Wind Offshore','Wind Onshore','Photovoltaik','Sonstige Erneuerbare','Pumpspeicher']].sum(axis=1)
    df['Total'] = df.loc[:,'Biomasse':'Sonstige Konventionelle'].sum(axis=1)
    df['Residual'] = df['Total']- df['Erneuerbar']
    return df

def addPercantageRenewable(df):
    df['Anteil Erneuerbar [%]'] = (df.loc[:,['Biomasse','Wasserkraft','Wind Offshore','Wind Onshore','Photovoltaik','Sonstige Erneuerbare','Pumpspeicher']].sum(axis=1)/df.loc[:,'Biomasse':'Sonstige Konventionelle'].sum(axis=1)*100).round(2)
    return df

def addPercentageRenewableLast(df):
    df['Anteil Erneuerbar [%]'] = (100-df['Residuallast']/df['Gesamt']*100).round(2)
    return df

# Renewable portion for each row
def countPercentageRenewable(df):
    renewable_percentage = df['Anteil Erneuerbar [%]'].to_numpy()
    vector = np.zeros(11, dtype=int)
    
    for i in range(1, 11):
        vector[i] = np.sum(renewable_percentage >= 10 * i)
    vector[0] = len(df)
    
    return vector.tolist()

# Renewable portion for each row excluding already counted
def countPercentageRenewableExclude(df):
    renewable_percentage = df['Anteil Erneuerbar [%]'].to_numpy()
    vector = np.zeros(11, dtype=int)
    
    for i in range(0, 11):
        vector[i] = np.sum((renewable_percentage >= 10 * i) & (renewable_percentage < 10 * (i+1)))
        
    return vector.tolist()


# Consumption

# Save data in csv
def appendCSV(df1, df2, df3, df4, df5, df6):
    filePath = '../data/Datensatz.csv'
    generation = [df1, df2, df3]
    consumption = [df4, df5, df6]
    with open(filePath, 'a') as file:
        file.write("Stromerzeugung von 2021-2023\n")
    write_header = True
    for df in generation:
        numberRows = df.shape[0]
        df = df[['Jahr', 'Biomasse', 'Wasserkraft', 'Wind Offshore', 
                 'Wind Onshore', 'Photovoltaik', 'Sonstige Erneuerbare',
                 'Kernenergie', 'Braunkohle', 'Steinkohle', 'Erdgas', 
                 'Pumpspeicher', 'Sonstige Konventionelle', 'Erneuerbar', 
                 'Anteil Erneuerbar [%]', 'Total', 'Residual']]
        
        df = df.groupby('Jahr').sum().reset_index()
        for column in df.columns:
            if column not in ['Jahr', 'Anteil Erneuerbar [%]']:
                df[column] = round(df[column] / 1e+6,3)
        df['Anteil Erneuerbar [%]'] = round(df['Anteil Erneuerbar [%]'] / numberRows,2)
        
        df.to_csv(filePath, mode='a', header=write_header, index=False, sep=';', decimal=',')
        write_header = False
    write_header = True
    with open(filePath, 'a') as file:
        file.write("Stromverbrauch von 2021-2023\n")
    for df in consumption:
        df = df[['Jahr', 'Gesamt', 'Residuallast', 'Pumpspeicher']]
        df = df.groupby('Jahr').sum().reset_index()
        for column in df.columns:
            if column not in ['Jahr']:
                df[column] = round(df[column] / 1e+6,3)
        df.to_csv(filePath, mode='a', header=write_header, index=False, sep=';', decimal=',')
        write_header = False
    with open(filePath, 'a') as file:
        file.write("Alle Werte sind in TWh angegeben\n")
        file.write("https://www.smard.de/home/downloadcenter/download-marktdaten/\n")


if __name__ == "__main__":
    # df = read_SMARD("Realisierte_Erzeugung_202301010000_202401010000_Viertelstunde.csv")
    df = read_SMARD("Realisierter_Stromverbrauch_202101010000_202201010000_Viertelstunde.csv", False)
    print(df)
    # print(sumColumn(df,"Photovoltaik"))