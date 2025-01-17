import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import os

def visualize(simulationDict: dict[str, list]):
    key = str(next(iter(simulationDict)))
    keyStr = str(key)
    dfList = list(simulationDict[key])

    folder = "../output/" + keyStr + "/PNG"
    if not os.path.exists(folder):
        os.makedirs(folder)


    visualizationYear = '2030'

    for df in dfList:
        if int(visualizationYear) == int(df['Datum von'].dt.year.iloc[0]):
            dfv = df
  


    plotHistogramPercent(dfv, folder , 'Histogramm Abdeckung der Viertelstunden ' + visualizationYear)
    plot_pie_rene(dfv, folder ,'Anteilige Erzeugung Erneuerbarer '+ visualizationYear)
    plot_pie_conv(dfv, folder ,'Stromzusammensetzung '+ visualizationYear)
    # #graphics.plotHeatmap(dfv , 'Ungenutzte Energie', 'Monat', 'Tag', 'Heatmap')
    plot_energy_data_from_df(dfv, folder + '/Stromverbrauch und Produktion '+ visualizationYear)
    plot_energy_data_from_df_original(dfv, folder + '/Stromverbrauch und Produktion Zoom in schlechtesten Tag '+ visualizationYear)
    # clearScreen()

    #Entwicklung über die Jahre
    aggregate_and_plot(dfList, folder)

def visualize_multiple(simulationDict: dict[str, list]):
    folder = "../output/combined/PNG"
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    columns = [
        'Biomasse', 'Wasserkraft', 'Wind Offshore', 'Wind Onshore',
        'Photovoltaik', 'Sonstige Erneuerbare', 'Pumpspeicher Produktion',
        'Batteriespeicher Produktion',
        'Sonstige Konventionelle','Wärmepumpe','E-Auto', 'E-LKW', 'Verbrauch', 'Konventionell', 'Price'
    ]
    combined_yearly_sums = {column: {} for column in columns}
    
    for scenario, df_list in simulationDict.items():
        for column in columns:
            for df in df_list:
                year = df['Datum von'].dt.year.iloc[0]
                if year not in combined_yearly_sums[column]:
                    combined_yearly_sums[column][year] = {}
                if scenario not in combined_yearly_sums[column][year]:
                    combined_yearly_sums[column][year][scenario] = 0
                combined_yearly_sums[column][year][scenario] = df[column].sum()/1e6
    
    for column in columns:
        if column == 'Price':
            plot_combined_yearly_price(combined_yearly_sums[column], folder, column)
            plot_combined_price_kWh(combined_yearly_sums, folder)
            continue
        elif column in ['Wind Offshore', 'Wind Onshore',
        'Photovoltaik',  'Verbrauch', 'Konventionell']:
            plot_combined_yearly_sums(combined_yearly_sums[column], folder, column)
    plot_combined_percentrenewable(combined_yearly_sums, folder)

def plot_combined_percentrenewable(combined_yearly_sums, folder):
    year = 2030
    scenarios = sorted(combined_yearly_sums['Verbrauch'][year].keys())
    
    results_used = {}
    results_produced = {}
    results_storage = {}
    
    for scenario in scenarios:
        verbrauch = combined_yearly_sums['Verbrauch'][year][scenario] * 1e9
        erneuerbar = (combined_yearly_sums['Verbrauch'][year][scenario] -
                      combined_yearly_sums['Konventionell'][year][scenario]) * 1e9
        gesamt = (combined_yearly_sums['Photovoltaik'][year][scenario] +
                  combined_yearly_sums['Wind Onshore'][year][scenario] +
                  combined_yearly_sums['Wind Offshore'][year][scenario] +
                  combined_yearly_sums['Biomasse'][year][scenario] +
                  combined_yearly_sums['Wasserkraft'][year][scenario] +
                  combined_yearly_sums['Sonstige Erneuerbare'][year][scenario]) * 1e9
        speicher = (combined_yearly_sums['Pumpspeicher Produktion'][year][scenario] +
                    combined_yearly_sums['Batteriespeicher Produktion'][year][scenario]) * 1e9
        
        results_used[scenario] = erneuerbar / verbrauch
        results_produced[scenario] = gesamt / verbrauch
        results_storage[scenario] = speicher / verbrauch

    x = np.arange(len(scenarios))
    width = 0.25

    _, ax = plt.subplots(figsize=(12, 8))
    bars1 = ax.bar(x - width, results_used.values(), width, label='Genutzte Erneuerbare')
    bars2 = ax.bar(x, results_produced.values(), width, label='Erneuerbar Produziert')
    bars3 = ax.bar(x + width, results_storage.values(), width, label='Gespeicherte Energie')

    ax.set_xlabel('Szenario')
    ax.set_ylabel('Anteil am Verbrauch')
    ax.set_title('Anteil der genutzten, produzierten und gespeicherten Energie zum Verbrauch für 2030')
    ax.set_xticks(x)
    ax.set_xticklabels(scenarios, rotation=45)
    ax.legend()

    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.2f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')

    plt.tight_layout()
    path = os.path.join(folder, 'Anteil der genutzten und produzierten Energie 2030.png')
    plt.savefig(path, format='png', dpi=300)
    plt.close()

