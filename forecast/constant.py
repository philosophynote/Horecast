import datetime

dt_now = datetime.datetime.now()

DATA_PATH_NAME = 'data'
HORSE_RESULT_PATH_NAME = 'horse_results'
PEDS_PATH_NAME = 'peds'
HORSE_RESULT_OLD_ALL_FILENAME = f'horse_results_all_{str(dt_now.year) + str(dt_now.month).zfill(2) + str(dt_now.day)}.pickle'
HORSE_RESULT_NEW_ALL_FILENAME = 'horse_results_all.pickle'
PEDS_OLD_ALL_FILENAME = f'peds_all_{str(dt_now.year) + str(dt_now.month).zfill(2) + str(dt_now.day)}.pickle'
PEDS_NEW_ALL_FILENAME = 'peds_all.pickle'

JOCKEY_FILENAME = 'jockey_results_all.pickle'
TRAINER_FILENAME = 'trainer_results_all.pickle'
RESULT_FILENAME = 'race_results_all.pickle'

INPUT_FILENAME = f"input_data_{str(dt_now.year) + str(dt_now.month).zfill(2) + str(dt_now.day)}.csv"

