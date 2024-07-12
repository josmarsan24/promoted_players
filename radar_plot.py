import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import pi

def plot_radar(df, cols, index1, index2):

    name_1 = df.loc[index1]['Name']
    name_2 = df.loc[index2]['Name']

    cols_plot = list(map(lambda x: x.split('_')[2], cols))

    # Verificar que las columnas están en el DataFrame
    for col in cols:
        if col not in df.columns:
            raise ValueError(f"La columna {col} no está en el DataFrame")

    # Extraer los datos para los dos índices
    values1 = df.loc[index1, cols].values.flatten().tolist()
    values2 = df.loc[index2, cols].values.flatten().tolist()
    
    # Añadir el primer valor al final para cerrar el gráfico de radar
    values1 += values1[:1]
    values2 += values2[:1]

    # Número de variables
    num_vars = len(cols)

    # Calcular los ángulos para cada variable
    angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
    angles += angles[:1]

    # Inicializar el gráfico
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    # Dibujar una línea para cada conjunto de valores y rellenar el área
    ax.plot(angles, values1, linewidth=2, linestyle='solid', label=f'Index {index1}')
    ax.fill(angles, values1, alpha=0.25)

    ax.plot(angles, values2, linewidth=2, linestyle='solid', label=f'Index {index2}')
    ax.fill(angles, values2, alpha=0.25)

    # Añadir etiquetas para cada ángulo
    plt.xticks(angles[:-1], cols_plot)

    # Añadir una leyenda
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

    # Título del gráfico
    plt.title(f'Comparación de {name_1} y {name_2} esperado en 1ra división', size=20, color='blue', y=1.1)

    # Mostrar el gráfico
    plt.show()

df = pd.read_csv('promoted_players.csv',header=0)
df2 = pd.read_csv('new_players_pred.csv',header=0)
df = df.append(df2,ignore_index=True)

#get percentiles in columns to plot
cols = ['1_xG','1_PrgC','1_PrgP','1_xA','1_OffAct']
for col in cols:
    df['Per_Rank'+col] = df[col].rank(pct = True)

print(df.tail(5))

cols = ['Per_Rank1_xG','Per_Rank1_PrgC','Per_Rank1_PrgP','Per_Rank1_xA','Per_Rank1_OffAct']
index1 = len(df)-1
index2 = len(df)-2

plot_radar(df, cols, index1, index2)
