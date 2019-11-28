# Process the annotations > save them
import glob
import json
from collections import defaultdict, Counter

annotations = defaultdict(list)
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

            for key in worker_annot['annotations']:
                ann = worker_annot['annotations'][key]
                gt = worker_annot['ground_truths'][key]
                annotations[key].append((gt, ann))

annotations = dict(annotations)

c = Counter()
for key in annotations:
    for instance in annotations[key]:
        c[instance] += 1
# print(annotations)
print(c)
H_H = c[('human', 'human')]
H_AI = c[('human', 'ai')]
AI_H = c[('ai', 'human')]
AI_AI = c[('ai', 'ai')]

print(f"Baseline Ratio:", H_H/(H_H + H_AI))
print(f"RESGEN Ratio:", AI_H/(AI_AI + AI_H))