import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


#df: data, 
# title: headline, 
# colName: name of column with to be displayed data,
# indexY: Time on Y-axis
# indexX: Time on X-axis

def plotHeatmap(df, title, colName, indexY, indexX, filename: str):
    
    path = "../data/" + filename + ".png"
    heatmap_data = df.pivot_table(index = indexY, columns = indexX , values=colName, aggfunc=np.mean) # Leistungsmittelwerte!

    plt.figure(figsize=(20, 8))
    sns.heatmap(heatmap_data, cmap='coolwarm', annot=False, linewidths=.8, cbar=True, xticklabels=1)

    plt.title(title)
    plt.xlabel(indexX)
    plt.ylabel(indexY)
    plt.savefig(path, format='png', dpi=300, bbox_inches='tight')
    
    plt.show()  

def plotHistogramPercent(vec, filename: str):
    
    path = "../data/" + filename + ".png"
    x_labels = [f"{(i+1)*10}%" for i in range(10)]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(x_labels, vec[1:], color='skyblue')
    plt.xlabel('Anteil Erneuerbar [%]')
    plt.ylabel('Anzahl an Viertelstunden')
    plt.title('Histogramm der erneuerbaren Anteile ' + filename)

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 2, yval, ha='center', va='bottom')
    plt.savefig(path, format='png', dpi=300, bbox_inches='tight')
    
    plt.show()

def plotHistogramErzeuger(df, filename: str):

    path = "../data/" + filename + ".png"
    erzeuger_spalten = [
        'Biomasse', 'Wasserkraft', 'Wind Offshore', 'Wind Onshore',
        'Photovoltaik', 'Sonstige Erneuerbare', 'Pumpspeicher'
    ]
    

    summen = df[erzeuger_spalten].sum()/(1e+6)
    

    plt.figure(figsize=(10, 6))
    summen.plot(kind='bar', color='skyblue')
    plt.title(filename)
    plt.ylabel('Energie in TWh')
    plt.xlabel('Erzeuger')
    plt.xticks(rotation=10)

    for i, value in enumerate(summen):
        plt.text(i, value + 1, f'{value:.2f}TWh', ha='center', va='bottom')

    plt.savefig(path, format='png', dpi=300, bbox_inches='tight')
    plt.show()

def plotPiePercent(vec, filename: str):

    path = "../data/" + filename + ".png"
    labels = [f"{i}/{10} EEs" if vec[i] > 0 else "" for i in range(len(vec))]

    def func(pct):
        if pct > 0:
            return f'{pct:.0f}%'
        return ''
    
    plt.figure(figsize=(8, 8))
    plt.pie(vec, labels = labels, autopct=lambda pct: func(pct), startangle=90, colors=plt.cm.Paired.colors, wedgeprops={'width': 0.3}, pctdistance=0.85)
    plt.title('Anzahl von Viertelstunden mit [%] Anteil von Erneuerbaren')
    plt.savefig(path, format='png', dpi=300, bbox_inches='tight')
    
    plt.show()

def plot_pie_chart(df, filename: str):
    path = "../data/" + filename + ".png"

    erneuerbare_spalten = ['Biomasse', 'Wasserkraft', 'Wind Offshore', 'Wind Onshore', 'Photovoltaik', 'Sonstige Erneuerbare']
    konventionelle_spalten = ['Pumpspeicher', 'Kernenergie', 'Braunkohle', 'Steinkohle', 'Erdgas', 'Sonstige Konventionelle']
    
    erneuerbare_summe = df[erneuerbare_spalten].sum().sum()/(1e+6)
    konventionelle_summe = df[konventionelle_spalten].sum().sum()/(1e+6)

    labels = [f'Erneuerbare Energie {erneuerbare_summe:.2f} GWh', f'Konventionelle Energie {konventionelle_summe:.2f} GWh']
    values = [erneuerbare_summe, konventionelle_summe]

    plt.figure(figsize=(6, 6))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.title(filename)
    plt.savefig(path, format='png', dpi=300, bbox_inches='tight')

    plt.show()