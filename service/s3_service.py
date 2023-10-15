# Code adapted from: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html
import logging

import boto3
from botocore.exceptions import ClientError, NoCredentialsError


def upload_to_s3(file_name, bucket, object_name=None):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
        # Make the object public
        s3_client.put_object_acl(ACL='public-read', Bucket=bucket, Key=object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def is_public_s3_bucket(bucket_name) -> bool:
    try:
        s3 = boto3.client('s3')
        response = s3.head_bucket(Bucket=bucket_name)
    except ClientError as error:
        error_code = int(error.response['Error']['Code'])
        if error_code == 403:
            print("Private Bucket. Forbidden Access! ", bucket_name)
        elif error_code == 404:
            print("Bucket Does Not Exist!", bucket_name)
        return False
    except NoCredentialsError:
        print("No AWS credentials found")
        return False
    return True

def verify_config() -> None:
    import os
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

    if aws_access_key_id and aws_secret_access_key:
        # Use the AWS credentials in your Python code
        print("AWS Access Key:", aws_access_key_id)
        print("AWS Secret Access Key:", aws_secret_access_key)
    else:
        print("AWS credentials not found in environment variables.")
