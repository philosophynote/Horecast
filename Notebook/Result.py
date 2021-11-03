# 親クラスの読み込み
from DP import DataProcessor

# データフレーム用
import pandas as pd

# スクレイピング用
import requests
import re
import time
from tqdm.notebook import tqdm
from bs4 import BeautifulSoup

# ラベル変換用
from sklearn.preprocessing import LabelEncoder


class Results(DataProcessor):
    def __init__(self, results):
        super(Results, self).__init__()
        self.data = results

    @classmethod
    def read_pickle(cls, path_list):
        df = pd.concat([pd.read_pickle(path) for path in path_list])
        return cls(df)

    @staticmethod
    def scrape(race_id_list):

        # race_idをkeyにしてDataFrame型を格納
        race_results = {}
        for race_id in tqdm(race_id_list):
            try:
                url = "https://db.netkeiba.com/race/" + race_id
                # メインとなるテーブルデータを取得
                df = pd.read_html(url)[0]

                html = requests.get(url)
                html.encoding = "EUC-JP"
                soup = BeautifulSoup(html.text, "html.parser")

                df["prize"] = soup.find("table", attrs={"class": "race_table_01 nk_tb_common"}).find_all(
                    "td", attrs={"class": "txt_r"})[4].text
                # 天候、レースの種類、コースの長さ、馬場の状態、日付をスクレイピング
                texts = (
                    soup.find("div", attrs={"class": "data_intro"}).find_all(
                        "p")[0].text
                    + soup.find("div", attrs={"class": "data_intro"}).find_all("p")[1].text
                )
                info = re.findall(r'\w+', texts)
                if info[0][0] in ["芝","ダ","障"]:
                    df["race_turn"] = info[0][1]
                for text in info:
                    if text in ["芝", "ダート"]:
                        df["race_type"] = [text] * len(df)
                    if "障" in text:
                        df["race_type"] = ["障害"] * len(df)
                    if "m" in text:
                        df["course_len"] = [
                            int(re.findall(r"\d+", text)[0])] * len(df)
                    if text in ["良", "稍重", "重", "不良"]:
                        df["race_condition"] = [text] * len(df)
                    if text in ["曇", "晴", "雨", "小雨", "小雪", "雪"]:
                        df["weather"] = [text] * len(df)
                    if "年" in text:
                        df["date"] = [text] * len(df)
                    if "回" in text:
                        df["race_park"] = re.findall(r"\D+", text)[0][1:]
                        # 馬ID、騎手IDをスクレイピング
                horse_id_list = []
                horse_a_list = soup.find("table", attrs={"summary": "レース結果"}).find_all(
                    "a", attrs={"href": re.compile("^/horse")}
                )
                for a in horse_a_list:
                    horse_id = re.findall(r"\d+", a["href"])
                    horse_id_list.append(horse_id[0])
                jockey_id_list = []
                jockey_a_list = soup.find("table", attrs={"summary": "レース結果"}).find_all(
                    "a", attrs={"href": re.compile("^/jockey")}
                )
                for a in jockey_a_list:
                    jockey_id = re.findall(r"\d+", a["href"])
                    jockey_id_list.append(jockey_id[0])

                trainer_id_list = []
                trainer_a_list = soup.find("table", attrs={"summary": "レース結果"}).find_all(
                    "a", attrs={"href": re.compile("^/trainer")}
                )
                for a in trainer_a_list:
                    trainer_id = re.findall(r"\d+", a["href"])
                    trainer_id_list.append(trainer_id[0])

                df["horse_id"] = horse_id_list
                df["jockey_id"] = jockey_id_list
                df["trainer_id"] = trainer_id_list

                # インデックスをrace_idにする
                df.index = [race_id] * len(df)

                race_results[race_id] = df
                time.sleep(1)
            # 存在しないrace_idを飛ばす
            except IndexError:
                continue
            # wifiの接続が切れた時などでも途中までのデータを返せるようにする
            except Exception as e:
                print(e)
                break
            # Jupyterで停止ボタンを押した時の対処
            except:
                break
        # pd.DataFrame型にして一つのデータにまとめる
        race_results_df = pd.concat([race_results[key]
                                    for key in race_results])

        return race_results_df

    def preprocessing(self):
        df = self.data.copy()
        # 出走頭数
        df['n_horses'] = df.index.map(df.index.value_counts())
        # 着順についての前処理
        # 数値に変換できる物は変換して、該当しないものはNanを返す
        df["着順"] = pd.to_numeric(df["着順"], errors="coerce")
        df.dropna(subset=["着順"], inplace=True)
        df["rank"] = df["着順"].astype(int)

        def rank(x):
            if x >= 1 and x <= 3:
                return 0
            else:
                return 1
        df['rank'] = df['着順'].map(lambda x: rank(x))

        df["course_len"] = df["course_len"] // 100

        # 性齢を性と年齢に分ける
        df["sex"] = df["性齢"].map(lambda x: str(x)[0])
        df["age"] = df["性齢"].map(lambda x: str(x)[1:]).astype(int)

        # prizeについての前処理
        df["prize"] = pd.to_numeric(
            df["prize"].str.replace(",", ""), errors="coerce")
        df["prize"] = df["prize"].astype(float)

        # # 馬体重を体重と体重変化に分ける
        # df["体重"] = df["馬体重"].str.split("(", expand=True)[0].astype(int)
        # df["増減"] = df["馬体重"].str.split("(", expand=True)[1].str.split(")", expand=True)[0]

        # データ型を変換
        df["date"] = pd.to_datetime(df["date"], format="%Y年%m月%d日")
        df["weight_j"] = df["斤量"].astype(float)
        df["単勝"] = df["単勝"].astype(float)

        # カラム名変換
        df.rename(columns={"枠番": "frame_number", "馬番": "horse_number", "単勝": "odds",
                           "人気": "favorite", "馬場条件": "race_condition", "競馬場": "race_park"}, inplace=True)

        # 不要な列を削除
        df.drop(["着順", "馬名", "性齢", "斤量", "騎手", "タイム",
                "着差", "馬体重", "調教師"], axis=1, inplace=True)
        # 順番入れ替え
        df = df.reindex(columns=["rank", "odds", "favorite", "frame_number", "horse_number", "sex", "age", "weight_j", "prize", "race_turn", "course_len",
                                 "weather", "race_type", "race_condition", "n_horses", "date", "race_park", "horse_id", "jockey_id", "trainer_id"])

        self.data_p = df

    def process_categorical(self):
        # fitメゾット()内の値を番号にラベルに変換
        self.le_jockey = LabelEncoder().fit(self.data_pe["jockey_id"])
        self.le_trainer = LabelEncoder().fit(self.data_pe["trainer_id"])
        super().process_categorical(self.le_jockey, self.le_trainer, self.data_pe)
