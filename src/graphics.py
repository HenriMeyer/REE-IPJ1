import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def plotWeekdayHeatmap(df, title = 'first Try', colName = 'Photovoltaik'):

    heatmap_data = df.pivot_table(index='Tag_von', columns='Uhrzeit_von', values=colName, aggfunc=np.mean) # Leistungsmittelwerte!

    plt.figure(figsize=(20, 8))
    sns.heatmap(heatmap_data, cmap='coolwarm', annot=False, linewidths=.8, cbar=True, xticklabels=1)

    plt.title(title)
    plt.xlabel('Viertelstunde')
    plt.ylabel('Wochentag')

    plt.show()  