def plot_combined_price_kWh(combined_yearly_sums, folder):
    year = 2030
    scenarios = sorted(combined_yearly_sums['Verbrauch'][year].keys())
    
    results = {}
    for scenario in scenarios:
        verbrauch = combined_yearly_sums['Verbrauch'][year][scenario]*1e9
        konventionell = combined_yearly_sums['Konventionell'][year][scenario]*1e9
        gesamtpreis = combined_yearly_sums['Price'][year][scenario]*1e6
        results[scenario] = gesamtpreis/ (verbrauch - konventionell)

    for i, (scenario, value) in enumerate(results.items()):
        plt.text(i, value, f'{value:.2f}', ha='center', va='bottom')

    plt.figure(figsize=(12, 8))
    plt.bar(results.keys(), results.values(), color='skyblue')
    plt.xlabel('Szenario')
    plt.ylabel('€/kWh')
    plt.title('Preis pro kWh in € für 2030')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    path = os.path.join(folder, 'Preis pro kWh in 2030.png')
    plt.savefig(path, format='png', dpi=300)
    plt.close()


def plot_combined_yearly_sums(combined_yearly_sums, folder, column):
    years = sorted(combined_yearly_sums.keys())
    scenarios = sorted(next(iter(combined_yearly_sums.values())).keys())
    
    plt.figure(figsize=(12, 8))
    
    for scenario in scenarios:
        sums = [combined_yearly_sums[year].get(scenario, 0) for year in years]
        plt.plot(years, sums, marker='o', linestyle='-', label=scenario)
    
    plt.xlabel('Year')
    plt.ylabel(f'Summe von {column} in TWh')
    plt.title(f'Jährliche Summen {column}')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    path = os.path.join(folder, f'{column}_summe_jährlich.png')
    plt.savefig(path, format='png', dpi=300)
    plt.close()

def plot_combined_yearly_price(combined_yearly_sums, folder, column):
    years = sorted(combined_yearly_sums.keys())
    scenarios = sorted(next(iter(combined_yearly_sums.values())).keys())
    
    plt.figure(figsize=(12, 8))
    
    for scenario in scenarios:
        sums = [combined_yearly_sums[year].get(scenario, 0)/1e3 for year in years]
        plt.plot(years, sums, marker='o', linestyle='-', label=scenario)
    
    plt.xlabel('Year')
    plt.ylabel(f'Gesamtkosten in Milliarden €')
    plt.title(f'Gesamtkosten')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    path = os.path.join(folder, f'{column}_summe_jährlich.png')
    plt.savefig(path, format='png', dpi=300)
    plt.close()
    
#functions for plotting


