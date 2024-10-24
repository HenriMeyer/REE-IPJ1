import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


#df: data, 
# title: headline, 
# colName: name of column with to be displayed data,
# indexY: Time on Y-axis
# indexX: Time on X-axis

def plotWeekdayHeatmap(df, title, colName, indexY, indexX):

    heatmap_data = df.pivot_table(index = indexY, columns = indexX , values=colName, aggfunc=np.mean) # Leistungsmittelwerte!

    plt.figure(figsize=(20, 8))
    sns.heatmap(heatmap_data, cmap='coolwarm', annot=False, linewidths=.8, cbar=True, xticklabels=1)

    plt.title(title)
    plt.xlabel(indexX)
    plt.ylabel(indexY)

    plt.show()  


