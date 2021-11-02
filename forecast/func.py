from django.db import connection
import pandas as pd
from sqlalchemy import create_engine
from .return_calc import  bet_umaren,bet_sanrenpuku,bet_umatan,bet_sanrentan
from django.conf import settings
import psycopg2
import time
from pangres import upsert


user = settings.DATABASES["default"]["USER"]
password = settings.DATABASES["default"]["PASSWORD"]
database = settings.DATABASES['default']['NAME']
host = settings.DATABASES['default']['HOST']
port = settings.DATABASES['default']['PORT']

connection_config = {
    "user":user,
    "password":password,
    "database":database,
    "host":host,
    "port":port,
}


# connection = psycopg2.connect(**connection_config)
engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')


def calc_predict(model,df):
    pred = model.predict(df.drop(
        ["horse_id", "date", "jockey_id", "trainer_id"], axis=1))
    pred = pd.DataFrame(pred, columns=["pred"])
    proba = model.predict_proba(df.drop(
        ["horse_id", "date", "jockey_id", "trainer_id"], axis=1))
    return pred,proba

def select_sql_r(df,tablename):
    race_date = df["date"].unique()[0]  
    df = pd.read_sql(f"SELECT * FROM {tablename}",con=connection)
    df["race_date"] = pd.to_datetime(df["race_date"])
    
    df = df[df["race_date"] == race_date]

    return df

def select_sql_h(df,tablename): 
    df = pd.read_sql(f"SELECT * FROM {tablename}",con=connection)
    return df

def making_predtable(pred,proba,race):
    pred_table = pd.concat(
        [race[["race_id", "horse_number"]], pred], axis=1)
    pred_table['pred_proba'] = proba[:, 0]
    rank_d = pd.DataFrame(pred_table.groupby("race_id").rank(ascending=False)[
        "pred_proba"]).rename(columns={"pred_proba": "rank_d"})
    pred_table = pd.concat([pred_table, rank_d.astype(int)], axis=1)
    pred_table['center'] = 0
    pred_table['bet'] = 0
    pred_table['center'] = pred_table.apply(
        lambda x: x["center"] + 1 if x['pred'] == 0 and x['rank_d'] == 1 else x["center"], axis=1)
    pred_table["bet"].mask(pred_table["rank_d"] <= 4, 1, inplace=True)
    return pred_table


def insert_predtable(pred_table):
    insert = pred_table[["race_id",
                         "horse_number", "pred", "center", "bet"]]
    insert["id"] = insert['race_id'].str.cat(insert['horse_number'].astype(str).str.zfill(2))
    insert.reset_index(drop=True,inplace=True)
    insert.set_index('id',inplace=True)
    insert.index[insert.index.duplicated(keep=False)]
    upsert(engine=engine,
          df=insert,
          schema="public",
          table_name="predict",
          if_row_exists='update') 

def read_table(race_id,table_name):
    return pd.read_sql(f"SELECT * FROM {table_name} WHERE race_id = '{race_id}'", con=engine)

