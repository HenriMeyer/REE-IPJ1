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
        
    # Error handling
    except FileNotFoundError:
        print(f"File '{filename}' has not been found at path: {path}")


# Total functions
def total_sum(df):
    return df.iloc[:,2:].sum().sum()

def total_renewable(df):
    return df.loc[:, ['Biomasse','Wasserkraft','Wind Offshore','Wind Onshore','Photovoltaik','Sonstige Erneuerbare','Pumpspeicher']].sum().sum()

def total_portion_renewable(df):
    return total_renewable(df)/total_sum(df)

def total_residual(df):
    return (total_sum(df)-total_renewable(df))


# Row functions
def row_renewable(df, index: int):
    return df.loc[index, ['Biomasse','Wasserkraft','Wind Offshore','Wind Onshore','Photovoltaik','Sonstige Erneuerbare','Pumpspeicher']].sum()
    
def row_total(df, index: int):
    return df.iloc[index, 2:].sum()

def row_residual(df, index: int):
    return(row_total(df, index)-row_renewable(df,index))


# For testing: "Realisierte_Erzeugung_202410050000_202410160000_Viertelstunde.csv"
if __name__ == "__main__":
    for i in range(0,10):
        print(total_sum(read_SMARD("Realisierte_Erzeugung_202410050000_202410160000_Viertelstunde.csv")))