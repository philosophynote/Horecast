import pandas as pd
import time
from urllib.request import urlopen
from forecast.func import umaren,umatan,sanrenpuku,sanrentan,insert_result

race_id_list_a = ['2021050405{}'.format(str(i).zfill(2)) for i in range(1, 13, 1)]
race_id_list_b = ['2021090405{}'.format(str(i).zfill(2)) for i in range(1, 13, 1)]
race_id_list_c = ['2021040505{}'.format(str(i).zfill(2)) for i in range(1, 13, 1)]
race_id_list = race_id_list_a  + race_id_list_b + race_id_list_c

insert_result(race_id_list)
print("結果をDBに格納しました")

return_tables = {}
for race_id in race_id_list:
    try:
        print(race_id)
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
umatan(return_tables_df)
sanrenpuku(return_tables_df)
sanrentan(return_tables_df)

print("払戻金をDBに格納しました")