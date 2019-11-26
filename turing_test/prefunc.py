import json
import re
import boto3
from botocore.exceptions import ClientError


def get_object(s3, s3Uri):
    m = re.match(r"s3:\/\/(.+?)\/(.+)", s3Uri)
    bucket, key = m.group(1), m.group(2)
    return s3.get_object(Bucket=bucket, Key=key)["Body"].read().decode()


def lambda_handler(event, context):
    s3 = boto3.client('s3')

    # HITs
    source_ids = list(map(int, event['dataObject']['source-ids'].split(",")))
    print(source_ids)

    # Predictions
    predictions = event['dataObject']['predictions']
    predictions = get_object(s3, predictions)
    lines = predictions.split("\n")
    tests = [json.loads(line) for line in lines if len(line) > 0]
    tests = [test for test in tests if test['id'] in source_ids]

    return {
        "taskInput": {
            "data": tests,
            "labels": str(["AI", "Human"])
        }
    }
