import pandas as pd
import numpy as np


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
        
        # Add further information to dataframe
        df = formatTime(df)
        df = addDataInformation(df)
        df = addPercantageRenewable(df)
        
        # Reorder the columns
        new_order = [
            'Jahr', 'Monat', 'Tag', 'Uhrzeit',
            'Biomasse', 'Wasserkraft', 'Wind Offshore', 'Wind Onshore',
            'Photovoltaik', 'Sonstige Erneuerbare', 'Pumpspeicher',
            'Kernenergie', 'Braunkohle', 'Steinkohle', 'Erdgas', 'Pumpspeicher',
            'Sonstige Konventionelle','Erneuerbar','Anteil Erneuerbar [%]', 'Total', 'Residual'
        ]
        df = df[new_order]
        
        return df
        
    # Error handling
    except FileNotFoundError:
        print(f"File '{filename}' has not been found at path: {path}")

# Extract time components and reorder
def formatTime(df):
    # Extract year, month, day, hour, minute from 'Datum von'
    df['Jahr'] = df['Datum von'].dt.year
    df['Monat'] = df['Datum von'].dt.month
    df['Tag'] = df['Datum von'].dt.day
    df['Uhrzeit'] = df['Datum von'].dt.time
    
    # Remove the original date columns
    df = df.drop(columns=['Datum von', 'Datum bis'])

    # Return the updated DataFrame
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

# Add further information to dataframe
def addPercantageRenewable(df):
    df['Anteil Erneuerbar [%]'] = (df.loc[:,['Biomasse','Wasserkraft','Wind Offshore','Wind Onshore','Photovoltaik','Sonstige Erneuerbare','Pumpspeicher']].sum(axis=1)/df.loc[:,'Biomasse':'Sonstige Konventionelle'].sum(axis=1)*100).round(2)
    return df

def addDataInformation(df):
    df['Erneuerbar'] = df.loc[:,['Biomasse','Wasserkraft','Wind Offshore','Wind Onshore','Photovoltaik','Sonstige Erneuerbare','Pumpspeicher']].sum(axis=1)
    df['Total'] = df.loc[:,'Biomasse':'Sonstige Konventionelle'].sum(axis=1)
    df['Residual'] = df['Total']- df['Erneuerbar']
    return df


# For testing: "Realisierte_Erzeugung_202101010000_202201010000_Viertelstunde.csv"
if __name__ == "__main__":
    df = read_SMARD("Realisierte_Erzeugung_202101010000_202201010000_Viertelstunde.csv")
    print(df)
    print(countPercentageRenewable(df))