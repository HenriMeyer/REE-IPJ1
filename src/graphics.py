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
    
    path = "../Output/" + filename + ".png"
    heatmap_data = df.pivot_table(index = indexY, columns = indexX , values=colName, aggfunc=np.mean) # Leistungsmittelwerte!

    plt.figure(figsize=(20, 8))
    sns.heatmap(heatmap_data, cmap='coolwarm', annot=False, linewidths=.8, cbar=True, xticklabels=1)

    plt.title(filename)
    plt.xlabel(indexX)
    plt.ylabel(indexY)
    plt.savefig(path, format='png', dpi=300)
    
    plt.show()  

def plotHistogramPercent(df, filename: str):
    path = "../Output/" + filename + ".png"

    # Histogram erstellen und die x-Achse als Prozentwerte anzeigen
    plt.figure(figsize=(10, 6))
    plt.hist(df['Anteil Erneuerbar [%]'], bins=[0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115], color='skyblue', edgecolor='black')
    plt.xlabel('Anteil Erneuerbar [%]')
    plt.ylabel('Anzahl an Viertelstunden')
    plt.title(filename)

    # Speichern und anzeigen
    plt.savefig(path, format='png', dpi=300)
    plt.show()

#plots collumnchart of renewable energyproducers
def plot_balk_rene(df, filename: str):

    erzeuger_spalten = [
        'Biomasse', 'Wasserkraft', 'Wind Offshore', 'Wind Onshore',
        'Photovoltaik', 'Sonstige Erneuerbare'
    ]
    summen = df[erzeuger_spalten].sum()/(1e+6)
    ylabel = 'Energie in TWh'
    xlabel = 'Erzeuger'
    plotBalken(summen, ylabel, xlabel, filename)


#plots columnchart of all energyproducers
def plot_balk_all(df, filename: str):
    erzeuger_spalten = [
        'Biomasse', 'Wasserkraft', 'Wind Offshore', 
        'Wind Onshore', 'Photovoltaik', 'Sonstige Erneuerbare',
        'Braunkohle', 'Steinkohle', 'Erdgas', 
        'Pumpspeicher', 'Sonstige Konventionelle'
    ]
    summen = df[erzeuger_spalten].sum()/(1e+6)
    ylabel = 'Energieerzeugung in TWh'
    xlabel = 'Erzeuger'
    plotBalken(summen, ylabel, xlabel, filename)

#plots piechart of energyproduction
def plot_pie_prod(df, filename: str):

    erneuerbare_spalten = ['Biomasse', 'Wasserkraft', 'Wind Offshore', 'Wind Onshore', 'Photovoltaik', 'Sonstige Erneuerbare']
    konventionelle_spalten = ['Braunkohle', 'Steinkohle', 'Erdgas', 'Sonstige Konventionelle']
    erneuerbare_summe = df[erneuerbare_spalten].sum().sum()/(1e+6)
    konventionelle_summe = df[konventionelle_spalten].sum().sum()/(1e+6)
    labels = [f'Erneuerbare Energie ({erneuerbare_summe:.2f} TWh)', f'Konventionelle Energie ({konventionelle_summe:.2f} TWh)']
    data = [erneuerbare_summe, konventionelle_summe]

    plot_pie(data, labels, filename)

#plots piechart of energyusage
def plot_pie_usage(df, df2, filename: str):
    
    erneuerbare_summe = (df['Gesamt'].sum().sum()-df['Residuallast'].sum().sum())/(1e+6)
    erneuerbare_summe_res = (df2['Biomasse'].sum().sum()+ df2['Wasserkraft'].sum().sum() + df2['Sonstige Erneuerbare'].sum().sum())/(1e+6)
    konventionelle_summe = df['Residuallast'].sum().sum()/(1e+6)- erneuerbare_summe_res
    labels = [f'Photovoltaik und Windkraft ({erneuerbare_summe:.2f} TWh)', f'Biomasse, Wasserkraft, Sonst. EEs ({erneuerbare_summe_res:.2f} TWh)', f'Konventionelle Energie ({konventionelle_summe:.2f} TWh)']
    data = [erneuerbare_summe, erneuerbare_summe_res ,konventionelle_summe]

    plot_pie(data, labels, filename)

#plots piechart of renewables
def plot_pie_rene(df, filename: str):

    erzeuger_spalten = ['Biomasse', 'Wasserkraft', 'Wind Offshore', 'Wind Onshore', 'Photovoltaik', 'Sonstige Erneuerbare']
    data = df[erzeuger_spalten].sum() / 1e+6
    labels = [f'{name} ({value:.2f} TWh)' for name, value in zip(erzeuger_spalten, data)]

    plot_pie(data, labels, filename)

#plots piechart of conventionals
def plot_pie_conv(df, filename: str):

    konventionelle_spalten = ['Braunkohle', 'Steinkohle', 'Erdgas', 'Sonstige Konventionelle']
    data = df[konventionelle_spalten].sum() / 1e+6
    labels = [f'{name} ({value:.2f} TWh)' for name, value in zip(konventionelle_spalten, data)]

    plot_pie(data, labels, filename)


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
    plt.show()

#visualization of columncharts
def plotBalken(data, ylabel, xlabel, filename: str):

    path = "../data/" + filename + ".png"

    plt.figure(figsize=(10, 6))
    data.plot(kind='bar', color='skyblue')
    plt.title(filename)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.xticks(rotation=15)

    for i, value in enumerate(data):
        plt.text(i, value + 1, f'{value:.2f}', ha='center', va='bottom')

    plt.savefig(path, format='png', dpi=300)
    plt.show()