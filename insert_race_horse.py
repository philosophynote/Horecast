from forecast.func import insert_race_card

race_id_list_nmo = ['2021060405{}'.format(str(i).zfill(2)) for i in range(1, 13, 1)]
race_id_list_cmo = ['2021070505{}'.format(str(i).zfill(2)) for i in range(1, 13, 1)]
race_id_list_mo = race_id_list_nmo  + race_id_list_cmo 

insert_race_card(race_id_list_mo)
print("出馬表をDBに格納しました")