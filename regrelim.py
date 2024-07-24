import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')
from sklearn.linear_model import LinearRegression

#read data
df = pd.read_csv('promoted_players.csv',header=0)
df_new = pd.read_csv('new_players.csv',header=0)
print(df.head(5))

PLAYER_0 = df_new.iloc[0]
PLAYER_1 = df_new.iloc[1]
data_pred = {'Name':[PLAYER_0['Name'],PLAYER_1['Name']],
             '1_90s':[0.0,0.0],'1_Pos':[PLAYER_0['Pos'],PLAYER_1['Pos']],
             '1_xG':[0.0,0.0],'1_PrgC':[0.0,0.0],
             '1_PrgP':[0.0,0.0],'1_xA':[0.0,0.0],
             '1_OffAct':[0.0,0.0],'2_90s':[PLAYER_0['90s'],PLAYER_1['90s']],
             '2_Pos':[PLAYER_0['Pos'],PLAYER_1['Pos']],
             '2_xG':[PLAYER_0['xG'],PLAYER_1['xG']],
             '2_PrgC':[PLAYER_0['PrgC'],PLAYER_1['PrgC']],
             '2_PrgP':[PLAYER_0['PrgP'],PLAYER_1['PrgP']],
             '2_xA':[PLAYER_0['xA'],PLAYER_1['xA']],
             '2_OffAct':[PLAYER_0['OffAct'],PLAYER_1['OffAct']],
             'Team':[PLAYER_0['Team'],PLAYER_1['Team']]}

dict_esp={'1':'1ra','2':'2da','xG':'xG','PrgC':'ProgCar','PrgP':'ProgPass','xA':'xA','OffAct':'AccOff'}

def col_name_esp(col):
    col=str(col)
    try:
        div = dict_esp[col.split('_')[0]]
        return col.split('_')[1] + ' en ' + div
    except:
        return col
        
def regrelim(df, col1, col2):
    if col1 not in df.columns or col2 not in df.columns:
        raise ValueError(f"Una o ambas columnas no están en el DataFrame: {col1}, {col2}")
    
    x_train = df[col2].values.reshape(-1, 1)
    y_train = df[col1].values

    regr = LinearRegression()
    regr.fit(x_train, y_train)
    y_pred = regr.predict(x_train)

    r2 = regr.score(x_train, y_train)
    slope = regr.coef_[0]
    intercept = regr.intercept_

    return regr, y_pred, r2, slope, intercept

#plot regrelim
def plot_regression(df, col1, col2,val0,val1):
    regr, y_pred, r2, slope, intercept = regrelim(df, col1, col2)
    
    plt.figure(figsize=(10, 6))
    plt.scatter(df[col2], df[col1], color='blue', label='Resto jugadores')
    plt.plot(df[col2], y_pred, color='red', linewidth=2, label='Regresión lineal')

    x_pred = np.array([val0]).reshape(-1, 1)
    new_pred = regr.predict(x_pred)
    y_0 = new_pred[0]
    plt.scatter(x_pred, new_pred, color='green', s=100, label=PLAYER_0['Name'])

    x_pred = np.array([val1]).reshape(-1, 1)
    new_pred = regr.predict(x_pred)
    y_1 = new_pred[0]
    plt.scatter(x_pred, new_pred, color='purple', s=100, label=PLAYER_1['Name'])

    col1_esp = col_name_esp(col1)
    col2_esp = col_name_esp(col2)
    plt.xlabel(col2_esp)
    plt.ylabel(col1_esp)
    plt.suptitle(f'Regresión Lineal entre {col1_esp} y {col2_esp}',fontsize=16)
    plt.title(f'$R^2 = {r2:.2f}$ ' + f'$y = {slope:.2f}x + {intercept:.2f}$',fontsize=12)
    plt.legend()
    plt.grid(True)
    plt.show()

    return y_0,y_1

#regrelim for all cols
cols = ['xG','PrgC','PrgP','xA','OffAct']
for col in cols:
    y_0,y_1 = plot_regression(df,'1_'+col,'2_'+col,PLAYER_0[col],PLAYER_1[col])
    data_pred['1_'+col] = [y_0,y_1]

df_pred = pd.DataFrame(data_pred)
df_pred.to_csv('new_players_pred.csv',index=False)