import os
import logging
import boto3


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

CONNECTION_TABLE = os.environ['CONNECTION_TABLE']

def lambda_handler(event, context):

    dynamodb = boto3.resource('dynamodb')
    connection_table = dynamodb.Table(CONNECTION_TABLE)
    
    connection_id = event.get('requestContext', {}).get('connectionId')
    try:
        connection_table.put_item(Item={'connectionId': connection_id})
        logger.info(f'connected id: {connection_id}')
    except Exception as e:
        logger.error(e)
        return {'statusCode': 500, 'body': f'Failed to connect: {e}'}

    return {'statusCode': 200, 'body': 'Connected.'}
