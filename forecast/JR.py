# データフレーム用
import pandas as pd

# スクレイピング用
import time
import re
import numpy as np
import requests
from bs4 import BeautifulSoup


class JockeyResults:
    def __init__(self, jockey_results):
        self.jockey_results = jockey_results
        self.preprocessing()

    @classmethod
    def read_pickle(cls, path_list):
        df = pd.concat([pd.read_pickle(path) for path in path_list])
        return cls(df)

    @staticmethod
    def scrape(jockey_id_list):
        data = pd.DataFrame()
        for jockey_id in jockey_id_list:
            url = "https://db.netkeiba.com/jockey/result/" + jockey_id
            df = pd.read_html(url)[0]
            df.index = [jockey_id] * len(df)
            data = data.append(df)
            time.sleep(1)
        data = data.T.reset_index().drop("level_0", axis=1).rename(
            columns={"level_1": "jockey_id"}).set_index("jockey_id").T
        return data
    
    def preprocessing(self):
        df = self.jockey_results.copy()
        df = df.replace("累計", np.nan).dropna()
        df = df[["年度","勝率","複勝率","収得賞金(万円)"]]
        df.rename(columns = {"年度":"year","勝率":"win_rate_1","複勝率":"win_rate_3","収得賞金(万円)":"prize"},inplace=True)
        df["year"] = df["year"].astype(str)+"1231"
        df["year"] = pd.to_datetime(df["year"],format='%Y%m%d')
        self.jockey_results = df

    def feature_processing(self, jockey_id_list, date):
        target_df = self.jockey_results.query(
            'index in @jockey_id_list')
        filtered_df = target_df[target_df['year'] < date]
        self.jockey_dict = {}
        self.jockey_dict["_1Y_before_j"] = filtered_df.groupby(
            level=0).nth(0).add_suffix("_1Y_before_j")
        # self.jockey_dict["_2Y_before_j"] = filtered_df.groupby(
        #     level=0).nth(1).add_suffix("_2Y_before_j")
        # self.jockey_dict["_3Y_before_j"] = filtered_df.groupby(
        #     level=0).nth(2).add_suffix("_3Y_before_j")

    def merge(self, results, date):
        # 学習データor出馬表のデータフレームの中から指定した日付のデータフレームを作成する
        df = results[results['date'] == date]
        # 該当レースに出走する競走馬のリストを作成する
        jockey_id_list = df["jockey_id"].unique()
        # 該当レースに出走する競走馬の過去成績データを作成
        self.feature_processing(jockey_id_list, date)
        merged_df = df.merge(
            self.jockey_dict["_1Y_before_j"], left_on='jockey_id', right_index=True, how='left')
        # df = df.merge(
        #     self.jockey_dict["_2Y_before_j"], left_on='jockey_id', right_index=True, how='left')
        # merged_df = df.merge(
        #     self.jockey_dict["_3Y_before_j"], left_on='jockey_id', right_index=True, how='left')
        return merged_df

    def merge_all(self, results):
        date_list = results['date'].unique()
        merged_df = pd.concat([self.merge(results, date) for date in date_list])
        return merged_df
