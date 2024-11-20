# For local storage
import os

# For AWS S3 storage 
import boto3

from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv()

LOCAL_STORAGE_PATH = "uploads"


# AWS S3 Config

S3_BUCKET = os.getenv('S3_BUCKET_NAME')
S3_REGION = os.getenv('S3_REGION')

s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=S3_REGION
)

def save_to_local(file):
    if not os.path.exists(LOCAL_STORAGE_PATH):
        os.makedirs(LOCAL_STORAGE_PATH)
        
    filename = secure_filename(file.filename)
    file_path = os.path.join(LOCAL_STORAGE_PATH, filename)
    file.save(file_path)
    
    return file_path

def upload_to_s3(file):
    filename = secure_filename(file.filename)
    s3_client.upload_fileobj(
        file,
        S3_BUCKET,
        filename,
        ExtraArgs={"ContentType": file.content_type}
    )
    
    file_url = f'https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{filename}'
    return file_url