#df: data, 
# title: headline, 
# colName: name of column with to be displayed data,
# indexY: Time on Y-axis
# indexX: Time on X-axis
def plotHeatmap(df: pd.DataFrame , colName, indexY, indexX, filename: str):
    
    print(df)
    
    path = "../output/" + filename + ".png"
    heatmap_data = df.pivot_table(index = indexY, columns = indexX , values=colName, aggfunc=np.mean) # Leistungsmittelwerte!

    plt.figure(figsize=(20, 8))
    sns.heatmap(heatmap_data, cmap='coolwarm', annot=False, linewidths=.8, cbar=True, xticklabels=1)

    plt.title(filename)
    plt.xlabel(indexX)
    plt.ylabel(indexY)
    plt.tight_layout()
    plt.savefig(path, format='png', dpi=300)
    
    #plt.show()  

def plotHistogramPercent(df,folder, filename: str):
    path = folder + "/" + filename
    df['Anteil Erneuerbar [%]'] = df['Anteil Erneuerbar [%]'].clip(upper=100)
    df['Anteil Erneuerbar [%] ohne Speicher'] = df['Anteil Erneuerbar [%] ohne Speicher'].clip(upper=100)
    plt.figure(figsize=(10, 6))
    counts, bins, patches = plt.hist(df['Anteil Erneuerbar [%]'], bins=[0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100], 
                                     color='skyblue', edgecolor='black', cumulative=-1)
    plt.xlabel('Anteil Erneuerbar [%]')
    plt.ylabel('Anzahl an Viertelstunden')
    plt.title(filename)
    plt.tight_layout()
    
    for count, patch in zip(counts, patches):
        height = patch.get_height()
        plt.text(patch.get_x() + patch.get_width() / 2, height, int(height), ha='center', va='bottom')
    
    plt.savefig(path+ ".png", format='png', dpi=300)

    plt.figure(figsize=(10, 6))
    counts, bins, patches = plt.hist(df['Anteil Erneuerbar [%] ohne Speicher'], bins=[0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100], 
                                     color='skyblue', edgecolor='black', cumulative=-1)
    plt.xlabel('Anteil Erneuerbar [%] ohne Speicher')
    plt.ylabel('Anzahl an Viertelstunden')
    plt.title(filename + " ohne Speicher")
    plt.tight_layout()
    
    for count, patch in zip(counts, patches):
        height = patch.get_height()
        plt.text(patch.get_x() + patch.get_width() / 2, height, int(height), ha='center', va='bottom')
    
    plt.savefig(path + " ohne Speicher" + ".png", format='png', dpi=300)

#plots collumnchart of renewable energyproducers
def plot_balk_rene(df, folder, filename: str):
    path = folder + "/" + filename + ".png"
    erzeuger_spalten = [
        'Biomasse', 'Wasserkraft', 'Wind Offshore', 'Wind Onshore',
        'Photovoltaik', 'Sonstige Erneuerbare'
    ]
    summen = df[erzeuger_spalten].sum()/(1e+6)
    ylabel = 'Energie in TWh'
    xlabel = 'Erzeuger'
    plt.tight_layout()
    plotBalken(summen, ylabel, xlabel, filename)
    plt.savefig(path, format='png', dpi=300)


#plots columnchart of all energyproducers
def plot_balk_all(df, filename: str):
    path = "../output/" + filename + ".png"
    erzeuger_spalten = [
        'Biomasse', 'Wasserkraft', 'Wind Offshore', 
        'Wind Onshore', 'Photovoltaik', 'Sonstige Erneuerbare',
        'Braunkohle', 'Steinkohle', 'Erdgas', 
        'Pumpspeicher', 'Sonstige Konventionelle'
    ]
    summen = df[erzeuger_spalten].sum()/(1e+6)
    ylabel = 'Energieerzeugung in TWh'
    xlabel = 'Erzeuger'
    plt.tight_layout()
    plotBalken(summen, ylabel, xlabel, filename)
    plt.savefig(path, format='png', dpi=300)

