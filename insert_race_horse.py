from forecast.func import insert_race_card
from forecast.race_card import ShutubaTable as st

race_id_list_nst = ['2021060406{}'.format(str(i).zfill(2)) for i in range(1, 13, 1)]
race_id_list_cst = ['2021070506{}'.format(str(i).zfill(2)) for i in range(1, 13, 1)]
race_id_list_st = race_id_list_nst  + race_id_list_cst 



rc = st.scrape(race_id_list_st,"2021/09/25")
rc.data.reset_index(inplace=True)
rc.data.rename(columns={"index":"race_id"},inplace=True)
insert_race_card(rc.data)
print("出馬表をDBに格納しました")