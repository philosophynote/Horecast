from forecast.func import insert_race_card
from forecast.race_card import ShutubaTable as st

race_id_list_a = ['2021060505{}'.format(str(i).zfill(2)) for i in range(1, 13, 1)]
race_id_list_b = ['2021090605{}'.format(str(i).zfill(2)) for i in range(1, 13, 1)]
race_id_list_c = ['2021070605{}'.format(str(i).zfill(2)) for i in range(1, 13, 1)]
race_id_list = race_id_list_a  + race_id_list_b + race_id_list_c
# race_id_list = race_id_list_a  + race_id_list_b 



rc = st.scrape(race_id_list,"2021/12/18")
rc.data.reset_index(inplace=True)
rc.data.rename(columns={"index":"race_id"},inplace=True)
insert_race_card(rc.data)
print("出馬表をDBに格納しました")