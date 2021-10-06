import boto3
import io
import pandas as pd
from collections import deque


class SthreeController():
    def __init__(self, accesskey, secretkey, region,
                 bucket_name,):
        self.accesskey = accesskey
        self.secretkey = secretkey
        self.region = region
        self.bucket_name = bucket_name


    def read_result(self):
        s3 = boto3.resource('s3',aws_access_key_id=self.accesskey,
                          aws_secret_access_key=self.secretkey,
                          region_name=self.region)
        buffer_0 = io.BytesIO()
        object_0 = s3.Object(self.bucket_name,"output/result_1.snappy.parquet")
        object_0.download_fileobj(buffer_0)
        df_0 = pd.read_parquet(buffer_0)
        buffer_1 = io.BytesIO()
        object_1 = s3.Object(self.bucket_name,"output/result_2.snappy.parquet")
        object_1.download_fileobj(buffer_1)
        df_1 = pd.read_parquet(buffer_1)
        df = pd.concat([df_0, df_1],ignore_index=True)
        return df

    def read_peds(self):
        s3 = boto3.resource('s3',aws_access_key_id=self.accesskey,
                          aws_secret_access_key=self.secretkey,
                          region_name=self.region)
        buffer_0 = io.BytesIO()
        object_0 = s3.Object(self.bucket_name,"output/peds.snappy.parquet")
        object_0.download_fileobj(buffer_0)
        df = pd.read_parquet(buffer_0)
        # df = pd.concat([df_0, df_1, df_2],ignore_index=True)


    

        return df

