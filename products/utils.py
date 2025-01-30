import boto3
from botocore.exceptions import NoCredentialsError

from decouple import config
# Initialize S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id=config("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=config("AWS_SECRET_ACCESS_KEY"),
    region_name=config("AWS_S3_REGION_NAME")
)

import urllib.parse

def upload_image_to_s3(image_file, image_name):
    try:
        # URL encode the image name to ensure it's correctly formatted for S3
        encoded_image_name = urllib.parse.quote(image_name)
        
        # Upload the image to the specified S3 bucket
        s3.upload_fileobj(
            image_file,
            config("AWS_STORAGE_BUCKET_NAME"),
            encoded_image_name,
            ExtraArgs={'ContentType': image_file.content_type}
        )
        
        # Construct the URL for the uploaded image
        
        image_url = f"https://{config('AWS_STORAGE_BUCKET_NAME')}.s3.{config('AWS_S3_REGION_NAME')}.amazonaws.com/{encoded_image_name}"

        print(image_url)
        return image_url
    except NoCredentialsError:
        return None
    except Exception as e:
        return None
