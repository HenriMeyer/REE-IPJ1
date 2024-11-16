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
    
    for i in range(0, 11):
        vector[i] = np.sum((renewable_percentage >= 10 * i) & (renewable_percentage < 10 * (i+1)))
        
    return vector.tolist()

# Append to csv
def append_sum_to_csv(df: pd.DataFrame, csv_filename: str):
    # Erstelle eine leere Liste, um die Summen der relevanten Spalten zu speichern
    year_summaries = []

    # Iteriere durch die Jahre im DataFrame
    unique_years = df['Jahr'].unique()
    for year in unique_years:
        # Filtere den DataFrame für das aktuelle Jahr
        yearly_data = df[df['Jahr'] == year]
        
        # Berechne die Summe für jede Spalte
        column_sums = yearly_data.sum(numeric_only=True)
        
        # Erstelle eine Zeile für das Jahr mit den berechneten Summen
        summary_row = {'Jahr': year}
        summary_row.update(column_sums.to_dict())
        
        # Füge die Zeile zur Liste hinzu
        year_summaries.append(summary_row)

    # Erstelle einen DataFrame aus den Jahreszusammenfassungen
    summary_df = pd.DataFrame(year_summaries)

    # Überprüfe, ob die CSV-Datei bereits existiert
    if os.path.exists(csv_filename):
        # Falls ja, hänge die neuen Daten an
        summary_df.to_csv(csv_filename, mode='a', header=False, index=False)
    else:
        # Falls nein, schreibe die Datei mit Header
        summary_df.to_csv(csv_filename, mode='w', header=True, index=False)

    print(f"Summen der Jahre wurden erfolgreich zu {csv_filename} hinzugefügt.")


# For Testing
if __name__ == "__main__":
    df = read_SMARD("Realisierte_Erzeugung_202301010000_202401010000_Viertelstunde.csv")
    # df = read_SMARD("Realisierter_Stromverbrauch_202101010000_202201010000_Viertelstunde.csv", False)
    print(df)
    # print(sumColumn(df,"Photovoltaik"))