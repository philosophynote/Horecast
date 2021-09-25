from django.db import connection
import pandas as pd
from sqlalchemy import create_engine
from .return_calc import  bet_umaren,bet_sanrenpuku
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

def search_sql(race_date, race_park, race_number):
    # conditions = {
    #     "race_date": race_date,
    #     "race_park": race_park,
    #     "race_number": race_number,
    # }
    # sql = f"""
    #     SELECT race_id,race_park,race_name,race_number,race_date
    #     FROM race
    #     WHERE race_date ={conditions["race_date"]} 
    #     AND race_park ={conditions["race_park"]}
    #     AND race_number ={conditions["race_number"]}
    # """
    # query = 'race_date == {race_date} and race_park == {race_park} and race_number == {race_number}'.format(
    #     **conditions)
    race_df = pd.read_sql("race", con=engine)
    race_df["race_date"] = pd.to_datetime(race_df["race_date"])
    race_df = race_df.query('race_date == @race_date and race_park == @race_park and race_number == @race_number')
    race_id = race_df["race_id"].iloc[-1]
    horse_df = pd.read_sql(f"SELECT * FROM horse WHERE race_id = '{race_id}'", con=engine)
    pred_table = pd.read_sql(f"SELECT * FROM predict WHERE race_id = '{race_id}'", con=engine)

    result = pd.read_sql(f"SELECT * FROM result WHERE race_id = '{race_id}'", con=engine)

    umaren =  pd.read_sql(f"SELECT * FROM umaren WHERE race_id = '{race_id}'",con=engine)

    sanrenpuku = pd.read_sql(f"SELECT * FROM sanrenpuku WHERE race_id = '{race_id}'",con=engine)

   
    df = race_df.merge(horse_df,left_on="race_id",right_on="race_id",how="inner")
    df = df.merge(pred_table, left_on=["race_id", "horse_number"], right_on=["race_id", "horse_number"], how="inner")
    df_pre = df[["race_park","race_name","race_number","race_turn","course_len","weather","race_type","race_condition","n_horses","horse_number","horse_name","sex_age","jockey_name","jockey_weight","pred","center","bet"]]
    df["horse_number"] = df["horse_number"].astype(str)
    df = df.merge(result, left_on=["race_id", "horse_number"], right_on=["race_id", "horse_number"], how="left")
    df_lat = df[["rank","horse_number","horse_name","sex_age","jockey_name","jockey_weight","favorite","odds"]]
    df_lat["rank"] = pd.to_numeric(df_lat["rank"] ,errors="coerce")
    df_lat["rank"].fillna("*",inplace=True)

    df_umaren = umaren.merge(pred_table,how="inner",left_on=["race_id"],right_on=["race_id"])
    race_id_list = df_umaren["race_id"].unique()
    umaren_money = [bet_umaren(df_umaren,race_id) for race_id in race_id_list]
    umaren_dict = dict(zip(race_id_list,umaren_money))
    umaren_df = pd.DataFrame(list(umaren_dict.items()),columns=['race_id', 'umaren'])

    df_sanrenpuku = sanrenpuku.merge(pred_table,how="inner",left_on=["race_id"],right_on=["race_id"])
    race_id_list = df_sanrenpuku["race_id"].unique()
    sanrenpuku_money = [bet_sanrenpuku(df_sanrenpuku,race_id) for race_id in race_id_list]
    sanrenpuku_dict = dict(zip(race_id_list,sanrenpuku_money))
    sanrenpuku_df = pd.DataFrame(list(sanrenpuku_dict.items()),columns=['race_id', 'sanrenpuku'])

    df_re = race_df.merge(umaren_df,how="left",right_on="race_id",left_on="race_id")
    df_re = df_re.merge(sanrenpuku_df,how="left",right_on="race_id",left_on="race_id")
    
    df_re = df_re[["race_number","umaren","sanrenpuku"]]
    return df_pre,df_lat,df_re

def insert_race_card(df):
    race_df = df[["race_id","race_park","race_name","race_number","date","race_turn","course_len","weather","race_type","race_condition","n_horses"]]
    horse_df = df[["race_id","horse_id",'枠', '馬番', '馬名', '性齢', '騎手', '斤量']]
    race_df.rename(columns={'date':'race_date'},inplace=True)
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
    umaren = df[df[0]=='馬連'][[1,2]]
    wins = umaren[1].str.split(expand=True)
    wins = umaren[1].str.split(expand=True)[[0,1]].add_prefix('win_')
    return_ = umaren[2].rename('return') 
    return_ = return_.str.replace('円','')
    return_ = return_.str.replace(',','')
    df = pd.concat([wins, return_], axis=1) 
    df =  df.rename(columns = {'win_0':'win_1','win_1':'win_2'})
    df.apply(lambda x: pd.to_numeric(x.str.replace(',',''), errors='coerce'))
    df.dropna(subset=["win_1"], inplace=True)
    df.index.name = "race_id"
    df["win_1"] = df["win_1"].astype(int)
    df["win_2"] = df["win_2"].astype(int)
    df["return"] = df["return"].astype(int)
    upsert(engine=engine,
          df=df,
          schema="public",
          table_name="umaren",
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
