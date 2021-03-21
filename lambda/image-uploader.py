import json
import boto3
import os
import logging
import base64
import uuid
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)
s3_client = boto3.client('s3')

s3_bucket = os.environ['BUCKET_NAME']


# main lambda handler method
def handler(event, context):
    payload = json.loads(event['body'])
    # upload image to get s3 URL
    logger.info('upload_image_to_s3 , bucket=' + s3_bucket)
    image = payload['content']
    # check we have file name in input
    if 'fileName' in payload:
        file_name = payload['fileName']
    else:
        # extract file extension from base63 content and create fileName
        file_extension = extract_file_extension(image)
        file_name = f"{str(uuid.uuid1())}.{file_extension}"

    image = image[image.find(",") + 1:]  # get the image data from input
    file_content = base64.b64decode(image)
    s3_upload(file_name, file_content, {})
    # image uploaded successfully return presigned url to download s
    response = {
        'success': True,
        's3_url': create_presigned_url(s3_bucket, file_name)
    }
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(response)
    }


# The response contains the presigned URL
def create_presigned_url(bucket_name, object_name, expiration=3600):
    # Generate a presigned URL for the S3 object
    try:
        return s3_client.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': object_name},
                                                ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        raise


# extract image extension from base 64 encoded file data
# base64_encoded_file syntax as 'image/png;base64,<<imageData>>'
def extract_file_extension(base64_encoded_file):
    if base64_encoded_file.find(';') > -1:
        extension = base64_encoded_file.split(';')[0]
        return extension[extension.find('/') + 1:]
    # default to PNG if we are not able to extract extension or string is not bas64 encoded
    return 'png'


# upload object to s3
def s3_upload(s3_key, file_content, metadata):
    logger.info(f'saving_s3_file , bucket={s3_bucket} , path={s3_key}')
    try:
        response = s3_client.put_object(Body=file_content, Bucket=s3_bucket, Key=s3_key, Metadata=metadata)
        logger.info('S3 Result' + json.dumps(response, indent=2))
    except ClientError as e:
        logging.error(e)
        raise
