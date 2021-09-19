from forecast.func import insert_race_card
from forecast.race_card import ShutubaTable as st

race_id_list_nmo = ['2021060405{}'.format(str(i).zfill(2)) for i in range(1, 13, 1)]
race_id_list_cmo = ['2021070505{}'.format(str(i).zfill(2)) for i in range(1, 13, 1)]
race_id_list_mo = race_id_list_nmo  + race_id_list_cmo 



rc = st.scrape(race_id_list_mo,"2021/09/20")
rc.data.reset_index(inplace=True)
rc.data.rename(columns={"index":"race_id"},inplace=True)
insert_race_card(rc.data)
print("出馬表をDBに格納しました")