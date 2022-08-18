import boto3
import json
import io
import bz2
import pickle
import datetime
import pandas as pd
from .func import calc_predict, select_sql_r, select_sql_h, making_predtable, insert_predtable
from django.conf import settings

class ConnectS3():
  def __init__(self):
    self.accesskey = settings.AWS_ACCESS_KEY_ID
    self.secretkey = settings.AWS_SECRET_ACCESS_KEY
    self.region = settings.AWS_S3_REGION_NAME
    self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    self.src_file_encoding = settings.SRC_FILE_ENCODING

  @classmethod
  def download_csv(self):
      s3 = boto3.resource('s3', aws_access_key_id=self.accesskey,
                          aws_secret_access_key=self.secretkey,
                          region_name=self.region)
      
      src_obj = s3.Object(self.bucket_name, "inputdata_0807.csv")
      body_in = src_obj.get()['Body'].read().decode(
          self.src_file_encoding
      )
      buffer_in = io.StringIO(body_in)
      df_in = pd.read_csv(
          buffer_in,
          lineterminator='\n'
      )
      filename = bz2.BZ2File('HorecastModel_20220326.bz2', 'rb')
      lgb_clf = pickle.load(filename)
      pred, proba = calc_predict(lgb_clf, df_in)
      race_df = select_sql_r(df_in, "race")
      horse_df = select_sql_h(df_in, "horse")
      pred_table = race_df.merge(horse_df, left_on="race_id",
                                 right_on="race_id", how="left")
      pred_table = making_predtable(pred, proba, pred_table)
      insert_predtable(pred_table)
