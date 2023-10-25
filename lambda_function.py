import json
import os

def lambda_handler(event, context):
    # TODO implement
	os.system('ls')
	os.system('yum list installed | grep wgrib2')

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
