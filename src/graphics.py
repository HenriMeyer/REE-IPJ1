import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


# df: data, 
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
    plt.title('Histogramm der erneuerbaren Anteile')

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 2, yval, ha='center', va='bottom')
    plt.savefig(path, format='png', dpi=300, bbox_inches='tight')
    
    plt.show()
    
def plotHistogramStorage(df, filename: str):
    # Datei-Pfad für das Speichern
    path = "../data/" + filename + ".png"
    
    # Berechnung der Summen der einzelnen Technologien in TWh
    storage_data = (df.loc[:, ['Pumpspeicher', 'Braunkohle', 'Steinkohle', 'Erdgas', 'Kernenergie']]
                    .sum(axis=0) / 1e+6).round(2)
    
    # Plot
    plt.figure(figsize=(10, 6))
    ax = storage_data.plot(kind='bar', color='skyblue')
    
    # Labels und Titel
    plt.xlabel('Energiespeichertechnologien')
    plt.ylabel('Energieerzeugung [TWh]')
    plt.title('Regelbare Kraftwerkleistung 2023')
    
    # Drehung der x-Achsen-Beschriftungen auf 0 setzen
    plt.xticks(rotation=0)
    
    # Werte über den Balken anzeigen
    for i, value in enumerate(storage_data):
        plt.text(i, value + 1, f"{value}", ha='center', va='bottom', fontsize=10)
    
    # Diagramm speichern
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