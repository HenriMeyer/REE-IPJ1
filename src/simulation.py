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


def simulation(df: pd.DataFrame) -> pd.DataFrame:
    df = fixDataFrame(df)
    startYear = int(df['Datum von'].dt.year.iloc[0])
    while True:
        generationYear = input("Year for forecast: ")
        if generationYear.isdigit() and int(generationYear) > startYear:
                break
        else:
            print(f"{'\033[31m'}{generationYear} is an invalid input, it has to be bigger than {startYear} and a digit!{'\033[0m'}")
    for key in generation:
        while True:
            try:
                generation[key] = float(input(f"Value for {key}: "))
                break
            except ValueError:
                print("\033[31mInvalid input! Please enter a numeric value.\033[0m")
    resultFrames = []
    current_df = df.copy()
    print(current_df['Datum von'].astype)
    current_df['Datum von'] = current_df['Datum von'].dt.strftime('%d.%m.%Y %H:%M:%S')
    current_df['Datum bis'] = current_df['Datum bis'].dt.strftime('%d.%m.%Y %H:%M:%S')
    print(current_df['Datum von'].astype)
    for currentYear in range(startYear + 1, int(generationYear) + 1):
        print(currentYear)
        current_df['Datum von'] = current_df['Datum von'].apply(lambda x: x.replace(str(currentYear - 1),str(currentYear)))
        current_df['Datum bis'] = current_df['Datum bis'].apply(lambda x: x.replace(str(currentYear - 1),str(currentYear)))
        if f"31.12.{currentYear} 23:45:00" in current_df['Datum von']:
            current_df['Datum bis'] = current_df['Datum bis'].apply(lambda x: x.replace(str(currentYear - 1),str(currentYear + 1)))
        for column in df.columns:
            if column in ['Datum von', 'Datum bis']:
                continue
            if column in generation:
                current_df[column] = round(df[column] * (((generation[column] / df[column].sum() - 1) / (int(generationYear) - startYear)) * (currentYear - startYear) + 1), 2)
            else:
                print(column + " wasn't simulated.")
        time_df = current_df.copy()
        resultFrames.append(time_df.copy())
    
    return pd.concat(resultFrames, ignore_index=True)


def fixDataFrame(df: pd.DataFrame) -> pd.DataFrame:
    df['Datum von'] = pd.to_datetime(df['Jahr'].astype(str) + '-' +
                                      df['Monat'].astype(str).str.zfill(2) + '-' +
                                      df['Tag'].astype(str).str.zfill(2) + ' ' +
                                      df['Uhrzeit'].astype(str), format='%Y-%m-%d %H:%M:%S')

    df['Datum bis'] = df['Datum von'] + pd.Timedelta(minutes=15)

    df = df.drop(columns=['Jahr', 'Monat', 'Tag', 'Uhrzeit', 'Monat Tag','Erneuerbar', 'Anteil Erneuerbar [%]','Total', 'Kernenergie'])
    df = df[['Datum von', 'Datum bis','Biomasse', 'Wasserkraft', 'Wind Offshore', 'Wind Onshore','Photovoltaik', 'Sonstige Erneuerbare', 'Pumpspeicher', 'Braunkohle', 'Steinkohle', 'Erdgas','Sonstige Konventionelle']]
    return df
