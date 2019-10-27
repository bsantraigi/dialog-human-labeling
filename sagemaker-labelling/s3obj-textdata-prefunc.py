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