#plots piechart of energyproduction
def plot_pie_prod(df, filename: str):
    path = "../output/" + filename + ".png"
    erneuerbare_spalten = ['Biomasse', 'Wasserkraft', 'Wind Offshore', 'Wind Onshore', 'Photovoltaik', 'Sonstige Erneuerbare']
    konventionelle_spalten = ['Braunkohle', 'Steinkohle', 'Erdgas', 'Sonstige Konventionelle']
    erneuerbare_summe = df[erneuerbare_spalten].sum().sum()/(1e+6)
    konventionelle_summe = df[konventionelle_spalten].sum().sum()/(1e+6)
    labels = [f'Erneuerbare Energie ({erneuerbare_summe:.2f} TWh)', f'Konventionelle Energie ({konventionelle_summe:.2f} TWh)']
    data = [erneuerbare_summe, konventionelle_summe]
    plt.tight_layout()
    plt.figure(figsize=(10, 6))
    plt.pie(data, labels=labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.tab20.colors)
    plt.title(filename, fontsize=14)
    plt.savefig(path, format='png', dpi=300)

#plots piechart of energyusage
def plot_pie_usage(df, df2, filename: str):
    path = "../output/" + filename + ".png"
    erneuerbare_summe = (df['Gesamt'].sum().sum()-df['Residuallast'].sum().sum())/(1e+6)
    erneuerbare_summe_res = (df2['Biomasse'].sum().sum()+ df2['Wasserkraft'].sum().sum() + df2['Sonstige Erneuerbare'].sum().sum())/(1e+6)
    konventionelle_summe = df['Residuallast'].sum().sum()/(1e+6)- erneuerbare_summe_res
    labels = [f'Photovoltaik und Windkraft ({erneuerbare_summe:.2f} TWh)', f'Biomasse, Wasserkraft, Sonst. EEs ({erneuerbare_summe_res:.2f} TWh)', f'Konventionelle Energie ({konventionelle_summe:.2f} TWh)']
    data = [erneuerbare_summe, erneuerbare_summe_res ,konventionelle_summe]
    plt.tight_layout()
    plot_pie(data, labels, filename)
    plt.savefig(path, format='png', dpi=300)

#plots piechart of renewables
def plot_pie_rene(df, folder, filename: str):
    path = folder + "/" + filename + ".png"
    erzeuger_spalten = ['Biomasse', 'Wasserkraft', 'Wind Offshore', 'Wind Onshore', 'Photovoltaik', 'Sonstige Erneuerbare']
    data = df[erzeuger_spalten].sum() / 1e+6
    labels = [f'{name} ({value:.2f} TWh)' for name, value in zip(erzeuger_spalten, data)]
    plt.figure(figsize=(10,6))
    plt.tight_layout()
    plt.pie(data, labels=labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.tab20.colors)
    plt.title(filename, fontsize=14)
    plt.savefig(path, format='png', dpi=300)

