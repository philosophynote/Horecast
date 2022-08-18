import datetime
from forecast.func import insert_race_card
from forecast.race_card import ShutubaTable as st
from forecast.connect_s3 import create_horse_data, read_horse_result, read_peds, create_peds, read_jockey, read_trainer, read_race_result, create_inputfile
from forecast.HR import HorseResults as HR
from forecast.Ped import Peds
from forecast.JR import JockeyResults as JR
from forecast.TR import TrainerResults as TR
from forecast.Result import Results
from forecast.constant import *

race_id_list_a = ['2022040204{}'.format(
    str(i).zfill(2)) for i in range(1, 13, 1)]
race_id_list_b = ['2022010106{}'.format(
    str(i).zfill(2)) for i in range(1, 13, 1)]
# race_id_list_c = ['2022040108{}'.format(
#     str(i).zfill(2)) for i in range(1, 13, 1)]
# race_id_list = race_id_list_a + race_id_list_b + race_id_list_c
# race_id_list = race_id_list_a  + race_id_list_b 
race_id_list = ['202204020401','202204020402']

dt_now = datetime.datetime.now()
rc = st.scrape(race_id_list, f'{str(dt_now.year)}/{str(dt_now.month).zfill(2)}/{str(dt_now.day).zfill(2)}')
rc.data.reset_index(inplace=True)
rc.data.rename(columns={"index":"race_id"},inplace=True)
insert_race_card(rc.data)
print("出馬表をDBに格納しました")

rc.preprocessing()

create_horse_data(rc.data_p.head())
horse_results_all = read_horse_result()
hr = HR(horse_results_all)
rc.merge_horse_results(hr)
print("処理が終了しました")

peds_all = read_peds()
p = Peds(peds_all)
p.encode()
rc.merge_peds(p.peds_e)
try:
    peds_new = Peds.scrape(rc.no_peds)
    create_peds(peds_new)
except ValueError:
    print("スクレイピングする対象がありませんでした")
    pass
else:
    print('出馬表の血統データのスクレイピングが終了しました')
jockey_result = read_jockey()
jr = JR(jockey_result)
rc.merge_jockey(jr)
print("騎手データ処理が終了しました")

trainer_result = read_trainer()
tr = JR(trainer_result)
rc.merge_trainer(tr)
print("調教師データ処理が終了しました")

race_result = read_race_result()

r = Results(race_result)
r.preprocessing()


r.merge_horse_results(hr)

p.encode()
r.merge_peds(p.peds_e)

r.merge_jockey(jr)

r.merge_trainer(tr)
r.process_categorical()

rc.process_categorical(r.le_jockey, r.le_trainer, r.data_pe)

create_inputfile(rc.data_c)
