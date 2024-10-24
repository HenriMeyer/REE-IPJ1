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
        df = row_sums_all(df)
        df = extract_time_components(df)
        return df
        
    # Error handling
    except FileNotFoundError:
        print(f"File '{filename}' has not been found at path: {path}")

# Extract time components and reorder
def extract_time_components(df):
    # Extract year, month, day, hour, minute from 'Datum von'
    df['Jahr_von'] = df['Datum von'].dt.year
    df['Monat_von'] = df['Datum von'].dt.month
    df['Tag_von'] = df['Datum von'].dt.day
    df['Uhrzeit_von'] = df['Datum von'].dt.time
    
    # Extract year, month, day, hour, minute from 'Datum bis'
    df['Jahr_bis'] = df['Datum bis'].dt.year
    df['Monat_bis'] = df['Datum bis'].dt.month
    df['Tag_bis'] = df['Datum bis'].dt.day
    df['Uhrzeit_bis'] = df['Datum bis'].dt.time
    
    # Remove the original date columns
    df = df.drop(columns=['Datum von', 'Datum bis'])
    
    # Reorder the columns
    new_order = [
        'Jahr_von', 'Monat_von', 'Tag_von', 'Uhrzeit_von',
        'Jahr_bis', 'Monat_bis', 'Tag_bis', 'Uhrzeit_bis',
        'Biomasse', 'Wasserkraft', 'Wind Offshore', 'Wind Onshore',
        'Photovoltaik', 'Sonstige Erneuerbare', 'Pumpspeicher',
        'Kernenergie', 'Braunkohle', 'Steinkohle', 'Erdgas', 'Pumpspeicher',
        'Sonstige Konventionelle','Erneuerbar', 'Total', 'Residual'
    ]

    df = df[new_order]

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
    return df.loc[index, ['Jahr_von', 'Monat_von', 'Tag_von', 'Uhrzeit_von',
                           'Jahr_bis', 'Monat_bis', 'Tag_bis', 'Uhrzeit_bis',
                           'Biomasse', 'Wasserkraft', 'Wind Offshore', 'Wind Onshore',
                           'Photovoltaik', 'Sonstige Erneuerbare', 'Pumpspeicher']]

# row EE anteil switch case 'd' 'm' 'y' und dann als dataframe zurückgeben??? ist realisierbar oder als float64
# 
# 
# 

def row_sums_all(df):

    df['Erneuerbar'] = df.loc[:,['Biomasse','Wasserkraft','Wind Offshore','Wind Onshore','Photovoltaik','Sonstige Erneuerbare','Pumpspeicher']].sum(axis = 1)
    df['Total'] = df.loc[:,'Biomasse':'Sonstige Konventionelle'].sum(axis = 1)
    df['Residual'] = df['Total']- df['Erneuerbar']
    return df


# For testing: "Realisierte_Erzeugung_202410050000_202410160000_Viertelstunde.csv"
if __name__ == "__main__":
    df = read_SMARD("Realisierte_Erzeugung_202410050000_202410160000_Viertelstunde.csv")
    print(df)
    # Display the first 10 renewable data rows
    # for i in range(0, 10):
    #     row_df = row_renewable_df(df, i)
    #     print(row_df)