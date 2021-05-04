import logging
import os
import boto3
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    
    logging.info('Python HTTP trigger function processing a S123 Submit.')

    ses_iam_sk = os.environ['ses_iam_sk']
    ses_iam_ak = os.environ['ses_iam_ak']
    
    recipients = ['']
    sender = ''
    subject = 'Response Submitted!'
    body = 'A response was successfully submitted for your survey!'
    send_email(ses_iam_ak, ses_iam_sk, sender, recipients, subject, body)

    message = "HTTP Trigger processed"
    return func.HttpResponse(message)

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
    logging.info(response)
    logging.info("Email Response ")

    return
