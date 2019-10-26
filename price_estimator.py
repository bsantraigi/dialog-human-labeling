import os
import glob
# import nltk
import regex
import math

input_folder = "gcp-dataset"

files = glob.glob(f"{input_folder}/samples/*.txt")

total = 0.

for file in files:
    with open(file) as f:
        words = len(regex.split(r" +", f.read()))
        units = math.ceil(words/50)
        total += units

num_annotators = 3

print(f"Google Data Labelling Cost estimate: \nUSD {num_annotators*total*129/1000}")
        