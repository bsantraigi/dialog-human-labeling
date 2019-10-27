"""Sample PreHumanTaskLambda ( pre-processing lambda) for custom labeling jobs.

For custom AWS SageMaker Ground Truth Labeling Jobs, you have to specify a PreHumanTaskLambda (pre-processing lambda).
AWS SageMaker invokes this lambda for each item to be labeled. Output of this lambda, is merged with the specified
custom UI template. This code assumes that specified custom template have only one placeholder "taskObject".
If your UI template have more parameters, please modify output of this lambda.


Parameters
----------
event: dict, required
    Content of event looks some thing like following

    {
        "version":"2018-10-16",
        "labelingJobArn":"<your labeling job ARN>",
        "dataObject":{
            "source-ref":"s3://<your bucket>/<your keys>/awesome.jpg"
        }
    }

    As SageMaker product evolves, content of event object will change. For a latest version refer following URL

    Event doc: https://docs.aws.amazon.com/sagemaker/latest/dg/sms-custom-templates-step3.html

context: object, required
    Lambda Context runtime methods and attributes

    Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

Returns
------
output: dict

    This output is an example JSON. We assume that your template have only one placeholder named "taskObject".
    If your template have more than one placeholder, make sure to add one more attribute under "taskInput"

    {
        "taskInput":{
            "taskObject":src_url_http
        },
        "humanAnnotationRequired":"true"
    }


    Note: Output of this lambda will be merged with the template, you specify in your labeling job.
    You can use preview button on SageMaker Ground Truth console to make sure merge is successful.

    Return doc: https://docs.aws.amazon.com/sagemaker/latest/dg/sms-custom-templates-step3.html
"""
import json
import re

def lambda_handler(event, context):
    # TODO implement
    source = event['dataObject']['source'] if "source" in event['dataObject'] else None
    source_ref = event['dataObject']['source-ref'] if "source-ref" in event['dataObject'] else None
    
    # if source_ref is not None:
    #     from urllib.request import urlopen
    #     try:
    #         source_ref = urlopen(source_ref).read().decode()
    #         source_ref = re.sub(r"\n", "<br>", source_ref)
    #     except Exception as e:
    #         source_ref = str(e)
    
    task_object = source if source is not None else source_ref
    
    return {
        "taskInput": {
            "utterance": task_object,
            "labels": str(["Response 1","Response 2","Response 3","Response 4"])
        }
    }
