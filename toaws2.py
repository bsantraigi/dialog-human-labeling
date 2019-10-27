import regex
import json
import glob


gcp_folder = "gcp-dataset/samples"
samples = glob.glob(f"{gcp_folder}/*.txt")

bucket_path = "dialog-labeling-demo1"
with open("gcp-dataset/aws_manifest.json", "w") as awsf:
    import random
    
    for x in samples:
        if random.random() > 0.8:
            s = regex.sub("\n", r"</br>", open(x).read())
            s3_name = {"source": f'{s}'}
            # s3://dialog-labeling-demo1/samples/M1-1.txt
            awsf.write(json.dumps(s3_name) + "\n")