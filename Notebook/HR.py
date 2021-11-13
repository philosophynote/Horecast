# データフレーム用
import pandas as pd

# スクレイピング用
from tqdm.notebook import tqdm
import time
import re
import numpy as np
import requests
from sklearn.impute import SimpleImputer
from bs4 import BeautifulSoup


# map関数で使用
place_dict = {"札幌": "01", "函館": "02", "福島": "03", "新潟": "04", "東京": "05", "中山": "06", "中京": "07", "京都": "08", "阪神": "09", "小倉": "10", "園田": "11",
              "名古屋": "11", "高知": "11", "佐賀": "11", "金沢": "11", "笠松": "11", "大井": "11", "盛岡": "11", "水沢": "11", "川崎": "11", "門別": "11", "船橋": "11", "浦和": "11"}
race_type_dict = {"芝": "芝", "ダ": "ダート", "障": "障害"}
field_mapping = {"不": "悪", "重": "悪", "稍": "悪", "良": "良"}


class HorseResults:
    def __init__(self, horse_results):
        self.horse_results = horse_results[
            ['日付', 'オッズ', '人気', '着順', '距離', '上り', '通過', '賞金',  'time_index']]
        self.preprocessing()

    @classmethod
    def read_pickle(cls, path_list):
        df = pd.concat([pd.read_pickle(path) for path in path_list])
        return cls(df)

    @staticmethod
    def scrape(horse_id_list):

        # horse_idをkeyにしてDataFrame型を格納
        horse_results = {}
        for horse_id in tqdm(horse_id_list):
            try:
                url = 'https://db.netkeiba.com/horse/' + horse_id
                df = pd.read_html(url)[3]
                # 受賞歴がある馬の場合、3番目に受賞歴テーブルが来るため、4番目のデータを取得する
                if df.columns[0] == '受賞歴':
                    df = pd.read_html(url)[4]
                # 出走歴のない馬の場合、テーブル自体がないため、処理を飛ばす
                if df.columns[0] == 0:
                    continue
                df.index = [horse_id] * len(df)
                horse_results[horse_id] = df
                time.sleep(1)

                # メールアドレスとパスワードの指定
                USER = "**********"
                PASS = "**********"

                login_info = {
                    "login_id": USER,
                    "pswd": PASS,
                }
                # セッションを開始
                session = requests.session()

                url_login = "https://regist.netkeiba.com/account/?pid=login&action=auth"

                ses = session.post(url_login, data=login_info)

                res = session.get(url)

                soup = BeautifulSoup(res.content, "html.parser")

                table = soup.find(
                    'table', {'class': 'db_h_race_results'})
                if table is not None:
                    rows = table.find_all("tr")
                    bikou = []
                    time_index = []
                    baba_index = []
                else:
                    continue

                for row in rows:
                    row = [td.text for td in row.find_all(["td", "th"])]
                    bikou.append(row[25].replace('\xa0', '').replace('\n', ''))
                    baba_index.append(row[16].replace(
                        '\xa0', '').replace('\n', ''))
                    time_index.append(row[19].replace(
                        '\xa0', '').replace('\n', ''))

                del bikou[0]
                del time_index[0]
                del baba_index[0]

                df_s = pd.DataFrame()
                df_s["baba_index"] = baba_index
                df_s["time_index"] = time_index
                df_s["bikou"] = bikou
                df_s.index = [horse_id] * len(df_s)
                df = pd.concat([df, df_s], axis=1)
                horse_results[horse_id] = df
                time.sleep(1)
            except IndexError:
                continue
            except Exception as e:
                print(e)
                break
            except:
                break

        # pd.DataFrame型にして一つのデータにまとめる
        horse_results_df = pd.concat(
            [horse_results[key] for key in horse_results])

        return horse_results_df

    def preprocessing(self):
        df = self.horse_results.copy()

        df["date"] = pd.to_datetime(df["日付"])
        df.drop(['日付'], axis=1, inplace=True)

        # 列名を変更,欠損値削除
        df.rename(columns={"オッズ": "odds"}, inplace=True)
        df.dropna(subset=["odds"], inplace=True)

        # 列名を変更,欠損値削除,データ型変更
        df.rename(columns={"人気": "favorite"}, inplace=True)
        df.dropna(subset=["favorite"], inplace=True)
        df["favorite"] = df["favorite"].astype(int)

        # 列名を変更,欠損値削除,データ型変更
        df["着順"] = df["着順"].astype(str)
        df["着順"] = df["着順"].map(lambda x: x.replace("(降)", ""))
        df["着順"] = pd.to_numeric(df["着順"], errors="coerce")
        df.dropna(subset=["着順"], inplace=True)
        df['着順'] = df['着順'].astype(int)
        df.rename(columns={"着順": "rank"}, inplace=True)

        # 列名を変更
        df.rename(columns={"斤量": "weight_j"}, inplace=True)

        # 距離変換
        df["course_len"] = df["距離"].apply(
            lambda x: str(x)[1:]).astype(float) // 100


        # 不要なので削除
        df.drop(["距離"], axis=1, inplace=True)


        # 4コーナーの値のみ取り出す

        def corner(x, n):
            if type(x) != str:  # xが文字列型でなかった場合、ｘをそのまま返す
                return x
            elif n == 4:
                return int(re.findall(r'\d+', x)[-1])
            elif n == 1:
                return int(re.findall(r'\d+', x)[0])

        df['final_corner'] = df['通過'].map(lambda x: corner(x, 4))
        df.dropna(subset=["final_corner"], inplace=True)
        df["final_corner"] = df["final_corner"].astype(int)
        df.drop(["通過"], axis=1, inplace=True)

        # 欠損値削除,列名を変更
        df.dropna(subset=["上り"], inplace=True)
        df.rename(columns={"上り": "last"}, inplace=True)

        # 賞金のNaNを0で埋める
        df['賞金'].fillna(0, inplace=True)
        df.rename(columns={"賞金": "money"}, inplace=True)
        df["money"] = df["money"].astype(int)

        # 数字でない列を欠損値に変換し、平均値で埋める
        df["time_index"] = df["time_index"].replace([''], np.nan)
        df['time_index'] = df["time_index"].replace(['**'], np.nan)
        df["time_index"] = pd.to_numeric(df["time_index"], errors="coerce")
        imr = SimpleImputer()
        df["time_index"] = imr.fit_transform(df[["time_index"]])
        df["time_index"] = df["time_index"].astype(int)

        df.index.name = "horse_id"

        # 加工したものに新しく名前をつける
        self.horse_results = df
        self.target_list = ['date', "course_len",'rank', 'money', "favorite", "last",
                              "odds", 'final_corner', "time_index"]
    # 過去n走分の着順と賞金を計算する関数を定義
    # horse_id_listは学習データor出馬表のhorse_idのリスト,dateは出馬表の日付
    def feature_processing(self, horse_id_list, date):
        target_df = self.horse_results[self.target_list].query(
            'index in @horse_id_list')
        filtered_df = target_df[target_df['date'] < date]
        self.process_dict = {}
        self.process_dict["_1R_before"] = filtered_df.groupby(["horse_id"])[self.target_list].nth(0).add_suffix(
            "_1R_before")
        self.process_dict["_2R_before"] = filtered_df.groupby(["horse_id"])[self.target_list[2:]].nth(1).add_suffix(
            "_2R_before")
        self.process_dict["_3R_before"] = filtered_df.groupby(["horse_id"])[self.target_list[2:]].nth(2).add_suffix(
            "_3R_before")
        self.course_len_all = filtered_df.groupby(level=0)["course_len"].mean().rename("course_len_all")


    def merge(self, results, date):
        # 学習データor出馬表のデータフレームの中から指定した日付のデータフレームを作成する
        df = results[results['date'] == date]
        # 該当レースに出走する競走馬のリストを作成する
        horse_id_list = df["horse_id"]
        # 該当レースに出走する競走馬の過去成績データを作成
        self.feature_processing(horse_id_list, date)
        # left(元々のDF)right(結合したいDF),howは結合方法(指定しないと削除される)
        # 過去成績データと学習データor出馬表のデータフレームと該当馬の過去成績データを結合
        df = df.merge(
            self.process_dict["_1R_before"], left_on='horse_id', right_index=True, how='left')
        df = df.merge(
            self.process_dict["_2R_before"], left_on='horse_id', right_index=True, how='left')
        df = df.merge(
            self.process_dict["_3R_before"], left_on='horse_id', right_index=True, how='left')
        merged_df = df.merge(self.course_len_all, left_on='horse_id', right_index=True, how='left')
        df_tmp_time_index = merged_df[["time_index_1R_before","time_index_2R_before","time_index_3R_before"]]
        df_time_index = df_tmp_time_index.mean(axis='columns') 
        merged_df["time_index_ave"] = df_time_index
        merged_df["time_rank_p"]=merged_df.groupby(level=0)["time_index_ave"].rank(ascending=False,method="max")
        merged_df.drop(["time_index_1R_before","time_index_2R_before","time_index_3R_before","time_index_ave"],inplace=True,axis=1)
        return merged_df

    def merge_all(self, results):
        date_list = results['date'].unique()
        merged_df = pd.concat([self.merge(results, date)
                              for date in tqdm(date_list)])
        return merged_df