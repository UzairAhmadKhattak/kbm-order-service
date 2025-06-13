
import boto3
from botocore.client import Config
from dotenv import dotenv_values
from fastapi import UploadFile
import os
from botocore.exceptions import ClientError

env = dotenv_values('.env')

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
AWS_S3_ENDPOINT_URL = os.environ['AWS_S3_ENDPOINT_URL']


s3_client = boto3.client(
    's3',
    endpoint_url=AWS_S3_ENDPOINT_URL,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    config=Config(signature_version='s3v4')
)

# Ensure bucket exists
try:
    s3_client.head_bucket(Bucket=AWS_STORAGE_BUCKET_NAME)
    print(f"Bucket '{AWS_STORAGE_BUCKET_NAME}' already exists and is accessible.")
except ClientError as e:
    error_code = e.response['Error']['Code']
    if error_code == '404':
        # Bucket does not exist, create it
        try:
            s3_client.create_bucket(Bucket=AWS_STORAGE_BUCKET_NAME)
            print(f"Bucket '{AWS_STORAGE_BUCKET_NAME}' created successfully.")
        except ClientError as create_error:
            print(f"Failed to create bucket: {create_error}")
    elif error_code == '403':
        # Access denied (e.g., bucket owned by another account or insufficient permissions)
        print(f"Access denied to bucket '{AWS_STORAGE_BUCKET_NAME}'. Check permissions.")
    else:
        # Other errors, including BucketAlreadyOwnedByYou
        print(f"Error accessing bucket '{AWS_STORAGE_BUCKET_NAME}': {e}")


async def save_file_to_minio(file: UploadFile,
                             file_name:str,
                             bucket: str = AWS_STORAGE_BUCKET_NAME
                             ) -> str:
    """Save file to MinIO and return the object name."""

    # Read file content
    content = await file.read()

    # Upload to MinIO
    s3_client.put_object(
        Bucket=bucket,
        Key=file_name,
        Body=content,
        ContentType=file.content_type,
        ACL='public-read'
    )
    public_url = f"{AWS_S3_ENDPOINT_URL}/{bucket}/{file_name}"

    return public_url