def search_sql(race_date, race_park, race_number):
    race_df = pd.read_sql("race", con=engine)
    race_df["race_date"] = pd.to_datetime(race_df["race_date"])
    race_df = race_df.query('race_date == @race_date and race_park == @race_park and race_number == @race_number')
    race_id = race_df["race_id"].iloc[-1]
    horse_df = read_table(race_id,'horse')
    pred_table = read_table(race_id,"predict")
    result = read_table(race_id,"result")
    umaren = read_table(race_id,"umaren")
    umatan = read_table(race_id,"umatan")
    sanrenpuku = read_table(race_id,"sanrenpuku")
    sanrentan = read_table(race_id,"sanrentan")
    
   
    df = race_df.merge(horse_df,left_on="race_id",right_on="race_id",how="inner")
    print("競走馬データとマージ")
    print(df.head())
    df = df.merge(pred_table, left_on=["race_id", "horse_number"], right_on=["race_id", "horse_number"], how="inner")
    print("予想データとマージ")
    print(df.head())  
    df_pre = df[["race_park","race_name","race_number","race_turn","course_len","weather","race_type","race_condition","n_horses","horse_number","horse_name","sex_age","jockey_name","jockey_weight","pred","center","bet"]]
    print("必要なデータを抽出")
    print(df_pre.head()) 
    df["horse_number"] = df["horse_number"].astype(str)
    df = df.merge(result, left_on=["race_id", "horse_number"], right_on=["race_id", "horse_number"], how="left")
    print("レース結果")
    print(df.head()) 
    df_lat = df[["rank","horse_number","horse_name","sex_age","jockey_name","jockey_weight","favorite","odds"]]
    df_lat["rank"] = pd.to_numeric(df_lat["rank"] ,errors="coerce")
    df_lat["favorite"] = pd.to_numeric(df_lat["favorite"] ,errors="coerce")
    df_lat["odds"] = pd.to_numeric(df_lat["odds"] ,errors="coerce")
    df_lat["rank"].fillna("*",inplace=True)
    df_lat["favorite"].fillna("*",inplace=True)
    df_lat["odds"].fillna("*",inplace=True)

    df_umaren = umaren.merge(pred_table,how="inner",left_on=["race_id"],right_on=["race_id"])
    race_id_list = df_umaren["race_id"].unique()
    umaren_money = [bet_umaren(df_umaren,race_id) for race_id in race_id_list]
    umaren_dict = dict(zip(race_id_list,umaren_money))
    umaren_df = pd.DataFrame(list(umaren_dict.items()),columns=['race_id', 'umaren'])

    df_umatan = umatan.merge(pred_table,how="inner",left_on=["race_id"],right_on=["race_id"])
    race_id_list = df_umatan["race_id"].unique()
    umatan_money = [bet_umatan(df_umatan,race_id) for race_id in race_id_list]
    umatan_dict = dict(zip(race_id_list,umatan_money))
    umatan_df = pd.DataFrame(list(umatan_dict.items()),columns=['race_id', 'umatan'])

    df_sanrenpuku = sanrenpuku.merge(pred_table,how="inner",left_on=["race_id"],right_on=["race_id"])
    race_id_list = df_sanrenpuku["race_id"].unique()
    sanrenpuku_money = [bet_sanrenpuku(df_sanrenpuku,race_id) for race_id in race_id_list]
    sanrenpuku_dict = dict(zip(race_id_list,sanrenpuku_money))
    sanrenpuku_df = pd.DataFrame(list(sanrenpuku_dict.items()),columns=['race_id', 'sanrenpuku'])

    df_sanrentan = sanrentan.merge(pred_table,how="inner",left_on=["race_id"],right_on=["race_id"])
    race_id_list = df_sanrentan["race_id"].unique()
    sanrentan_money = [bet_sanrentan(df_sanrentan,race_id) for race_id in race_id_list]
    sanrentan_dict = dict(zip(race_id_list,sanrentan_money))
    sanrentan_df = pd.DataFrame(list(sanrentan_dict.items()),columns=['race_id', 'sanrentan'])

    df_re = race_df.merge(umaren_df,how="left",right_on="race_id",left_on="race_id")
    df_re = df_re.merge(sanrenpuku_df,how="left",right_on="race_id",left_on="race_id")
    df_re = df_re.merge(umatan_df,how="left",right_on="race_id",left_on="race_id")
    df_re = df_re.merge(sanrentan_df,how="left",right_on="race_id",left_on="race_id")
    
    df_re = df_re[["race_number","umaren","umatan","sanrenpuku","sanrentan"]]
    df_re["umaren"] = pd.to_numeric(df_re["umaren"] ,errors="coerce")
    df_re["umatan"] = pd.to_numeric(df_re["umatan"] ,errors="coerce")
    df_re["sanrenpuku"] = pd.to_numeric(df_re["sanrenpuku"] ,errors="coerce")
    df_re["sanrentan"] = pd.to_numeric(df_re["sanrentan"] ,errors="coerce")
    df_re["umaren"].fillna("*",inplace=True)
    df_re["umatan"].fillna("*",inplace=True)
    df_re["sanrenpuku"].fillna("*",inplace=True)
    df_re["sanrentan"].fillna("*",inplace=True)
    return race_id,df_pre,df_lat,df_re

