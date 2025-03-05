import boto3
from botocore.exceptions import NoCredentialsError
from config.config import get_configs # Import settings

async def upload_to_spaces(file, filename):
    try:
        config = get_configs()
        s3 = boto3.client(
            "s3",
            endpoint_url=f"https://{config.do_spaces_region}.digitaloceanspaces.com",
            aws_access_key_id=config.do_spaces_key,
            aws_secret_access_key=config.do_spaces_secret,
        )

        bucket_name = config.do_spaces_bucket
        object_name = f"uploads/{filename}"

        # Upload file to DigitalOcean Spaces
        s3.upload_fileobj(file.file, bucket_name, object_name, ExtraArgs={"ACL": "public-read"})

        return f"https://{bucket_name}.{config.do_spaces_region}.digitaloceanspaces.com/{object_name}"

    except NoCredentialsError:
         return {"error": "Invalid DigitalOcean Spaces credentials"}
