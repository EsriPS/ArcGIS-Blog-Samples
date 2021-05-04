import json
import os
import boto3
import urllib.request
import urllib.parse

def lambda_handler(event, context):
    print('Checking if request is valid...')
    
    # Get environment variables
    portalUrl = os.environ['portalUrl']
    ses_iam_sk = os.environ['ses_iam_sk']
    ses_iam_ak = os.environ['ses_iam_ak']
    
    # Get the JSON body of the request
    body = json.loads(event['body'])

    # Check if the portal and user info supplied in the S123 request is valid
    if body['portalInfo']['url'] == portalUrl:
        
        # Get request parameters
        selfUrl = portalUrl + '/sharing/rest/portals/self'
        payload = {
            'token': body['portalInfo']['token'],
            'f': 'json'
        }
        
        # Send POST request
        data = urllib.parse.urlencode(payload)
        data = data.encode('ascii')
        req = urllib.request.Request(selfUrl, data)
        
        # Read the response
        res = urllib.request.urlopen(req)
        res_body = res.read()
        res_json = json.loads(res_body.decode("utf-8"))
        print(f'Request to {selfUrl} was successful.')
        
        # Validate username
        print('Validating user information...')
        if body['userInfo']['username'] == res_json['user']['username']:
            print(f"The username {body['userInfo']['username']} is valid. Processing webhook...")
            
            recipients = ['']
            sender = ''
            subject = 'Response Submitted!'
            body = 'A response was successfully submitted for your survey!'
            send_email(ses_iam_ak, ses_iam_sk, sender, recipients, subject, body)
    
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': 'https://survey123.arcgis.com',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                },
                'body': json.dumps('Email Triggered!')
            }
    else:
        print('Portal URL does not match. Ending script.')
        
        return {
            'statusCode': 403,
            'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': 'https://survey123.arcgis.com',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps('Unauthorized!')
        }

def send_email(ses_ak, ses_sk, sender, recipients, subject, body):
    CHARSET = "UTF-8"

    client = boto3.client(
        'sesv2',
        aws_access_key_id=ses_ak,
        aws_secret_access_key=ses_sk,
        region_name='us-east-1'
    )

    response = client.send_email(
        FromEmailAddress=sender,
        Destination={
            'ToAddresses': recipients
        },
        Content={
            'Simple': {
                'Body': {
                    'Text': {
                        'Charset': CHARSET,
                        'Data': body
                    }
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': subject
                }
            }
        }
    )

    return
