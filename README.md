## AWS Sagemaker Scripts for Human Evaluation of Dialog Response Generation Models
 
Used Lambda function templates from [Sagemaker Ground Truth Sample Scripts](https://github.com/aws-samples/aws-sagemaker-ground-truth-recipe)

### Supports Amazon Mechanical Turk (MTurk) / Private in-lab study backend
For private / in-lab annotation create a private workforce from AWS Sagemaker dashboard using email-ids or usernames. Then distribute the account details to your annotators along with the Labeling portal sign-in URL (or Amazon Cognito).


After the annotation is complete you will get a consolidated output file like the one shown below. 
```json5
[
  {
    "source-ref": "https://storage.googleapis.com/dialogue-resp-selection/gcp-dataset/samples/M2-60.txt",
    "dialog-labeling-demo10-private": {
      "annotationsFromAllWorkers": [
        {
          "workerId": "private.us-east-1.166160a28ba80787",
          "annotationData": {
            "content": "{\"response\":{\"label\":\"Response 2\"}}"
          }
        },
        {
          "workerId": "private.us-east-1.ef02e9a5ea346047",
          "annotationData": {
            "content": "{\"response\":{\"label\":\"Response 2\"}}"
          }
        }
      ]
    },
    "dialog-labeling-demo10-private-metadata": {
      "type": "groundtruth/custom",
      "job-name": "dialog-labeling-demo10-private",
      "human-annotated": "yes",
      "creation-date": "2019-10-27T10:35:45+0000"
    }
  },
  {
    "source-ref": "https://storage.googleapis.com/dialogue-resp-selection/gcp-dataset/samples/M2-83.txt",
    "dialog-labeling-demo10-private": {
      "annotationsFromAllWorkers": [
        {
          "workerId": "private.us-east-1.166160a28ba80787",
          "annotationData": {
            "content": "{\"response\":{\"label\":\"Response 1\"}}"
          }
        },
        {
          "workerId": "private.us-east-1.ef02e9a5ea346047",
          "annotationData": {
            "content": "{\"response\":{\"label\":\"Response 4\"}}"
          }
        }
      ]
    },
    "dialog-labeling-demo10-private-metadata": {
      "type": "groundtruth/custom",
      "job-name": "dialog-labeling-demo10-private",
      "human-annotated": "yes",
      "creation-date": "2019-10-27T10:35:45+0000"
    }
  }
]
```