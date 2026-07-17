import boto3
from utils.logger import get_logger
BUCKET_NAME = 'music-intelligence-etl'
s3 = boto3.client('s3')

logger = get_logger("s3_uploader")

def export_to_s3(json_path, s3_key):
    """
    Uploads JSON data to an S3 bucket.

    Parameters:
    - json_path: The path to the JSON file to upload.
    - s3_key: The key under which to store the file in the S3 bucket.
    """

    try:
        with open(json_path, 'rb') as f:
            s3.put_object(Bucket=BUCKET_NAME, Key=s3_key, Body=f)
        logger.info(f"Successfully uploaded {s3_key} to {BUCKET_NAME}.")
    except Exception as e:
        logger.error(f"Error uploading {s3_key} to {BUCKET_NAME}: {e}") 
        raise