def insert_race_card(df):
    race_df = df[["race_id","race_park","race_name","race_number","date","race_turn","course_len","weather","race_type","race_condition","n_horses"]]
    horse_df = df[["race_id","horse_id",'枠', '馬番', '馬名', '性齢', '騎手', '斤量']]
    race_df.rename(columns={'date':'race_date'},inplace=True)
    race_df["race_date"] = race_df["race_date"].str.replace('-','/')
    horse_df.rename(columns={'枠': 'frame_number', '馬番': 'horse_number', '馬名': 'horse_name', '性齢': "sex_age", '騎手': 'jockey_name', '斤量': 'jockey_weight'}, inplace=True)
    race_df.drop_duplicates(inplace=True)
    race_df=race_df.reset_index(drop=True)
    race_df.set_index("race_id",inplace=True)
    horse_df["id"] = horse_df['race_id'].str.cat(horse_df['horse_number'].astype(str).str.zfill(2))
    horse_df=horse_df.reset_index(drop=True)
    horse_df.set_index("id",inplace=True)
    upsert(engine=engine,
          df=race_df,
          schema="public",
          table_name="race",
          if_row_exists='update') 
    upsert(engine=engine,
          df=horse_df,
          schema="public",
          table_name="horse",
          if_row_exists='update')

def insert_result(race_id_list):
    data = pd.DataFrame()
    for race_id in race_id_list:
        try:
            print(race_id)
            url = "https://race.netkeiba.com/race/result.html?race_id=" + race_id
            df = pd.read_html(url)[0]
            df["race_id"] = [race_id] * len(df)
            df["rank"] = df["着順"].astype(str)
            df["horse_number"] = df["馬番"].astype(str)
            df["favorite"] = df["人気"].astype(str)
            df["odds"] = df["単勝オッズ"].astype(str)
            df = df[["race_id","rank","horse_number","favorite","odds"]]
        #     df.rename(columns={'馬名':'horse_name'},inplace=True)
            data = data.append(df)
            time.sleep(1)
        # 存在しないrace_idを飛ばす
        except IndexError:
            continue
        # wifiの接続が切れた時などでも途中までのデータを返せるようにする
        except Exception as e:
            print(e)
            continue
        # Jupyterで停止ボタンを押した時の対処
        except:
            break
    data["id"] = data['race_id'].str.cat(data['horse_number'].astype(str).str.zfill(2))
    data.reset_index(drop=True,inplace=True)
    data.set_index("id",inplace=True)
    upsert(engine=engine,
          df=data,
          schema="public",
          table_name="result",
          if_row_exists='update')

