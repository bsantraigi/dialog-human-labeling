import json
from os import system

pred_file = 'data/PACK_resgen_multiwoz/predictions.json'

tmp_refs = open('refs.txt', "w")
tmp_hyp = open('hyps.txt', "w")

with open(pred_file) as f:
    for line in f:
        line = line.strip()

        predictions = json.loads(line)

        for turn in predictions:
            T = predictions[turn]
            if 'resgen' not in T:
                continue
            gold = T['gold']
            resgen = T['resgen']

            tmp_refs.write(gold + '\n')
            tmp_hyp.write(resgen + '\n')

tmp_hyp.close()
tmp_refs.close()

import tf_bleu
import pickle

fp = 'd_vocab_lang.pickle'
# if os.path.isfile(fp):
lang = pickle.load(open(fp, 'rb'))

def T(s):
    return lang.decodeSentence(lang.encodeSentence(s))

refs = []
with open('refs.txt') as f:
    for line in f:
        line = line.strip()
        refs.append([T(line)])

hyps = []
with open('hyps.txt') as f:
    for line in f:
        line = line.strip()
        hyps.append(T(line))

print(tf_bleu.compute_bleu(refs, hyps))


# system('perl multi-bleu.perl refs.txt < hyps.txt')
