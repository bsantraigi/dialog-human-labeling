import json
import sys
from s3_helper import S3Client
import boto3
import re


"""
lambda_handler receives following event object
{
  "version": "2018-10-06",
  "labelingJobArn": "arn:aws:sagemaker:us-east-1:986216541610:labeling-job/dialog-labeling-demo9-private",
  "payload": {
    "s3Uri": "s3://sagemaker-dialog-label-demo/dialog-labeling-demo9-private/annotations/consolidated-annotation/consolidation-request/iteration-1/2019-10-27_08:56:48.json"
  },
  "labelAttributeName": "dialog-labeling-demo9-private",
  "roleArn": "arn:aws:iam::986216541610:role/service-role/AmazonSageMaker-ExecutionRole-20191027T040862",
  "outputConfig": "s3://sagemaker-dialog-label-demo/dialog-labeling-demo9-private/annotations"
}



"""

def get_object(s3, s3Uri):
    m = re.match(r"s3:\/\/(.+?)\/(.+)", s3Uri)
    bucket, key = m.group(1), m.group(2)
    return s3.get_object(Bucket=bucket, Key=key)["Body"].read().decode()

def lambda_handler(event, context):
    labeling_job_arn = event["labelingJobArn"]
    label_attribute_name = event["labelAttributeName"]

    label_categories = None
    if "label_categories" in event:
        label_categories = event["labelCategories"]
        print(" Label Categories are : " + label_categories)

    payload = event["payload"]
    role_arn = event["roleArn"]

    output_config = None  # Output s3 location. You can choose to write your annotation to this location
    if "outputConfig" in event:
        output_config = event["outputConfig"]

    # If you specified a KMS key in your labeling job, you can use the key to write
    # consolidated_output to s3 location specified in outputConfig.
    kms_key_id = None
    if "kmsKeyId" in event:
        kms_key_id = event["kmsKeyId"]

    s3 = boto3.client('s3')
    # try:
    s3_ref = payload['s3Uri']

    consolidation_request = json.loads(get_object(s3, s3_ref))

    print("Consolidation Request:", json.dumps(consolidation_request, indent=2))

    # return {
    #     'event': event,
    #     'bucket': bucket,
    #     'key': key,
    #     'request': json.dumps(consolidation_request, indent="2")
    # }

    # Create s3 client object
    # s3_client = S3Client(role_arn, kms_key_id)

    # Perform consolidation
    return do_consolidation(labeling_job_arn, consolidation_request, label_attribute_name, s3)


def do_consolidation(labeling_job_arn, payload, label_attribute_name, s3):
    """
        Core Logic for consolidation

    :param labeling_job_arn: labeling job ARN
    :param payload:  payload data for consolidation
    :param label_attribute_name: identifier for labels in output JSON
    :param s3_client: S3 helper class
    :return: output JSON string
    """

    # Payload data contains a list of data objects.
    # Iterate over it to consolidate annotations for individual data object.
    consolidated_output = []
    success_count = 0  # Number of data objects that were successfully consolidated
    failure_count = 0  # Number of data objects that failed in consolidation

    for p in range(len(payload)):
        response = None
        try:
            dataset_object_id = payload[p]['datasetObjectId']
            log_prefix = "[{}] data object id [{}] :".format(labeling_job_arn, dataset_object_id)
            print("{} Consolidating annotations BEGIN ".format(log_prefix))

            annotations = payload[p]['annotations']
            print("{} Received Annotations from all workers {}".format(log_prefix, annotations))

            # Iterate over annotations. Log all annotation to your CloudWatch logs
            for i in range(len(annotations)):
                worker_id = annotations[i]["workerId"]
                annotation_content = annotations[i]['annotationData'].get('content')
                annotation_s3_uri = annotations[i]['annotationData'].get('s3uri')
                annotation = annotation_content if annotation_s3_uri is None else get_object(s3, annotation_s3_uri)
                annotation_from_single_worker = json.loads(annotation)

                print("{} Received Annotations from worker [{}] is [{}]"
                      .format(log_prefix, worker_id, annotation_from_single_worker))

            # Notice that, no consolidation is performed, worker responses are combined and appended to final output
            # You can put your consolidation logic here
            consolidated_annotation = {"annotationsFromAllWorkers": annotations}  # TODO : Add your consolidation logic

            # Build consolidation response object for an individual data object
            response = {
                "datasetObjectId": dataset_object_id,
                "consolidatedAnnotation": {
                    "content": {
                        label_attribute_name: consolidated_annotation
                    }
                }
            }

            success_count += 1
            print("{} Consolidating annotations END ".format(log_prefix))

            # Append individual data object response to the list of responses.
            if response is not None:
                consolidated_output.append(response)

        except:
            failure_count += 1
            print(" Consolidation failed for dataobject {}".format(p))
            print(" Unexpected error: Consolidation failed." + str(sys.exc_info()[0]))

    print("Consolidation Complete. Success Count {}  Failure Count {}".format(success_count, failure_count))

    print(" -- Consolidated Output -- ")
    print(consolidated_output)
    print(" ------------------------- ")
    return consolidated_output

