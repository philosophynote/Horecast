# データフレーム用
import pandas as pd

# スクレイピング用
from tqdm.notebook import tqdm
import time



class TrainerResults:
    def __init__(self, trainer_results):
        self.trainer_results = trainer_results

    @classmethod
    def read_pickle(cls, path_list):
        df = pd.concat([pd.read_pickle(path) for path in path_list])
        return cls(df)

    @staticmethod
    def scrape(trainer_id_list):
        data = pd.DataFrame()
        for trainer_id in tqdm(trainer_id_list):
            url = "https://db.netkeiba.com/jockey/result/" + trainer_id
            df = pd.read_html(url)[0]
            df.index = [trainer_id] * len(df)
            data = data.append(df)
            time.sleep(1)
        data = data.T.reset_index().drop("level_0", axis=1).rename(
            columns={"level_1": "trainer_id"}).set_index("trainer_id").T
        return data

    def feature_processing(self, trainer_id_list, date):
        target_df = self.trainer_results.query(
            'index in @trainer_id_list')
        filtered_df = target_df[target_df['year'] < date]
        self.trainer_dict = {}
        self.trainer_dict["_1Y_before_t"] = filtered_df.groupby(
            level=0).nth(0).add_suffix("_1Y_before_t")
        # self.trainer_dict["_2Y_before_t"] = filtered_df.groupby(
        #     level=0).nth(1).add_suffix("_2Y_before_t")
        # self.trainer_dict["_3Y_before_t"] = filtered_df.groupby(
        #     level=0).nth(2).add_suffix("_3Y_before_t")

    def merge(self, results, date):
        # 学習データor出馬表のデータフレームの中から指定した日付のデータフレームを作成する
        df = results[results['date'] == date]
        # 該当レースに出走する競走馬のリストを作成する
        trainer_id_list = df["trainer_id"]
        # 該当レースに出走する競走馬の過去成績データを作成
        self.feature_processing(trainer_id_list, date)
        merged_df = df.merge(
            self.trainer_dict["_1Y_before_t"], left_on='trainer_id', right_index=True, how='left')
        # df = df.merge(
        #     self.trainer_dict["_2Y_before_t"], left_on='trainer_id', right_index=True, how='left')
        # merged_df = df.merge(
        #     self.trainer_dict["_3Y_before_t"], left_on='trainer_id', right_index=True, how='left')
        return merged_df

    def merge_all(self, results):
        date_list = results['date'].unique()
        merged_df = pd.concat([self.merge(results, date)
                              for date in tqdm(date_list)])
        return merged_df
