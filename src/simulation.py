import pandas as pd

generation = {
    'Biomasse': None,
    'Wasserkraft': None,
    'Wind Offshore': None,
    'Wind Onshore': None,
    'Photovoltaik': None,
    'Sonstige Erneuerbare': None,
    'Kernenergie': None,
    'Braunkohle': None,
    'Steinkohle': None,
    'Erdgas': None,
    'Pumpspeicher': None,
    'sonstige Konventionelle': None
}

def simulation(df: pd.DataFrame) -> pd.DataFrame:
    while True:
        generationdYear = input("Year for forecast: ")
        if generationdYear.isdigit() and int(generationdYear) > df.loc[0,"Jahr"]:
                break
        else:
            print("{'\033[31m'}Invalid input!{'\033[30m'}")
    for key in generation:
        while True:
            try:
                generation[key] = float(input(f"Value for {key}: "))
                break
            except ValueError:
                print("\033[31mInvalid input! Please enter a numeric value.\033[0m")
    resultFrames = []
    current_df = df.copy()
    for currentYear in range(df.loc[0,"Jahr"] + 1, int(generationdYear) + 1):
        current_df['Jahr'] = currentYear
        for column in df.columns:
            if column in generation:
                current_df[column] = round(df[column] * (((generation[column] / df[column].sum() - 1) / (int(generationdYear) - df.loc[0,"Jahr"])) * (currentYear - df.loc[0, "Jahr"]) + 1), 2)
            else:
                print(column + " wasn't simulated.")
                # Hier sollte man einiges nicht berücksichtigen
        resultFrames.append(current_df.copy())
    
    return pd.concat(resultFrames, ignore_index=True)