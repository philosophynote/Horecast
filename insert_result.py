import pandas as pd
import time
from sqlalchemy import create_engine
from django.conf import settings
from urllib.request import urlopen
from forecast.func import umaren,sanrenpuku

user = settings.DATABASES["default"]["USER"]
password = settings.DATABASES["default"]["PASSWORD"]
database = settings.DATABASES['default']['NAME']
host = settings.DATABASES['default']['HOST']
port = settings.DATABASES['default']['PORT']

engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')

race_id_list_nsn = ['2021060404{}'.format(str(i).zfill(2)) for i in range(1, 13, 1)]
race_id_list_csn = ['2021070504{}'.format(str(i).zfill(2)) for i in range(1, 13, 1)]
race_id_list_sn = race_id_list_nsn  + race_id_list_csn 

data = pd.DataFrame()
for race_id in race_id_list_sn:
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

data.reset_index(drop=True,inplace=True)
data.to_sql(name="result",schema='public',con=engine,if_exists = "append",index=False)
print("結果をDBに格納しました")

return_tables = {}
for race_id in race_id_list_sn:
    try:
        url = "https://race.netkeiba.com/race/result.html?race_id=" + race_id
        #普通にスクレイピングすると複勝やワイドなどが区切られないで繋がってしまう。
        #そのため、改行コードを文字列brに変換して後でsplitする
        f = urlopen(url)
        html = f.read()
        html = html.replace(b'<br />', b'br')
        dfs = pd.read_html(html)
        #dfsの1番目に単勝〜馬連、2番目にワイド〜三連単がある
        df = pd.concat([dfs[1], dfs[2]])
        df.index = [race_id] * len(df)
        return_tables[race_id] = df
        time.sleep(1)
    except IndexError:
        continue
    except Exception as e:
        print(e)
        continue
    except:
        break
#pd.DataFrame型にして一つのデータにまとめる
return_tables_df = pd.concat([return_tables[key] for key in return_tables])
umaren(return_tables_df)
sanrenpuku(return_tables_df)

print("払戻金をDBに格納しました")