from forecast.func import insert_race_card
from forecast.race_card import ShutubaTable as st

race_id_list_nsn = ['2021060407{}'.format(str(i).zfill(2)) for i in range(1, 13, 1)]
race_id_list_csn = ['2021070507{}'.format(str(i).zfill(2)) for i in range(1, 13, 1)]
race_id_list_sn = race_id_list_nsn  + race_id_list_csn 



rc = st.scrape(race_id_list_sn,"2021/09/26")
rc.data.reset_index(inplace=True)
rc.data.rename(columns={"index":"race_id"},inplace=True)
insert_race_card(rc.data)
print("出馬表をDBに格納しました")