import json
import re
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    # TODO implement
    source = event['dataObject']['source'] if "source" in event['dataObject'] else None
    source_ref = event['dataObject']['source-ref'] if "source-ref" in event['dataObject'] else None
    
    if source_ref is not None:
        s3 = boto3.client('s3')
        # try:
        source_ref = s3.get_object(Bucket="sagemaker-dialog-label-demo", Key="samples/M1-10.txt")["Body"].read().decode()
        # except ClientError as e:
        #     # AllAccessDisabled error == bucket or object not found
        #     source_ref = str(e)
        #     print(e)
    
    task_object = source if source is not None else source_ref
    
    return {
        "taskInput": {
            "utterance": task_object,
            "labels": str(["Response 1","Response 2","Response 3","Response 4"])
        }
    }
