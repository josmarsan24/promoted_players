import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_bar_comparison_pairs(df, pairs, index):
    # Verificar que las columnas del par están en el DataFrame
    for col1, col2 in pairs:
        if col1 not in df.columns or col2 not in df.columns:
            raise ValueError(f"Una de las columnas {col1} o {col2} no está en el DataFrame")

    # Extraer los datos para los pares de columnas
    values1 = df.loc[index, [pair[0] for pair in pairs]].values.flatten()
    values2 = df.loc[index, [pair[1] for pair in pairs]].values.flatten()

    # Determinar los valores máximos para cada columna en el DataFrame completo
    max_values1 = df[[pair[0] for pair in pairs]].max().values
    max_values2 = df[[pair[1] for pair in pairs]].max().values
    max_values = []
    for i in range(0,len(max_values1)):
        max_values.append(max(max_values1[i],max_values2[i]))

    # Normalizar los valores por los máximos de sus respectivas columnas
    normalized_values1 = values1 / max_values
    normalized_values2 = values2 / max_values
    
    # Configurar las posiciones para las barras
    bar_width = 0.35
    index_pos = np.arange(len(pairs))

    # Crear la figura y los ejes
    fig, ax = plt.subplots(figsize=(10, 6))

    # Crear las barras para los dos conjuntos de valores normalizados
    bars1 = ax.bar(index_pos - bar_width / 2, normalized_values1, bar_width, label='Valores ajustados 1ra')
    bars2 = ax.bar(index_pos + bar_width / 2, normalized_values2, bar_width, label='Valores 2da divsion')

    # Añadir etiquetas, título y leyenda
    name = df.loc[index]['Name']
    ax.set_title(f'Comparación de estadísticas por 90min para {name}')
    ax.set_xticks(index_pos)
    ax.set_xticklabels([f'{col1} vs {col2}' for col1, col2 in pairs])
    ax.legend()

    # Añadir etiquetas de valor encima de las barras
    def add_labels(bars, original_values):
        for bar, original_value in zip(bars, original_values):
            height = bar.get_height()
            ax.annotate(f'{original_value:.2f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    add_labels(bars1, values1)
    add_labels(bars2, values2)

    # Mostrar el gráfico
    plt.tight_layout()
    plt.show()


# Pares de columnas a usar en el gráfico
pairs = [('1_xG', '2_xG'), ('1_xA', '2_xA'), ('1_PrgC', '2_PrgC'), ('1_PrgP', '2_PrgP'), ('1_OffAct', '2_OffAct')]

df = pd.read_csv('promoted_players.csv',header=0)
df2 = pd.read_csv('new_players_pred.csv',header=0)
df = df.append(df2,ignore_index=True)

index1 = len(df)-1
index2 = len(df)-2

plot_bar_comparison_pairs(df, pairs, index1)
plot_bar_comparison_pairs(df, pairs, index2)



