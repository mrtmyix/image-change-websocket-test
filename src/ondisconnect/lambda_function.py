import json
import os
import logging
import boto3


def lambda_handler(event, context):
    
    dynamodb = boto3.resource('dynamodb')
    connections = dynamodb.Table(os.environ['CONNECTION_TABLE'])

    connection_id = event.get('requestContext',{}).get('connectionId')
    result = connections.delete_item(Key={'connectionId': connection_id})
    return { 'statusCode': 200, 'body': 'ok' }
