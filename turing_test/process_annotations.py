# Process the annotations > save them
import glob
import json
from collections import defaultdict, Counter

annotations = defaultdict(list)
annotations_by_id = {}
for afile in glob.glob('annotation_download/multiwoz_turing/*.json'):
    # print(afile)
    json_arr = json.loads(open(afile).read())
    for obj in json_arr:
        # print(obj)
        real_annots = obj['annotations']
        for real_annot in real_annots:
            worker_annot = json.loads(real_annot['annotationData']['content'])
            for key, val in worker_annot.items():
                worker_annot[key] = json.loads(val)

            worker_id = real_annot['workerId']
            annotations_by_id[worker_id] = []
            for key in worker_annot['annotations']:
                ann = worker_annot['annotations'][key]
                gt = worker_annot['ground_truths'][key]
                annotations[key].append((gt, ann))
                annotations_by_id[worker_id].append((gt, ann))

annotations = dict(annotations)

c = Counter()
for key in annotations:
    for instance in annotations[key]:
        c[instance] += 1
# print(annotations)
print(c)
def average_compare(c):
    H_H = c[('human', 'human')]
    H_AI = c[('human', 'ai')]
    AI_H = c[('ai', 'human')]
    AI_AI = c[('ai', 'ai')]

    print(f"Baseline Ratio:", H_H/(H_H + H_AI))
    print(f"RESGEN Ratio:", AI_H/(AI_AI + AI_H))

average_compare(c)

"""BAD ANNOTATIONS
1. Any annotation with all 'human' or 'ai' as annotation!
2. 
"""
def personal_compare(c):
    H_H = c[('human', 'human')]
    H_AI = c[('human', 'ai')]
    AI_H = c[('ai', 'human')]
    AI_AI = c[('ai', 'ai')]

    if (AI_AI == 0 and H_AI == 0) or (AI_H == 0 and H_H==0):
        return 0

    return AI_H - H_AI

for worker_id in annotations_by_id:
    annots = annotations_by_id[worker_id]
    c = Counter(annots)
    print(worker_id)
    print(c)
    print(personal_compare(c))