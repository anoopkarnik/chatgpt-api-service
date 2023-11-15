import os
import logging
import boto3
from botocore.exceptions import NoCredentialsError

logger = logging.getLogger(__name__)

def upload_to_s3(local_file_path,s3_file_path,bucket_name):
    s3_client = boto3.client('s3',aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                      aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),region_name='ap-south-1')
    
    try:
        s3_client.upload_file(local_file_path, bucket_name, s3_file_path)
        logger.info(f"https://{bucket_name}.s3.amazonaws.com/{s3_file_path} Upload Successful")
    except FileNotFoundError:
        logger.info("The file was not found")
    except NoCredentialsError:
        logger.info("Credentials not available")

def read_from_s3(s3_file_path,bucket_name):
    s3_client = boto3.client('s3',aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                      aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),region_name='ap-south-1')
    try:
        if '/' in s3_file_path:
            file_name = s3_file_path.split('/')[-1]
        s3_client.download_file(bucket_name, s3_file_path,os.path.join('data',file_name))
        logger.info(f"Reading file from s3://{bucket_name}/{s3_file_path}")
        audio_stream = open(os.path.join('data',file_name), 'rb')
        return audio_stream

    except FileNotFoundError:
        logger.info("The file was not found")
    except NoCredentialsError:
        logger.info("Credentials not available")