import pandas as pd

generation = {
    'Biomasse': 40000000,
    'Wasserkraft': 40000000,
    'Wind Offshore': 40000000,
    'Wind Onshore': 40000000,
    'Photovoltaik': 40000000,
    'Sonstige Erneuerbare': 40000000,
    'Braunkohle': 40000000,
    'Steinkohle': 40000000,
    'Erdgas': 40000000,
    'Pumpspeicher': 40000000,
    'Sonstige Konventionelle': 40000000
}
generationYear = 2030

def simulation(df: pd.DataFrame) -> list:
    df = fixDataFrame(df)
    startYear = int(df['Datum von'].dt.year.iloc[0])
    while True:
        generationYear = input("Year for forecast: ")
        if generationYear.isdigit() and int(generationYear) > startYear:
                break
        else:
            print(f"\033[31m{generationYear} is an invalid input, it has to be bigger than {startYear} and a digit!\033[0m")
    for key in generation:
        while True:
            try:
                generation[key] = float(input(f"Value for {key}: "))
                break
            except ValueError:
                print("\033[31mInvalid input! Please enter a numeric value.\033[0m")
    dfList = []
    dfCurrent = df.copy()
    for currentYear in range(startYear + 1, int(generationYear) + 1):
        # Replace years
        print(dfCurrent['Datum von'].astype)
        dfCurrent['Datum von'] = dfCurrent['Datum von'].map(lambda x: x.replace(year=currentYear))
        dfCurrent['Datum bis'] = dfCurrent['Datum bis'].map(lambda x: x.replace(year=currentYear))
        # Replace last year
        dfCurrent.iloc[-1, dfCurrent.columns.get_loc('Datum bis')] = dfCurrent.iloc[-1]['Datum bis'].replace(year=currentYear + 1)
        for column in df.columns:
            if column in ['Datum von', 'Datum bis']:
                continue
            if column in generation:
                dfCurrent[column] = round(df[column] * (((generation[column] / df[column].sum() - 1) / (int(generationYear) - startYear)) * (currentYear - startYear) + 1), 2)
            else:   
                print(column + " wasn't simulated.")
        dfList.append(dfCurrent)
    
    return dfList



def simulation_use(df: pd.DataFrame) -> list:
    df = fixDataFrame2(df)
    startYear = int(df['Datum von'].dt.year.iloc[0])
    while True:
        try:
            usage = float(input(f"Value for nergyusage: "))
            break
        except ValueError:
            print("\033[31mInvalid input! Please enter a numeric value.\033[0m")
    dfList = []
    dfCurrent = df.copy()
    for currentYear in range(startYear + 1, int(generationYear) + 1):
        # Replace years
        print(dfCurrent['Datum von'].astype)
        dfCurrent['Datum von'] = dfCurrent['Datum von'].map(lambda x: x.replace(year=currentYear))
        dfCurrent['Datum bis'] = dfCurrent['Datum bis'].map(lambda x: x.replace(year=currentYear))
        # Replace last year
        dfCurrent.iloc[-1, dfCurrent.columns.get_loc('Datum bis')] = dfCurrent.iloc[-1]['Datum bis'].replace(year=currentYear + 1)
        dfCurrent['Gesamt'] = round(df['Gesamt'] * (((usage / df['Gesamt'].sum() - 1) / (int(generationYear) - startYear)) * (currentYear - startYear) + 1), 2)
        dfList.append(dfCurrent)
    
    return dfList



def fixDataFrame(df: pd.DataFrame) -> pd.DataFrame:
    df['Datum von'] = pd.to_datetime(df['Jahr'].astype(str) + '-' +
                                      df['Monat'].astype(str).str.zfill(2) + '-' +
                                      df['Tag'].astype(str).str.zfill(2) + ' ' +
                                      df['Uhrzeit'].astype(str), format='%Y-%m-%d %H:%M:%S')

    df['Datum bis'] = df['Datum von'] + pd.Timedelta(minutes=15)
    
    df = df.drop(columns=['Jahr', 'Monat', 'Tag', 'Uhrzeit', 'Monat Tag','Erneuerbar', 'Anteil Erneuerbar [%]','Total', 'Kernenergie'])
    df = df[['Datum von', 'Datum bis','Biomasse', 'Wasserkraft', 'Wind Offshore', 'Wind Onshore','Photovoltaik', 'Sonstige Erneuerbare', 'Pumpspeicher', 'Braunkohle', 'Steinkohle', 'Erdgas','Sonstige Konventionelle']]
    return df

def fixDataFrame2(df: pd.DataFrame) -> pd.DataFrame:
    df['Datum von'] = pd.to_datetime(df['Jahr'].astype(str) + '-' +
                                      df['Monat'].astype(str).str.zfill(2) + '-' +
                                      df['Tag'].astype(str).str.zfill(2) + ' ' +
                                      df['Uhrzeit'].astype(str), format='%Y-%m-%d %H:%M:%S')

    df['Datum bis'] = df['Datum von'] + pd.Timedelta(minutes=15)
    df = df.drop(columns=['Jahr', 'Monat', 'Tag', 'Uhrzeit', 'Monat Tag', 'Residuallast', 'Pumpspeicher'])
    df = df[['Datum von', 'Datum bis','Gesamt']]
    return df