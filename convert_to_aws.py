import regex
import json

gcp_catalog_file = "gcp-dataset/catalog.csv"
bucket_path = "sagemaker-dialog-label-demo"
with open(gcp_catalog_file) as f, open("gcp-dataset/aws_manifest.json", "w") as awsf:
    import random
    
    # for x in f:
    #     if random.random() > 0.8:
    #         m = regex.match(r"gs:\/\/.+?\/.+?\/(.+)", x)
    #         s3_name = {"source-ref": f"s3://{bucket_path}/{m.group(1)}"}
    #         # s3://dialog-labeling-demo1/samples/M1-1.txt
    #         awsf.write(json.dumps(s3_name) + "\n")

    for x in f:
        if random.random() > 0.8:
            m = regex.match(r"gs:\/\/.+?\/.+?\/(.+)", x)
            s3_name = {"source-ref": f"https://storage.googleapis.com/dialogue-resp-selection/gcp-dataset/{m.group(1)}"}
            # https://storage.googleapis.com/dialogue-resp-selection/gcp-dataset/samples/M1-1.txt
            awsf.write(json.dumps(s3_name) + "\n")