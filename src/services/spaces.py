import boto3
from botocore.exceptions import NoCredentialsError
from config.config import get_configs 

async def upload_to_spaces(file, filename):
    try:
        config = get_configs()
        s3 = boto3.client(
            "s3",
            endpoint_url=f"https://{config.do_spaces_region}.digitaloceanspaces.com",
            aws_access_key_id=config.do_spaces_key,
            aws_secret_access_key=config.do_spaces_secret,
        )
        print("===========================")
        print(config.do_spaces_key)
        bucket_name = config.do_spaces_bucket
        object_name = f"uploads/{filename}"

        s3.upload_fileobj(file.file, bucket_name, object_name, ExtraArgs={"ACL": "public-read"})

        return f"https://{bucket_name}.{config.do_spaces_region}.digitaloceanspaces.com/{object_name}"

    except NoCredentialsError:
         return {"error": "Invalid DigitalOcean Spaces credentials"}

async def delete_from_spaces(image_url: str):
    try:
        config = get_configs()
        session = boto3.session.Session()
        client = session.client(
            "s3",
            region_name=config.do_spaces_region, 
            endpoint_url=f"https://{config.do_spaces_region}.digitaloceanspaces.com",
            aws_access_key_id=config.do_spaces_key,
            aws_secret_access_key=config.do_spaces_secret,
        )
        bucket_name = config.do_spaces_bucket
        file_key = image_url.split("/")[-1]

        client.delete_object(Bucket=bucket_name, Key=file_key)
        return True
    except ClientError as e: # type: ignore
        print(f"Error deleting file: {e}")
        return False