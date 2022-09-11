import json
import os
import logging
import boto3


logger = logging.getLogger()
logger.setLevel(logging.INFO)

CONNECTION_TABLE = os.environ['CONNECTION_TABLE']
S3_BUCKET_NAME = 'ws-image-test'
S3_ENDPOINT_URL = f'https://{S3_BUCKET_NAME}.s3.ap-northeast-1.amazonaws.com'

def lambda_handler(event, context):

    dynamodb = boto3.resource('dynamodb')
    connection_table = dynamodb.Table(CONNECTION_TABLE)
    
    DOMAIN_NAME = event.get('requestContext', {}).get('domainName')
    STAGE = event.get('requestContext', {}).get('stage')
    WEBSOCKET_ENDPOINT_URL = f'https://{DOMAIN_NAME}/{STAGE}'

    try:
        items = connection_table.scan(ProjectionExpression='connectionId').get('Items')
    except Exception as e:
        logger.error(e)

    selected_image = json.loads(event.get('body', '{}')).get('selectedImage')
    apigw_management = boto3.client('apigatewaymanagementapi', endpoint_url=WEBSOCKET_ENDPOINT_URL)
    for item in items:
        try:
            image_s3 = f'{S3_ENDPOINT_URL}/{selected_image}.png'
            _ = apigw_management.post_to_connection(ConnectionId=item['connectionId'], Data=image_s3)
            logger.info(f'image change to: {image_s3}')
        except Exception as e:
            logger.error(e)
            return {'statusCode': 500, 'body': e}
    
    return {'statusCode': 200, 'body': 'Data sent.'}
