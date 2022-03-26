from forecast.func import insert_race_card
from forecast.race_card import ShutubaTable as st

race_id_list_a = ['2022060301{}'.format(
    str(i).zfill(2)) for i in range(1, 13, 1)]
race_id_list_b = ['2022090201{}'.format(
    str(i).zfill(2)) for i in range(1, 13, 1)]
race_id_list_c = ['2022070205{}'.format(
    str(i).zfill(2)) for i in range(1, 13, 1)]
race_id_list = race_id_list_a + race_id_list_b + race_id_list_c
# race_id_list = race_id_list_a  + race_id_list_b 



rc = st.scrape(race_id_list,"2022/03/26")
rc.data.reset_index(inplace=True)
rc.data.rename(columns={"index":"race_id"},inplace=True)
insert_race_card(rc.data)
print("出馬表をDBに格納しました")
