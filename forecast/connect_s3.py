import boto3
import json
import io
import bz2
import pickle
import datetime
import pandas as pd
from .func import calc_predict, select_sql_r, select_sql_h, making_predtable, insert_predtable
from django.conf import settings
from .HR import HorseResults as HR
from .Ped import Peds
from .constant import *
from pathlib import Path


def update_data(old, new):
    """
    Parameters:
    ----------
    old : pandas.DataFrame
        古いデータ
    new : pandas.DataFrame
        新しいデータ
    """

    filtered_old = old[~old.index.isin(new.index)]
    return pd.concat([filtered_old, new])

def download_csv():
    s3 = boto3.resource('s3', aws_access_key_id = settings.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY,
                        region_name = settings.AWS_S3_REGION_NAME)
    
    src_obj = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, "inputdata_0807.csv")
    body_in = src_obj.get()['Body'].read().decode(
        settings.SRC_FILE_ENCODING
    )
    buffer_in = io.StringIO(body_in)
    df_in = pd.read_csv(
        buffer_in,
        lineterminator='\n'
    )
    filename = bz2.BZ2File('forecast/HorecastModel_20220326.bz2', 'rb', 'rb')
    lgb_clf = pickle.load(filename)
    pred, proba = calc_predict(lgb_clf, df_in)
    race_df = select_sql_r(df_in, "race")
    horse_df = select_sql_h(df_in, "horse")
    pred_table = race_df.merge(horse_df, left_on="race_id",
                                right_on="race_id", how="left")
    pred_table = making_predtable(pred, proba, pred_table)
    insert_predtable(pred_table)
    
def create_horse_data(df):
  s3 = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                      region_name=AWS_S3_REGION_NAME)
  horse_id_list = df["horse_id"].unique()
  print("出走馬のデータ収集を開始します")
  horse_results_new = HR.scrape(horse_id_list)
  horse_results_old_all = pickle.loads(s3.Bucket(AWS_STORAGE_BUCKET_NAME).Object(
      f'{DATA_PATH_NAME}/{HORSE_RESULT_NEW_ALL_FILENAME}').get()['Body'].read())
  horse_results_new_all = update_data(horse_results_old_all, horse_results_new)
  # ディレクトリがないとエラーになるため作成
  dir = Path(f'{DATA_PATH_NAME}/{HORSE_RESULT_PATH_NAME}')
  dir.mkdir(parents=True, exist_ok=True)
  horse_results_old_all.to_pickle(
      f'{DATA_PATH_NAME}/{HORSE_RESULT_PATH_NAME}/{HORSE_RESULT_OLD_ALL_FILENAME}')
  dir = Path(f'{DATA_PATH_NAME}')
  dir.mkdir(parents=True, exist_ok=True)
  horse_results_new_all.to_pickle(
      f'{DATA_PATH_NAME}/{HORSE_RESULT_NEW_ALL_FILENAME}')
  s3.Object(AWS_STORAGE_BUCKET_NAME, f'{DATA_PATH_NAME}/{HORSE_RESULT_PATH_NAME}/{HORSE_RESULT_OLD_ALL_FILENAME}').put(
      Body=open(f'{DATA_PATH_NAME}/{HORSE_RESULT_PATH_NAME}/{HORSE_RESULT_OLD_ALL_FILENAME}', 'rb'))
  s3.Object(AWS_STORAGE_BUCKET_NAME, f'{DATA_PATH_NAME}/{HORSE_RESULT_NEW_ALL_FILENAME}').put(
      Body=open(f'{DATA_PATH_NAME}/{HORSE_RESULT_NEW_ALL_FILENAME}', 'rb'))


def read_horse_result():
  s3 = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                      region_name=AWS_S3_REGION_NAME)
  horse_results_all = pickle.loads(s3.Bucket(AWS_STORAGE_BUCKET_NAME).Object(
      f'{DATA_PATH_NAME}/{HORSE_RESULT_NEW_ALL_FILENAME}').get()['Body'].read())
  return horse_results_all


def read_peds():
  s3 = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                      region_name=AWS_S3_REGION_NAME)
  peds_all = pickle.loads(s3.Bucket(AWS_STORAGE_BUCKET_NAME).Object(f'{PEDS_PATH_NAME}/{PEDS_NEW_ALL_FILENAME}').get()['Body'].read())
  return peds_all
  

def create_peds(peds_new):
  s3 = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                      region_name=AWS_S3_REGION_NAME)
  peds_old = pickle.loads(s3.Bucket(AWS_STORAGE_BUCKET_NAME).Object(
      f'{DATA_PATH_NAME}/{PEDS_NEW_ALL_FILENAME}').get()['Body'].read())
  peds = update_data(peds_old, peds_new)
  # ディレクトリがないとエラーになるため作成
  dir = Path(f'{DATA_PATH_NAME}/{PEDS_PATH_NAME}')
  dir.mkdir(parents=True, exist_ok=True)
  peds_old.to_pickle(
      f'{DATA_PATH_NAME}/{PEDS_PATH_NAME}/{PEDS_OLD_ALL_FILENAME}')
  s3.Object(AWS_STORAGE_BUCKET_NAME, f'{DATA_PATH_NAME}/{PEDS_PATH_NAME}/{PEDS_OLD_ALL_FILENAME}').put(
      Body=open(f'{DATA_PATH_NAME}/{PEDS_PATH_NAME}/{PEDS_OLD_ALL_FILENAME}', 'rb'))
  # ディレクトリがないとエラーになるため作成
  dir = Path(f'{DATA_PATH_NAME}/{PEDS_PATH_NAME}')
  dir.mkdir(parents=True, exist_ok=True)
  peds.to_pickle(f'{DATA_PATH_NAME}')
  s3.Object(AWS_STORAGE_BUCKET_NAME, f'{DATA_PATH_NAME}/{PEDS_NEW_ALL_FILENAME}').put(
      Body=open(f'{DATA_PATH_NAME}/{PEDS_NEW_ALL_FILENAME}', 'rb'))

def read_jockey():
  s3 = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                      region_name=AWS_S3_REGION_NAME)
  jockey_result = pickle.loads(s3.Bucket(AWS_STORAGE_BUCKET_NAME).Object(
            f'{DATA_PATH_NAME}/{JOCKEY_FILENAME}').get()['Body'].read())
  return jockey_result


def read_trainer():
  s3 = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                      region_name=AWS_S3_REGION_NAME)
  trainer_result = pickle.loads(s3.Bucket(AWS_STORAGE_BUCKET_NAME).Object(
      f'{DATA_PATH_NAME}/{TRAINER_FILENAME}').get()['Body'].read())
  return trainer_result

def read_race_result():
   s3 = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                       aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                       region_name=AWS_S3_REGION_NAME)
   race_result = pickle.loads(s3.Bucket(AWS_STORAGE_BUCKET_NAME).Object(
       f'{DATA_PATH_NAME}/{RESULT_FILENAME}').get()['Body'].read())
   return race_result

def create_inputfile(df):
    s3 = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                        region_name=AWS_S3_REGION_NAME)
    df.to_csv(INPUT_FILENAME,index=False)
    s3.Object(AWS_STORAGE_BUCKET_NAME, INPUT_FILENAME).put(
        Body=open(INPUT_FILENAME, 'rb'))
    print("CSVデータの保存が終了しました")