def umaren(df):
    new_df = pd.DataFrame(columns=['win_1','win_2','win_3','win_4','return_1','return_2'])
    umaren = df[df[0]=='馬連'][[1,2]]
    if umaren[2].str.contains('br').any():
        new_df[['win_1','win_2','win_3','win_4']] = umaren[1].str.split(expand=True)[[0,1,2,3]]
        new_df[['return_1','return_2']] = umaren[2].str.split('br',expand=True)[[0,1]]

        new_df['return_1'] = new_df['return_1'].str.replace('円','')
        new_df['return_1'] = new_df['return_1'].str.replace(',','')
        new_df['return_2'] = new_df['return_2'].str.replace('円','')
        new_df['return_2'] = new_df['return_2'].str.replace(',','')
        new_df.apply(lambda x: pd.to_numeric(x.str.replace(',',''), errors='coerce'))
        new_df.dropna(subset=["win_1"], inplace=True)
        new_df.index.name = "race_id"
        new_df.fillna(0,inplace=True)
        new_df["win_1"] = new_df["win_1"].astype(int)
        new_df["win_2"] = new_df["win_2"].astype(int)
        new_df["win_3"] = new_df["win_3"].astype(int)
        new_df["win_4"] = new_df["win_4"].astype(int)
        new_df["return_1"] = new_df["return_1"].astype(int)
        new_df["return_2"] = new_df["return_2"].astype(int)
    else:
        umaren = df[df[0]=='馬連'][[1,2]]
        wins = umaren[1].str.split(expand=True)
        wins = umaren[1].str.split(expand=True)[[0,1]].add_prefix('win_')
        return_1 = umaren[2].rename('return_1') 
        return_1 = return_1.str.replace('円','')
        return_1 = return_1.str.replace(',','')
        new_df = pd.concat([wins, return_1], axis=1) 
        new_df =  new_df.rename(columns = {'win_0':'win_1','win_1':'win_2'})
        new_df.apply(lambda x: pd.to_numeric(x.str.replace(',',''), errors='coerce'))
        new_df.dropna(subset=["win_1"], inplace=True)
        new_df.index.name = "race_id"
        new_df["win_1"] = new_df["win_1"].astype(int)
        new_df["win_2"] = new_df["win_2"].astype(int)
        new_df["return_1"] = new_df["return_1"].astype(int)
    upsert(engine=engine,
          df=new_df,
          schema="public",
          table_name="umaren",
          if_row_exists='update')

def umatan(df):
    new_df = pd.DataFrame(columns=['win_1','win_2','win_3','win_4','return_1','return_2'])
    umatan = df[df[0]=='馬単'][[1,2]]
    if umatan[2].str.contains('br').any():
        new_df[['win_1','win_2','win_3','win_4']] = umatan[1].str.split(expand=True)[[0,1,2,3]]
        new_df[['return_1','return_2']] = umatan[2].str.split('br',expand=True)[[0,1]]

        new_df['return_1'] = new_df['return_1'].str.replace('円','')
        new_df['return_1'] = new_df['return_1'].str.replace(',','')
        new_df['return_2'] = new_df['return_2'].str.replace('円','')
        new_df['return_2'] = new_df['return_2'].str.replace(',','')
        new_df.apply(lambda x: pd.to_numeric(x.str.replace(',',''), errors='coerce'))
        new_df.dropna(subset=["win_1"], inplace=True)
        new_df.index.name = "race_id"
        new_df.fillna(0,inplace=True)
        new_df["win_1"] = new_df["win_1"].astype(int)
        new_df["win_2"] = new_df["win_2"].astype(int)
        new_df["win_3"] = new_df["win_3"].astype(int)
        new_df["win_4"] = new_df["win_4"].astype(int)
        new_df["return_1"] = new_df["return_1"].astype(int)
        new_df["return_2"] = new_df["return_2"].astype(int)
    else:
        umatan = df[df[0]=='馬単'][[1,2]]
        wins = umatan[1].str.split(expand=True)
        wins = umatan[1].str.split(expand=True)[[0,1]].add_prefix('win_')
        return_1 = umatan[2].rename('return_1') 
        return_1 = return_1.str.replace('円','')
        return_1 = return_1.str.replace(',','')
        new_df = pd.concat([wins, return_1], axis=1) 
        new_df =  new_df.rename(columns = {'win_0':'win_1','win_1':'win_2'})
        new_df.apply(lambda x: pd.to_numeric(x.str.replace(',',''), errors='coerce'))
        new_df.dropna(subset=["win_1"], inplace=True)
        new_df.index.name = "race_id"
        new_df["win_1"] = new_df["win_1"].astype(int)
        new_df["win_2"] = new_df["win_2"].astype(int)
        new_df["return_1"] = new_df["return_1"].astype(int)    
    upsert(engine=engine,
          df=new_df,
          schema="public",
          table_name="umatan",
          if_row_exists='update')

