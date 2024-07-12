import pandas as pd
import requests
import time
import sys

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
url_granada_2da = "https://fbref.com/en/squads/a0435291/2022-2023/Granada-Stats"
url_granada_1ra = "https://fbref.com/en/squads/a0435291/2023-2024/Granada-Stats"
url_alaves_2da = "https://fbref.com/en/squads/8d6fd021/2022-2023/Alaves-Stats"
url_alaves_1ra = "https://fbref.com/en/squads/8d6fd021/2023-2024/Alaves-Stats"
url_las_palmas_2da = "https://fbref.com/en/squads/0049d422/2022-2023/Las-Palmas-Stats"
url_las_palmas_1ra = "https://fbref.com/en/squads/0049d422/2023-2024/Las-Palmas-Stats"

def get_team_data(url,div):
    ID_TABLE_STANDARD = ""
    ID_TABLE_SHOOTING = ""
    ID_TABLE_PASSING = ""
    ID_TABLE_PASSING_TYPES = ""
    ID_TABLE_DRIBBLING = ""
    if div == 2:
        ID_TABLE_STANDARD = "stats_standard_17"
        ID_TABLE_SHOOTING = "stats_shooting_17"
        ID_TABLE_PASSING = "stats_passing_17"
        ID_TABLE_PASSING_TYPES = "stats_passing_types_17"
        ID_TABLE_DRIBBLING = "stats_possession_17"
    elif div == 1:
        ID_TABLE_STANDARD = "stats_standard_12"
        ID_TABLE_SHOOTING = "stats_shooting_12"
        ID_TABLE_PASSING = "stats_passing_12"
        ID_TABLE_PASSING_TYPES = "stats_passing_types_12"
        ID_TABLE_DRIBBLING = "stats_possession_12"
    else:
        return pd.DataFrame()
    
    #read standard df
    try:
        response = requests.get(url,headers=headers)
        retry = 5
        while response.status_code == 429 and retry > 0:
            retry = retry - 1
            print('retry')
            time.sleep(5)
            response = requests.get(url,headers=headers)
        df = pd.read_html(response.text, attrs={"id":ID_TABLE_STANDARD})[0]
    except:
        print('Cant retrieve data')
        sys.exit(1)
    df = df[[('Unnamed: 0_level_0', 'Player'),('Playing Time', '90s'),('Unnamed: 2_level_0', 'Pos'),('Expected', 'xG'),('Progression', 'PrgC'),('Progression', 'PrgP')]]
    df.columns = ['Name','90s','Pos','xG','PrgC','PrgP']
    df['xA']=0
    df['OffAct']=0
    #read shoots
    try:
        response = requests.get(url,headers=headers)
        retry = 5
        while response.status_code == 429 and retry > 0:
            print('retry')
            retry = retry - 1
            time.sleep(5)
            response = requests.get(url,headers=headers)
        df_aux = pd.read_html(response.text, attrs={"id":ID_TABLE_SHOOTING})[0]
    except:
        print('Cant retrieve data')
        sys.exit(1)
    df_aux = df_aux[[('Unnamed: 0_level_0', 'Player'),('Standard', 'Sh')]]
    df_aux.columns = ['Name','Sh']
    df['OffAct']=df_aux['Sh']
    #read crosses
    df_aux = pd.read_html(response.text, attrs={"id":ID_TABLE_PASSING_TYPES})[0]
    df_aux = df_aux[[('Unnamed: 0_level_0', 'Player'),('Pass Types', 'Crs')]]
    df_aux.columns = ['Name','Crs']
    df['OffAct']=df['OffAct']+df_aux['Crs']
    #read dribbles
    df_aux = pd.read_html(response.text, attrs={"id":ID_TABLE_PASSING_TYPES})[0]
    df_aux = df_aux[[('Unnamed: 0_level_0', 'Player'),('Take-Ons', 'Succ')]]
    df_aux.columns = ['Name','Drib']
    df['OffAct']=df['OffAct']+df_aux['Drib']
    #read xA
    df_aux = pd.read_html(response.text, attrs={"id":ID_TABLE_PASSING_TYPES})[0]
    df_aux = df_aux[[('Unnamed: 0_level_0', 'Player'),('Expected', 'xA')]]
    df_aux.columns = ['Name','xA']
    df['xA']=df_aux['xA']
    #filter Fowards/Midfielders and min 4.0 90s games and turn stats per 90
    numeric_columns = ['90s','xG','PrgC','PrgP','xA','OffAct']
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col])
    df = df[df['90s'] >= 4.0]
    positions = ['FW','FW,MF','MF,FW','MF']
    df = df.loc[df['Pos'].isin(positions)]
    columns_to_divide = ['xG', 'xA', 'PrgC', 'PrgP', 'OffAct']
    for col in columns_to_divide:
        df[col] = df[col] / df['90s']
    return df

def join_df(url1,url2,team):
    df1 = get_team_data(url1,1)
    df2 = get_team_data(url2,2)
    df1.columns = ['Name','1_90s','1_Pos','1_xG','1_PrgC','1_PrgP','1_xA','1_OffAct']
    df2.columns = ['Name','2_90s','2_Pos','2_xG','2_PrgC','2_PrgP','2_xA','2_OffAct']
    df1_unique = df1.drop_duplicates(subset=['Name'])
    df2_unique = df2.drop_duplicates(subset=['Name'])
    df_merged = pd.merge(df1_unique, df2_unique, on='Name', how='inner')
    df_merged['Team']=team
    return df_merged

#DF for Granada, Alaves and Las Palmas
df1 = join_df(url_granada_1ra,url_granada_2da,'GRANADA')
df2 = join_df(url_alaves_1ra,url_alaves_2da,'ALAVES')
df3 = join_df(url_las_palmas_1ra,url_las_palmas_2da,'LAS PALMAS')
df = pd.concat([df1,df2,df3])
df.to_csv('promoted_players.csv')
