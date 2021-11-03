import pandas as pd



class DataProcessor:
    def __init__(self):
        self.data = pd.DataFrame()  # raw data
        self.data_p = pd.DataFrame()  # after preprocessing
        self.data_h = pd.DataFrame()  # after merging horse_results
        self.data_pe = pd.DataFrame()  # after merge_peds
        self.data_j = pd.DataFrame()  # after merge_jockey
        self.data_t = pd.DataFrame()  # after merge_jockey
        self.data_c = pd.DataFrame()  # after LabelEncoder

    def merge_horse_results(self, hr):
        # 馬の過去成績データから、n_sample_listで指定されたレース分の特徴量の平均を追加してdata_hに返す
        self.data_h = self.data_p.copy()
        self.data_h = hr.merge_all(self.data_h)
        self.data_h['interval'] = (
            self.data_h['date'] - self.data_h['date_1R_before']).dt.days
        self.data_h['course_len_dif'] = (
            self.data_h['course_len'] - self.data_h['course_len_1R_before'])
        self.data_h.drop(
            ['date_1R_before', 'course_len_1R_before'], axis=1, inplace=True)

    def merge_peds(self, peds):
        # 5世代分の血統データを追加してdata_peに返す
        self.data_pe = \
            self.data_h.merge(peds, left_on='horse_id', right_index=True,
                              how='left')
        self.no_peds = self.data_pe[self.data_pe['peds_0'].isnull(
        )]['horse_id'].unique()
        if len(self.no_peds) > 0:
            print('scrape peds at horse_id_list "no_peds"')
    
    def merge_jockey(self, jr):
        self.data_j = self.data_pe.copy()
        self.data_j = jr.merge_all(self.data_j)
        self.data_j.drop(
           ['year_1Y_before_j'], axis=1, inplace=True)

    def merge_trainer(self, tr):
        self.data_t = self.data_j.copy()
        self.data_t = tr.merge_all(self.data_t)
        self.data_t.drop(
            ['year_1Y_before_t'], axis=1, inplace=True)

    def process_categorical(self, le_jockey, le_trainer, results_m):
        df = self.data_t.copy()
        race_turn = results_m["race_turn"].unique()
        weathers = results_m["weather"].unique()
        race_types = results_m["race_type"].unique()
        ground_state = results_m["race_condition"].unique()
        sexes = results_m["sex"].unique()
        place = results_m["race_park"].unique()

        df["race_turn"] = pd.Categorical(df["race_turn"], race_turn)
        df["weather"] = pd.Categorical(df["weather"], weathers)
        df["race_type"] = pd.Categorical(df["race_type"], race_types)
        df["race_condition"] = pd.Categorical(
            df["race_condition"], ground_state)
        df["sex"] = pd.Categorical(df["sex"], sexes)
        df["race_park"] = pd.Categorical(df["race_park"], place)
  
        
        df = pd.get_dummies(df, columns=[
                            "race_turn", "weather", "race_type", "race_condition", "sex", "race_park"])

        self.data_c = df
