import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd


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

def plotHistogramPercent(df, filename: str):
    path = "../output/" + filename + ".png"
    df['Anteil Erneuerbar [%]'] = df['Anteil Erneuerbar [%]'].clip(upper=115)
    # Histogram erstellen und die x-Achse als Prozentwerte anzeigen
    plt.figure(figsize=(10, 6))
    plt.hist(df['Anteil Erneuerbar [%]'], bins=[0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115], color='skyblue', edgecolor='black')
    plt.xlabel('Anteil Erneuerbar [%]')
    plt.ylabel('Anzahl an Viertelstunden')
    plt.title(filename)
    plt.tight_layout()
    # Speichern und anzeigen
    plt.savefig(path, format='png', dpi=300)
    #plt.show()

#plots collumnchart of renewable energyproducers
def plot_balk_rene(df, filename: str):
    path = "../output/" + filename + ".png"
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
def plot_pie_rene(df, filename: str):
    path = "../output/" + filename + ".png"
    erzeuger_spalten = ['Biomasse', 'Wasserkraft', 'Wind Offshore', 'Wind Onshore', 'Photovoltaik', 'Sonstige Erneuerbare']
    data = df[erzeuger_spalten].sum() / 1e+6
    labels = [f'{name} ({value:.2f} TWh)' for name, value in zip(erzeuger_spalten, data)]
    plt.figure(figsize=(10,6))
    plt.tight_layout()
    plt.pie(data, labels=labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.tab20.colors)
    plt.title(filename, fontsize=14)
    plt.savefig(path, format='png', dpi=300)

#plots piechart of conventionals
def plot_pie_conv(df, filename: str):
    path = "../output/" + filename + ".png"
    konventionelle_spalten = ['Braunkohle', 'Steinkohle', 'Erdgas', 'Sonstige Konventionelle']
    data = df[konventionelle_spalten].sum() / 1e+6
    labels = [f'{name} ({value:.2f} TWh)' for name, value in zip(konventionelle_spalten, data)]
    plt.tight_layout()
    plt.figure(figsize=(10, 6))
    plt.pie(data, labels=labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.tab20.colors)
    plt.title(filename, fontsize=14)
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
    weekly_df = df.groupby(df['Datum von'].dt.to_period('D')).agg({
        'Verbrauch': 'sum',
        'Biomasse': 'sum',
        'Wasserkraft': 'sum',
        'Wind Offshore': 'sum',
        'Wind Onshore': 'sum',
        'Photovoltaik': 'sum',
        'Sonstige Erneuerbare': 'sum',
        'Pumpspeicher Produktion': 'sum',
        'Batteriespeicher Produktion': 'sum',
        'Batteriespeicher': 'mean',
        'Pumpspeicher': 'mean'
    }).reset_index()

    # Produktion und Speicher berechnen
    weekly_df['Produktion'] = weekly_df[['Biomasse', 'Wasserkraft', 'Wind Offshore', 'Wind Onshore',
                                         'Photovoltaik', 'Sonstige Erneuerbare', 'Pumpspeicher Produktion',
                                         'Batteriespeicher Produktion']].sum(axis=1)
    weekly_df['Speicher'] = weekly_df[['Batteriespeicher', 'Pumpspeicher']].sum(axis=1)

    # Daten extrahieren
    time = weekly_df['Datum von'].dt.start_time
    consumption = weekly_df['Verbrauch']
    production = weekly_df['Produktion']
    storage = weekly_df['Speicher']

    # Diagramm erstellen
    plt.figure(figsize=(12, 6))

    # Verbrauch, Produktion und Speicher plotten
    plt.plot(time, consumption, label='Stromverbrauch', color='blue', linewidth=2)
    plt.plot(time, production, label='Stromproduktion', color='green', linewidth=2)
    plt.plot(time, storage, label='Speicher', color='orange', linewidth=2)

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


def aggregate_and_plot(dataframes: list[pd.DataFrame]):
    column_to_sum = input("Welche Spalte soll summiert werden? Bitte Spaltennamen eingeben: ")
    path = f"../output/{column_to_sum}_im_Vergleich_zum_Verbrauch.png"
    
    sums = []
    sums2 = []
    percentages = []
    years = []

    for df in dataframes:
        if column_to_sum == 'Wind':
            total_column = df['Wind Onshore'].sum().sum() / 1e6 + df['Wind Offshore'].sum().sum() / 1e6  # in TWh
        elif column_to_sum == 'Speicher':
            total_column = df['Pumpspeicher Produktion'].sum().sum() / 1e6 + df['Batteriespeicher Produktion'].sum().sum() / 1e6
        else:
            total_column = df[column_to_sum].sum().sum() / 1e6  # in TWh
        total_consumption = df['Verbrauch'].sum().sum() / 1e6  # in TWh
        
        sums.append(total_column)
        sums2.append(total_consumption)
        percentages.append((total_column / total_consumption) * 100)  # Prozentualer Anteil
        years.append(int(df['Datum von'].dt.year.iloc[0]))
    
    fig, ax1 = plt.subplots(figsize=(12, 8))

    # Erste Y-Achse für TWh-Werte
    ax1.plot(years, sums, label=f'{column_to_sum} (TWh)', color='green', marker='o')
    ax1.plot(years, sums2, label='Verbrauch (TWh)', color='blue', marker='o')
    
    ax1.set_xlabel('Jahr')
    ax1.set_ylabel('Energie (TWh)')
    ax1.set_xticks(years)
    ax1.set_xticklabels(years, rotation=45)
    
    ax1.set_title(f'Erzeugung von "{column_to_sum}" nach Jahr im Vergleich zum Verbrauch')
    ax1.legend(loc='upper left', fontsize=12)

    # Text für TWh-Werte an den Punkten
    for i, year in enumerate(years):
        ax1.text(year, sums[i], f'{sums[i]:.2f}', color='green', fontsize=10, ha='center', va='bottom')
        ax1.text(year, sums2[i], f'{sums2[i]:.2f}', color='blue', fontsize=10, ha='center', va='top')

    # Zweite Y-Achse für den Prozentanteil
    ax2 = ax1.twinx()
    ax2.plot(years, percentages, label=f'Anteil {column_to_sum} am Verbrauch (%)', color='orange', marker='o', linestyle='--')
    ax2.set_ylabel('Anteil (%)')
    ax2.set_ylim(0, 100)

    # Text für Prozentsätze an den Punkten
    for i, year in enumerate(years):
        ax2.text(year, percentages[i], f'{percentages[i]:.2f}%', color='orange', fontsize=10, ha='center', va='bottom')

    # Kombinierte Legende
    ax2.legend(loc='upper right', fontsize=12)

    plt.tight_layout()
    plt.savefig(path, format='png', dpi=300)
    plt.show()