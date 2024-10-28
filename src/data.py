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
                'Kernenergie', 'Braunkohle', 'Steinkohle', 'Erdgas', 'Pumpspeicher',
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

def addDataInformation(df):
    df['Erneuerbar'] = df.loc[:,['Biomasse','Wasserkraft','Wind Offshore','Wind Onshore','Photovoltaik','Sonstige Erneuerbare','Pumpspeicher']].sum(axis=1)
    df['Total'] = df.loc[:,'Biomasse':'Sonstige Konventionelle'].sum(axis=1)
    df['Residual'] = df['Total']- df['Erneuerbar']
    return df

def addPercantageRenewable(df):
    df['Anteil Erneuerbar [%]'] = (df.loc[:,['Biomasse','Wasserkraft','Wind Offshore','Wind Onshore','Photovoltaik','Sonstige Erneuerbare','Pumpspeicher']].sum(axis=1)/df.loc[:,'Biomasse':'Sonstige Konventionelle'].sum(axis=1)*100).round(2)
    return df


# Total functions
def total_sum(df):
    return df.iloc[:,2:].sum().sum()

def total_renewable_sum(df):
    return df.loc[:, ['Biomasse','Wasserkraft','Wind Offshore','Wind Onshore','Photovoltaik','Sonstige Erneuerbare','Pumpspeicher']].sum().sum()

def total_portion_renewable_sum(df):
    return total_renewable_sum(df)/total_sum(df)

def total_residual_sum(df):
    return (total_sum(df)-total_renewable_sum(df))


# Row functions
def row_renewable_sum(df, index: int):
    return df.loc[index, ['Biomasse','Wasserkraft','Wind Offshore','Wind Onshore','Photovoltaik','Sonstige Erneuerbare','Pumpspeicher']].sum()

def row_total_sum(df, index: int):
    return df.iloc[index, 2:].sum()

def row_residual_sum(df, index: int):
    return(row_total_sum(df, index)-row_renewable_sum(df,index))

def row_renewable_df(df, index: int):
    return df.loc[index, ['Jahr', 'Monat', 'Tag', 'Uhrzeit',
                           'Biomasse', 'Wasserkraft', 'Wind Offshore', 'Wind Onshore',
                           'Photovoltaik', 'Sonstige Erneuerbare', 'Pumpspeicher']]

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


if __name__ == "__main__":
    # df = read_SMARD("Realisierte_Erzeugung_202101010000_202201010000_Viertelstunde.csv")
    df = read_SMARD("Realisierter_Stromverbrauch_202101010000_202201010000_Viertelstunde.csv", False)
    print(df)