#plots piechart of conventionals
def plot_pie_conv(df, folder, filename: str):
    path = folder + "/" + filename + ".png"
    speicher = (df['Pumpspeicher Produktion'].sum() + df['Batteriespeicher Produktion'].sum()) / 1e+6
    rene = (df['Verbrauch'].sum() - df['Konventionell'].sum()) / 1e+6 - speicher
    flexible_kraftwerk = df['Regelbare Kraftwerke'].sum() / 1e+6
    luecke = df['Lücke'].sum() / 1e+6

    data = [luecke, rene, speicher, flexible_kraftwerk]
    labels = [
        f'Lücke ({luecke:.2f} TWh)',
        f'Erneuerbar ({rene:.2f} TWh)',
        f'Speicher ({speicher:.2f} TWh)',
        f'Flexibles Kraftwerk ({flexible_kraftwerk:.2f} TWh)'
    ]
    colors = ['red', 'green', 'orange', 'blue']

    plt.figure(figsize=(10, 6))
    plt.pie(data, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
    plt.title(filename, fontsize=14)
    plt.tight_layout()
    plt.savefig(path, format='png', dpi=300)


#visualization of piecharts
def plot_pie(data, labels, filename: str):

    path = "../data/" + filename + ".png"

    plt.figure(figsize=(10, 6))
    plt.pie(
        data,
        labels=labels,
        autopct='%1.2f%%',
        startangle=90,
        colors=plt.cm.Paired.colors
    )
    plt.title(filename)
    plt.savefig(path, format='png', dpi=300)
    #plt.show()

#visualization of columncharts
def plotBalken(data, ylabel, xlabel, filename: str):

    path = "../data/" + filename + ".png"

    plt.figure(figsize=(10, 6))
    data.plot(kind='bar', color='skyblue')
    plt.title(filename)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.xticks(rotation=15)
    plt.tight_layout()
    for i, value in enumerate(data):
        plt.text(i, value + 1, f'{value:.2f}', ha='center', va='bottom')

    plt.savefig(path, format='png', dpi=300)
    #plt.show()

def plot_energy_data_from_df(df, filename):
    path = "../output/" + filename + ".png"
    df['Datum von'] = pd.to_datetime(df['Datum von'])

    # Gruppieren nach Woche und aufsummieren
    daily_df = df.groupby(df['Datum von'].dt.to_period('D')).agg({
        'Verbrauch': 'sum',
        'Biomasse': 'sum',
        'Wasserkraft': 'sum',
        'Wind Offshore': 'sum',
        'Wind Onshore': 'sum',
        'Photovoltaik': 'sum',
        'Sonstige Erneuerbare': 'sum',
        'Pumpspeicher Produktion': 'sum',
        'Batteriespeicher Produktion': 'sum',
        'Konventionell': 'sum'
    }).reset_index()

    # Produktion und Speicher berechnen
    daily_df['Produktion'] = daily_df[['Biomasse', 'Wasserkraft', 'Wind Offshore', 'Wind Onshore',
                                         'Photovoltaik', 'Sonstige Erneuerbare']].sum(axis=1)
    daily_df['Speicher'] = daily_df[['Batteriespeicher Produktion', 'Pumpspeicher Produktion']].sum(axis=1)
    

    # Daten extrahieren
    time = daily_df['Datum von'].dt.start_time
    consumption = daily_df['Verbrauch']
    production = daily_df['Produktion']
    storage = daily_df['Speicher']
    conventionell = daily_df['Konventionell']

    # Diagramm erstellen
    plt.figure(figsize=(12, 6))

    # Verbrauch, Produktion und Speicher plotten
    plt.plot(time, consumption, label='Stromverbrauch', color='blue', linewidth=2)
    plt.plot(time, production, label='Stromproduktion', color='green', linewidth=2)
    plt.plot(time, storage, label='Speicher', color='orange', linewidth=2)
    plt.plot(time, conventionell, label='Konventionell', color='black', linewidth=2)

    # Titel und Achsenbeschriftungen
    plt.title('Zeitlicher Verlauf von Stromverbrauch, Produktion und Speicher', fontsize=16)
    plt.xlabel('Zeit', fontsize=14)
    plt.ylabel('Energie (MWh)', fontsize=14)
    plt.tight_layout()
    # Gitter und Legende
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(fontsize=12)
    plt.savefig(path, format='png', dpi=300)
    # Layout optimieren und anzeigen
    #plt.show()



def plot_energy_data_from_df_original(df, filename):
    path = "../output/" + filename + ".png"
    df['Datum von'] = pd.to_datetime(df['Datum von'])

    max_gap_index = df['Lücke'].idxmax()

    start_index = max(0, max_gap_index - 67)
    end_index = min(len(df), max_gap_index + 67)
    df = df.iloc[start_index:end_index]

    time = df['Datum von']
    consumption = df['Verbrauch']
    production = df[['Biomasse', 'Wasserkraft', 'Wind Offshore', 'Wind Onshore',
                     'Photovoltaik', 'Sonstige Erneuerbare']].sum(axis=1)
    storage = -df[['Batteriespeicher', 'Pumpspeicher']].sum(axis=1)
    gap = df['Lücke']
    controllable = df['Regelbare Kraftwerke']
    gap = gap.add(controllable, fill_value=0)

    plt.figure(figsize=(12, 6))

    plt.plot(time, consumption, label='Stromverbrauch', color='blue', linewidth=2)
    plt.plot(time, production, label='Stromproduktion', color='green', linewidth=2)
    plt.plot(time, storage, label='Speicher', color='orange', linewidth=2)
    plt.plot(time, gap, label='Lücke', color='red', linewidth=2)
    plt.plot(time, controllable, label='Regelbare Kraftwerke', color='purple', linewidth=2)

    # Titel und Achsenbeschriftungen
    plt.title('Zeitlicher Verlauf von Stromverbrauch, Produktion, Speicher, Lücke und Regelbare Kraftwerke', fontsize=16)
    plt.xlabel('Zeit', fontsize=14)
    plt.ylabel('Energie (MWh)', fontsize=14)
    plt.tight_layout()
    # Gitter und Legende
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(fontsize=12)
    plt.savefig(path, format='png', dpi=300)
    # Layout optimieren und anzeigen
    #plt.show()

def aggregate_and_plot(dataframes: list[pd.DataFrame], folder: str):
    # Eingabe: Auswahl der darzustellenden Spalten
    available_columns = [
        'Verbrauch', 'Biomasse', 'Wasserkraft', 'Wind Offshore', 'Wind Onshore', 'Photovoltaik',
        'Pumpspeicher Produktion', 'Batteriespeicher Produktion', 'Konventionell', 'Ungenutzte Energie',
        'Wärmepumpe','E-Auto', 'E-LKW', 'Speicher', 'Erneuerbare'
    ]
    print("Verfügbare Spalten:\n", ", ".join(available_columns))
    selected_columns = input("Welche Spalten möchten Sie darstellen? Geben Sie die Namen durch Komma getrennt ein: ").split(',')
    selected_columns = [col.strip() for col in selected_columns if col.strip() in available_columns]

    if not selected_columns:
        print("Keine gültigen Spalten ausgewählt. Abbruch.")
        return

    path = f"{folder}/{selected_columns}im Vergleich.png"
    years = []
    aggregated_data = {col: [] for col in selected_columns}

    for df in dataframes:
        # Jahr extrahieren
        years.append(int(df['Datum von'].dt.year.iloc[0]))

        # Daten aggregieren
        for col in selected_columns:
            total_value = df[col].sum() / 1e6  # in TWh
            aggregated_data[col].append(total_value)

    # Plot erstellen
    _, ax1 = plt.subplots(figsize=(14, 8))

    # Ausgewählte Spalten plotten
    colors = ['blue', 'green', 'orange', 'black', 'red', 'purple', 'brown', 'pink', 'cyan', 'gray']
    for i, (col, values) in enumerate(aggregated_data.items()):
        ax1.plot(years, values, label=f'{col} (TWh)', color=colors[i % len(colors)], marker='o', linewidth=2)

        # Werte an den Punkten darstellen
        for j, year in enumerate(years):
            ax1.text(year, values[j], f'{values[j]:.2f}', color=colors[i % len(colors)], fontsize=10, ha='center', va='bottom')

    # Achsenbeschriftungen und Titel
    ax1.set_xlabel('Jahr', fontsize=14)
    ax1.set_ylabel('Energie (TWh)', fontsize=14)
    ax1.set_xticks(years)
    ax1.set_xticklabels(years, rotation=45)
    ax1.set_title('Jährliche Stromerzeugung im Vergleich zum Verbrauch', fontsize=16)

    # Legende und Gitter
    ax1.legend(loc='upper left', fontsize=12)
    ax1.grid(True, linestyle='--', alpha=0.6)

    # Speicher für das Diagramm
    plt.tight_layout()
    plt.savefig(path, format='png', dpi=300)
    plt.close()

    # Balkendiagramm für 2030
    if 2030 in years:
        index_2030 = years.index(2030)
        values_2030 = {col: aggregated_data[col][index_2030] for col in selected_columns}

        plt.figure(figsize=(12, 8))
        plt.bar(values_2030.keys(), values_2030.values(), color='skyblue')
        plt.xlabel('Kategorie', fontsize=14)
        plt.ylabel('Energie (TWh)', fontsize=14)
        plt.title('Stromerzeugung und Verbrauch für 2030', fontsize=16)
        plt.xticks(rotation=45)

        for i, (col, value) in enumerate(values_2030.items()):
            plt.text(i, value, f'{value:.2f}', ha='center', va='bottom')

        plt.tight_layout()
        path_2030 = f"{folder}/Stromerzeugung und Verbrauch für 2030.png"
        plt.savefig(path_2030, format='png', dpi=300)
        plt.close()