def sanrenpuku(df):
    renpuku = df[df[0]=='3連複'][[1,2]]
    wins = renpuku[1].str.split(expand=True)[[0,1,2]].add_prefix('win_')
    return_ = renpuku[2].rename('return')
    return_ = return_.str.replace('円','')
    return_ = return_.str.replace(',','')
    df = pd.concat([wins, return_], axis=1)
    df =  df.rename(columns = {'win_0':'win_1','win_1':'win_2','win_2':'win_3'})
    df.apply(lambda x: pd.to_numeric(x.str.replace(',',''), errors='coerce'))
    df.dropna(subset=["win_1"], inplace=True)
    df.index.name = "race_id"
    df["win_1"] = df["win_1"].astype(int)
    df["win_2"] = df["win_2"].astype(int)
    df["win_3"] = df["win_3"].astype(int)
    df["return"] = df["return"].astype(int)
    upsert(engine=engine,
          df=df,
          schema="public",
          table_name="sanrenpuku",
          if_row_exists='update')

def sanrentan(df):
    new_df = pd.DataFrame(columns=['win_1','win_2','win_3','win_4','win_5','win_6','return_1','return_2'])
    rentan = df[df[0]=='3連単'][[1,2]]
    if rentan[2].str.contains('br').any():
        new_df[['win_1','win_2','win_3','win_4','win_5','win_6']] = rentan[1].str.split(expand=True)[[0,1,2,3,4,5]]
        new_df[['return_1','return_2']] = rentan[2].str.split('br',expand=True)[[0,1]]

        new_df['return_1'] = new_df['return_1'].str.replace('円','')
        new_df['return_1'] = new_df['return_1'].str.replace(',','')
        new_df['return_2'] = new_df['return_2'].str.replace('円','')
        new_df['return_2'] = new_df['return_2'].str.replace(',','')
        new_df.apply(lambda x: pd.to_numeric(x.str.replace(',',''), errors='coerce'))
        new_df.dropna(subset=["win_1"], inplace=True)
        new_df.index.name = "race_id"
        new_df.fillna(0,inplace=True)
        new_df["win_1"] = new_df["win_1"].astype(int)
        new_df["win_2"] = new_df["win_2"].astype(int)
        new_df["win_3"] = new_df["win_3"].astype(int)
        new_df["win_4"] = new_df["win_4"].astype(int)
        new_df["win_5"] = new_df["win_5"].astype(int)
        new_df["win_6"] = new_df["win_6"].astype(int)
        new_df["return_1"] = new_df["return_1"].astype(int)
        new_df["return_2"] = new_df["return_2"].astype(int)
    else:
        renpuku = df[df[0]=='3連単'][[1,2]]
        wins = renpuku[1].str.split(expand=True)[[0,1,2]].add_prefix('win_')
        return_1 = renpuku[2].rename('return_1')
        return_1 = return_1.str.replace('円','')
        return_1 = return_1.str.replace(',','')
        new_df = pd.concat([wins, return_1], axis=1)
        new_df =  new_df.rename(columns = {'win_0':'win_1','win_1':'win_2','win_2':'win_3'})
        new_df.apply(lambda x: pd.to_numeric(x.str.replace(',',''), errors='coerce'))
        new_df.dropna(subset=["win_1"], inplace=True)
        new_df.index.name = "race_id"
        new_df["win_1"] = new_df["win_1"].astype(int)
        new_df["win_2"] = new_df["win_2"].astype(int)
        new_df["win_3"] = new_df["win_3"].astype(int)
        new_df["return_1"] = new_df["return_1"].astype(int)     
    upsert(engine=engine,
          df=new_df,
          schema="public",
          table_name="sanrentan",
          if_row_exists='update')