import json
import os
import sys
import logging
import boto3
import botocore


def lambda_handler(event, context):

    dynamodb = boto3.resource('dynamodb')
    connections = dynamodb.Table(os.environ['CONNECTION_TABLE'])

    post_data = json.loads(event.get('body', '{}')).get('data')
    domain_name = event.get('requestContext',{}).get('domainName')
    stage       = event.get('requestContext',{}).get('stage')

    items = connections.scan(ProjectionExpression='connectionId').get('Items')
    if items is None:
        return { 'statusCode': 500,'body': 'something went wrong' }

    apigw_management = boto3.client('apigatewaymanagementapi', endpoint_url=F"https://{domain_name}/{stage}")
    for item in items:
        try:
            _ = apigw_management.post_to_connection(ConnectionId=item['connectionId'], Data=f'https://ws-image-test.s3.ap-northeast-1.amazonaws.com/{post_data}.png')
        except Exception as e:
            print(e)
    return { 'statusCode': 200,'body': 'ok' }
