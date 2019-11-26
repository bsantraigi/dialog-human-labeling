import json

def process_sample(sample):
    """
    root -> dict_keys(['name', 'annotations', 'text_payload'])
    root['text_payload'] -> dict_keys(['text_content'])

    each annotation entry ->
    'ANNOTATION_VALUE' {'text_classification_annotation': 
    {'annotation_spec': {'display_name': '3'}}}

    'ANNOTATION_METADATA' {'operator_metadata': 
    {'score': 1, 'total_votes': 3, 'label_votes': 3}}
    """
    payload = sample['text_payload']
    print(f"TEXT PAYLOAD: \n{payload['text_content']}")
    annotations_all = sample['annotations']
    for annot in annotations_all:
        print(f"ANNOTATIONS:\n")
        label = annot['annotation_value']['text_classification_annotation']['annotation_spec']['display_name']
        print(f"Label: Response {label}")

        score = annot['annotation_metadata']['operator_metadata']['score']
        votes = annot['annotation_metadata']['operator_metadata']['total_votes']
        print(f"Score: {score}")
        print(f"Votes: {votes}")


with open("annotated/gcp-dataset_annot-dialog-labeling-demo-1.json") as f:
    for i, line in enumerate(f):
        print(f"\n============== DIALOGUE {i} ===============\n")
        sample = json.loads(line.strip())
        process_sample(sample)