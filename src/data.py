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
        # ---------------------------------------------------------------------------------------------
        # BRAUCHT MAN DAS?
        # df['Datum von'] = pd.to_datetime(df['Datum von'], format='%d.%m.%Y %H:%M')
        # df['Datum bis'] = pd.to_datetime(df['Datum bis'], format='%d.%m.%Y %H:%M')
        # ---------------------------------------------------------------------------------------------
        return df
        
    # Error handling
    except FileNotFoundError:
        print(f"File '{filename}' has not been found at path: {path}")
        
        
def residual_load(df):
    return (total_sum(df)-renewable_total(df))
    
    
def renewable_total(df):
    renewable_columns = df.iloc[:, list(range(2,8))+ [12]]
    renewable_sum = renewable_columns.sum().sum()
    print(df.iloc[:, 0])
    return renewable_sum

def total_sum(df):
    numeric_columns = df.columns[2:]
    column_sums = df[numeric_columns].sum().sum()
    print(column_sums)
    return column_sums

def portion_renewable(df):
    # portion kann auch nur in return geschrieben werden nur zum testen
    portion = renewable_total(df)/total_sum(df)*100
    # print("Anteil der Erneubaren: " + str(portion) + "%")
    # print(residual_load(df))
    return portion
    
if __name__ == "__main__":
    portion_renewable(read_SMARD("Realisierte_Erzeugung_202410050000_202410160000_Viertelstunde.csv"))