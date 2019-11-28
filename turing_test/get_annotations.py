import boto3
import regex

# bucket_path = "s3://sagemaker-dialog-label-demo/PACK_resgen_multiwoz/template1/resgen-public1/annotations/consolidated-annotation/consolidation-request/iteration-1/2019-11-27_00:42:47.json"
bucket = "sagemaker-dialog-label-demo"
folder = "PACK_resgen_multiwoz/template1/resgen-public1/annotations/consolidated-annotation/consolidation-request/iteration-1/"
bucket_path = f"s3://{bucket}/{folder}"

# Get file list
s3 = boto3.resource('s3')
my_bucket = s3.Bucket(bucket)
for my_bucket_object in my_bucket.objects.filter(Prefix=folder):
    print(my_bucket_object.key)
    fname = regex.search(r"[^\/]+.json", my_bucket_object.key)
    fname = fname.group(0)
    fname = fname.replace(':', '_')
    # Download files with filename fix
    s3.meta.client.download_file(bucket, my_bucket_object.key, f"annotation_download/{fname}")