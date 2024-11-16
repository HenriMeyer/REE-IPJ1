import pandas as pd

# Biomasse [MWh] Originalauflösungen;Wasserkraft [MWh] Originalauflösungen;Wind Offshore [MWh] Originalauflösungen;Wind Onshore [MWh] Originalauflösungen;Photovoltaik [MWh] Originalauflösungen;Sonstige Erneuerbare [MWh] Originalauflösungen;Kernenergie [MWh] Originalauflösungen;Braunkohle [MWh] Originalauflösungen;Steinkohle [MWh] Originalauflösungen;Erdgas [MWh] Originalauflösungen;Pumpspeicher [MWh] Originalauflösungen;Sonstige Konventionelle [MWh] Originalauflösungen
# data = [Biomasse, Wasserkraft, Wind Offshore, Wind Onshore, Photovoltaik, Sonstige Erneuerbare, 
# Kernenergie, Braunkohle, Steinkohle, Erdgas, Pumpspeicher, sonstige Konventionelle]

prognose = {
    'Biomasse': 1340000.0, 
    'Wasserkraft': 890000.0, 
    'Wind Offshore': 1770000.0, 
    'Wind Onshore': 1230000.0, 
    'Photovoltaik': 950000.0, 
    'Sonstige Erneuerbare': 1520000.0, 
    'Kernenergie': 1080000.0, 
    'Braunkohle': 670000.0, 
    'Steinkohle': 1450000.0, 
    'Erdgas': 880000.0, 
    'Pumpspeicher': 1910000.0, 
    'sonstige Konventionelle': 1110000.0
}

def simulation(df: pd.DataFrame) -> pd.DataFrame:
    currentYear = 2024
    while True:
        prognosedYear = input("Year for prognose: ")
        if prognosedYear.isdigit() and int(prognosedYear) > currentYear:
                break
        else:
            print("{'\033[31m'}Invalid input!{'\033[30m'}")
    for key in prognose:
        while True:
            try:
                prognose[key] = float(input(f"Value for {key}: "))
                break
            except ValueError:
                print("\033[31mInvalid input! Please enter a numeric value.\033[0m")
    resultFrames = []
    current_df = df.copy()
    for currentYear in range(df.loc[0,"Jahr"], int(prognosedYear)):
        current_df['Jahr'] = currentYear
        for column in df.columns:
            if column in prognose:
                current_df[column] = df[column] * (prognose[column] * int(prognosedYear)) / (df[column].sum() * currentYear)
            else:
                print(column + " wasn't simulated.")
        resultFrames.append(current_df.copy())
    
    return pd.concat(resultFrames, ignore_index=True)