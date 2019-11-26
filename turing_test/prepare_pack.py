import regex
import json
import os

pack_name = "PACK_resgen_multiwoz"
pack_path = f"data/{pack_name}/"
bucket_path = "sagemaker-dialog-label-demo"

if not os.path.isdir(os.path.join(pack_path, 'files')):
    os.makedirs(os.path.join(pack_path, 'files'))

all_test_subjects = []

with open(os.path.join(pack_path, 'predictions.json')) as f:
    for i, x in enumerate(f):
        obj = json.loads(x)
        obj['id'] = f'D_{i}'
        all_test_subjects.append(obj)

"""
N = Number of lines in manifest.json = Number of HITs
Per line in manifest.json -- k annotation tasks
>> Total N*k annotations

# Number of annotation per HIT would be handled from AMT
"""
import random
N = 10 # Always assumes first N
per_person = 5
pages = N // per_person

with open(os.path.join(pack_path, 'manifest.json'), "w") as awsf:
    for x in range(0, N, per_person):
        y = x + per_person
        tests = all_test_subjects[x:y]
        awsf.write(json.dumps({
            'source-ids': ','.join(test['id'] for test in tests)
        }) + "\n")
