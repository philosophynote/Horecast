# 親クラスの読み込み
from .DP import DataProcessor

# データフレーム用
import pandas as pd

# スクレイピング用
import requests
import re
import time
from tqdm.notebook import tqdm
from bs4 import BeautifulSoup


class ShutubaTable(DataProcessor):

    def __init__(self, shutuba_tables):
        super(ShutubaTable, self).__init__()
        self.data = shutuba_tables

    @classmethod
    def scrape(cls, race_id_list, date):
        data = pd.DataFrame()
        for race_id in tqdm(race_id_list):

            url = "https://race.netkeiba.com/race/shutuba.html?race_id=" + race_id
            df = pd.read_html(url)[0]
            df = df.T.reset_index(level=0, drop=True).T

            html = requests.get(url)
            html.encodeing = "EUC-JP"
            soup = BeautifulSoup(html.content, "html.parser")
            race_number = re.findall(
                r'\d+', str(soup.find("span", attrs={"class": "RaceNum"})))
            df["race_number"] = race_number * len(df)
            race_name = soup.find("div", attrs={"class": "RaceName"}).text
            df["race_name"] = [race_name.replace('\n', '')] * len(df)
            texts = soup.find("div", attrs={"class": "RaceData01"}).text
            texts = re.findall(r"\w+", texts)
            for text in texts:
                if "m" in text:
                    # len(df)をかけることでデータフレームの長さだけ内容を追加する
                    df["course_len"] = [
                        int(re.findall(r"\d+", text)[0])] * len(df)
                if text in ["右", "左"]:
                    df["race_turn"] = [text] * len(df)
                if text in ["曇", "晴", "雨", "小雨", "小雪", "雪"]:
                    df["weather"] = [text] * len(df)
                if text in ["良", "稍重", "重"]:
                    df["race_condition"] = [text] * len(df)
                if "不" in text:
                    df["race_condition"] = ["不良"] * len(df)
                if '稍' in text:
                    df["race_condition"] = ['稍重'] * len(df)

                if "芝" in text:
                    df["race_type"] = ["芝"] * len(df)
                if "ダ" in text:
                    df["race_type"] = ["ダ"] * len(df)
                if "障" in text:
                    df["race_type"] = ["障害"] * len(df)
                if text in ["札幌", "函館", "福島", "中山", "東京", "新潟", "中京", "京都", "阪神", "小倉"]:
                    df["race_park"] = [text] * len(df)
            texts_2 = soup.find("div", attrs={"class": "RaceData02"}).text
            texts_2 = re.findall(r"\w+", texts_2)
            for text in texts_2:
                if text in ["札幌", "函館", "福島", "中山", "東京", "新潟", "中京", "京都", "阪神", "小倉"]:
                    df["race_park"] = [text] * len(df)
                df["prize"] = [texts_2[texts_2.index("本賞金")+1]] * len(df)
                df["prize"] = df["prize"].astype(int)

            df["date"] = [date] * len(df)
            

            horse_id_list = []
            horse_td_list = soup.find_all("td", attrs={"class": "HorseInfo"})
            for td in horse_td_list:
                horse_id = re.findall(r"\d+", td.find("a")["href"])[0]
                horse_id_list.append(horse_id)

            jockey_id_list = []
            jockey_td_list = soup.find_all("td", attrs={"class": "Jockey"})
            for td in jockey_td_list:
                jockey_id = re.findall(r"\d+", td.find("a")["href"])[0]
                jockey_id_list.append(jockey_id)

            trainer_id_list = []
            trainer_td_list = soup.find_all("td", attrs={"class": "Trainer"})
            for td in trainer_td_list:
                trainer_id = re.findall(r"\d+", td.find("a")["href"])[0]
                trainer_id_list.append(trainer_id)

            df["horse_id"] = horse_id_list
            df["jockey_id"] = jockey_id_list
            df["trainer_id"] = trainer_id_list

            df.index = [race_id] * len(df)
            df['n_horses'] = df.index.map(df.index.value_counts())
            data = data.append(df)
            time.sleep(1)
        return cls(data)

    def preprocessing(self):
        df = self.data.copy()
        # 性齢を性と年齢に分ける
        df["sex"] = df["性齢"].map(lambda x: str(x)[0])
        df["age"] = df["性齢"].map(lambda x: str(x)[1:]).astype(int)

        # 馬体重を体重と体重変化に分ける
        # df = df[df["馬体重(増減)"] != '--']
        # df["体重"] = df["馬体重(増減)"].str.split("(", expand=True)[0].astype(int)

        df["frame_number"] = df["枠"].astype(int)
        df["horse_number"] = df["馬番"].astype(int)
        df["weight_j"] = pd.to_numeric(df["斤量"], errors="coerce")
        df["weight_j"] = df["weight_j"].astype(float)

        df["date"] = pd.to_datetime(df["date"])

        df["course_len"] = df["course_len"] // 100

        df = df[
            ['n_horses', "frame_number", "horse_number", "weight_j", "race_turn", "course_len", "weather", "race_type", "race_condition", "race_park", "date", "horse_id", "jockey_id",
             "trainer_id", "sex", "age", "prize"]]

        self.data_p = df
