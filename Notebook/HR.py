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
# place_dict = {"札幌": "01", "函館": "02", "福島": "03", "新潟": "04", "東京": "05", "中山": "06", "中京": "07", "京都": "08", "阪神": "09", "小倉": "10", "園田": "11",
#               "名古屋": "11", "高知": "11", "佐賀": "11", "金沢": "11", "笠松": "11", "大井": "11", "盛岡": "11", "水沢": "11", "川崎": "11", "門別": "11", "船橋": "11", "浦和": "11"}
# race_type_dict = {"芝": "芝", "ダ": "ダート", "障": "障害"}
# field_mapping = {"不": "悪", "重": "悪", "稍": "悪", "良": "良"}


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
                USER = "adverdest@gmail.com"
                PASS = "sundai005107D"

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

        # 開催の列中にレース名などの余計な情報が含まれているので、削除し、カテゴリ型に変換
        # df["race_park"] = df["開催"].str.extract(
        #     r"(\D+)")[0].map(place_dict).fillna("11")
        # df.drop(["開催"], axis=1, inplace=True)

        # # ステルスオッズ結合用
        # df["R"] = df["R"].fillna(0)
        # df["R"] = pd.to_numeric(df["R"], errors="coerce")
        # df["R"] = df["R"].astype(int)
        # df["R"] = df["R"].astype(str).str.zfill(2)

        # # 列名を変更
        # df.rename(columns={"天気": "weather"}, inplace=True)

        # # 列名を変更,欠損値削除,データ型変更
        # df.rename(columns={"頭数": "count"}, inplace=True)
        # df.dropna(subset=["count"], inplace=True)
        # df["count"].astype(int)

        # # 列名を変更,欠損値削除,データ型変更
        # df.rename(columns={"枠番": "frame_number"}, inplace=True)
        # df.dropna(subset=["frame_number"], inplace=True)
        # df["frame_number"].astype(int)

        # # 列名を変更
        # df.rename(columns={"馬番": "horse_number"}, inplace=True)

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

        # # 芝・ダート・障害に変換
        # df["race_type"] = df.loc[:, "距離"].str[0].map(race_type_dict)

        # 不要なので削除
        df.drop(["距離"], axis=1, inplace=True)

        # 馬場変換
        # df["race_condition"] = df["馬場"].map(field_mapping)
        # df.drop(["馬場"], axis=1, inplace=True)

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

        # 馬体重処理
        # df['馬体重'] = df["馬体重"].replace(['計不'], np.nan)
        # df.dropna(subset=["馬体重"], inplace=True)
        # df["weight"] = df["馬体重"].str.split("(", expand=True)[0].astype(int)
        # df["weight_c"] = df["馬体重"].str.split(
        #     "(", expand=True)[1].str.split(")", expand=True)[0].astype(int)
        # df.drop(["馬体重"], axis=1, inplace=True)

        # 欠損値削除,列名を変更
        df.dropna(subset=["上り"], inplace=True)
        df.rename(columns={"上り": "last"}, inplace=True)

        # 賞金のNaNを0で埋める
        df['賞金'].fillna(0, inplace=True)
        df.rename(columns={"賞金": "money"}, inplace=True)
        df["money"] = df["money"].astype(int)

        # 0に置換
        # df['baba_index'] = df["baba_index"].replace([''], 0)
        # df['baba_index'] = df["baba_index"].replace(['**'], np.nan)
        # df["baba_index"] = pd.to_numeric(df["baba_index"], errors="coerce")
        # df.dropna(subset=["baba_index"], inplace=True)
        # df["baba_index"] = df["baba_index"].astype(int)

        # df["time_index"] = pd.to_numeric(df["time_index"], errors="ignore")
        # imr = SimpleImputer()
        # imr = imr.fit(df[["time_index"]])
        # df["time_index"] = imr.transform(df[["time_index"]])
        # df["time_index"] = df["time_index"].astype(int)

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

    # def average(self, horse_id_list, date, n_samples="all"):
    #     # 引数で使用したリストに掲載されている馬の過去成績データを引っ張てくる
    #     # query関数は、条件式で変数を使う際、@をつける
    #     target_df = self.horse_results.query('index in @horse_id_list')
    #     # 過去何走分取り出すか指定
    #     if n_samples == 'all':
    #         filtered_df = target_df[target_df['date'] < date]
    #     elif n_samples > 0:
    #         filtered_df = target_df[target_df['date'] < date]. \
    #             sort_values('date', ascending=False).groupby(
    #                 level=0).head(n_samples)
    #     else:
    #         raise Exception('n_samples must be >0')
    #     # 集計して辞書型に入れる
    #     self.average_dict = {}
    #     # 条件なし平均
    #     self.average_dict["non_category"] = filtered_df.groupby(level=0)[self.target_list].mean() \
    #         .add_suffix("_{}R".format(n_samples))
    #     # 条件付き平均
    #     # for column in ["race_type", "race_condition"]:
    #     #     self.average_dict[column] = filtered_df.groupby(["horse_id", column])[self.target_list].mean().add_suffix(
    #     #         "_{}_{}R".format(column, n_samples))

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
        
        df_tmp_money = merged_df[["money_1R_before","money_2R_before","money_3R_before"]]
        df_money = df_tmp_money.mean(axis='columns') 
        merged_df["money_ave"] = df_money
        merged_df["money_rank"]=merged_df.groupby(level=0)["money_ave"].rank(ascending=False,method="max")
        merged_df.drop(["money_1R_before","money_2R_before","money_3R_before"],inplace=True,axis=1)
        df_tmp_final = merged_df[["final_corner_1R_before","final_corner_2R_before","final_corner_3R_before"]]
        df_final = df_tmp_final.mean(axis='columns') 
        merged_df["final_ave"] = df_final
        merged_df["final_rank"]=merged_df.groupby(level=0)["final_ave"].rank(ascending=True,method="max")
        merged_df.drop(["final_corner_1R_before","final_corner_2R_before","final_corner_3R_before"],inplace=True,axis=1)
        df_tmp_last = merged_df[["last_1R_before","last_2R_before","last_3R_before"]]
        df_last = df_tmp_last.mean(axis='columns') 
        merged_df["last_ave"] = df_last
        merged_df["last_rank"]=merged_df.groupby(level=0)["last_ave"].rank(ascending=True,method="max")
        merged_df.drop(["last_1R_before","last_2R_before","last_3R_before"],inplace=True,axis=1)
        merged_df["final_plus_rank"] = merged_df["final_rank"] + merged_df["last_rank"]
        df_tmp_rank = merged_df[["rank_1R_before","rank_2R_before","rank_3R_before"]]
        df_rank = df_tmp_rank.mean(axis='columns') 
        merged_df["rank_ave"] = df_rank
        merged_df["rank_rank"]=merged_df.groupby(level=0)["rank_ave"].rank(ascending=True,method="max")
        merged_df.drop(["rank_1R_before","rank_2R_before","rank_3R_before"],inplace=True,axis=1)
        merged_df.drop(["favorite_1R_before","favorite_2R_before","favorite_3R_before"],inplace=True,axis=1)
        merged_df.drop(["prize","frame_number","money_ave","final_ave","final_rank","last_ave","last_rank","rank_ave"]
                       ,inplace=True,axis=1)
        return merged_df

    def merge_all(self, results):
        date_list = results['date'].unique()
        merged_df = pd.concat([self.merge(results, date)
                              for date in tqdm(date_list)])
        return merged_df
