from collections import defaultdict, Counter
import regex as re
import html
import unicodedata
# import numpy as np

class Lang:
    def __init__(self, name, _min_w_count=2):
        self.name = name
        self.word2index = {}
        self.word2count = {}
        self.index2word = {}
        self.VOCAB_SIZE = 0
        
        # Special tokens
        self.PAD = '<pad>'
        self.SOS = '<s>'
        self.EOS = '</s>'
        self.UNK = '<unk>'
        
        self.iPAD = 0
        self.iSOS = 1
        self.iEOS = 2
        self.iUNK = 3
        
        self.min_count = _min_w_count

        self.idf = defaultdict(lambda: 0)
        self.idf[self.PAD] = 0
        self.idf[self.SOS] = 0
        self.idf[self.EOS] = 0
        self.idf[self.UNK] = 0

        self.pos_weights = None
    
    def eos_id(self):
        return self.iEOS
    
    def bos_id(self):
        return self.iSOS
    
    def normalizeSentence(self, s, escape_html=True):
        """Normalizes a space delimited sentence 'line'
        
        Arguments:
        s -- string representing a sentence
        
        Returns:
        w_arr -- array containing the normalized words of the normalized sentence
        """
        
        # Turn a Unicode string to plain ASCII, thanks to
        # http://stackoverflow.com/a/518232/2809427
        def unicodeToAscii(s):
            return ''.join(
                c for c in unicodedata.normalize('NFD', s)
                if unicodedata.category(c) != 'Mn'
            )
        
        # Escape HTML
        if escape_html:
            s = html.unescape(s)
        #line = '<s> ' + line.strip() + ' </s>'
        
        #allowed_punct = ".!?,-"
        #s = unicodeToAscii(s.lower().strip())
        #s = re.sub(r"([%s])" % allowed_punct, r" \1 ", s)
        #s = re.sub(r"[^a-zA-Z0-9%s]+" % allowed_punct, r" ", s)
        
        """
        Alternative
        To keep hyphens without spaces intact
        """
        allowed_punct = ".!?,"
        s = unicodeToAscii(s.lower().strip())
        s = re.sub(r"([%s])" % allowed_punct, r" \1 ", s)
        
        allowed_punct = ".!?,-"
        s = re.sub(r"[^a-zA-Z0-9%s]+" % allowed_punct, r" ", s)
    
        s = s.strip()
        
        # Tokenize + Strip + Split
        tokenized_l = re.split('[ ]+', s)
        
        return tokenized_l
    def encodeSentence(self, l):
        l = self.normalizeSentence(l)
        el = []
        for w in l:
            if w in self.word2index:
                el.append(self.word2index[w])
            else:
                el.append(self.iUNK)
        return el
    
    def EncodeAsIds(self, l):
        return self.encodeSentence(l)
    
    def sample_encode_as_ids(self, l, *args): 
        return self.encodeSentence(l)
    
    def decodeSentence(self, el):
        dl = []
        for i in el:
            if i == self.iEOS:
                break
            dl.append(self.index2word[i])
        return dl
        #return [self.index2word[i] for i in el if i != self.iEOS]
    
    def DecodeIds(self, el):
        return ' '.join(self.decodeSentence(el))
    
    def limitVocab(self, max_size):
        """
        Decreases the vocab size by keeping top-k entries of the vocab based on word2count
        """
        if self.VOCAB_SIZE <= max_size:
            print(f'Current vocab size is {self.VOCAB_SIZE}, no need to decrease size')
            return
#         self.word2index = {}
#         # self.word2count = {}
#         self.index2word = {}
        self.VOCAB_SIZE = max_size
        
#         self.SOS = '<s>'
#         self.EOS = '</s>'
#         self.UNK = '<unk>'
#         self.iSOS = 0
#         self.iEOS = 1
#         self.iUNK = 2
        
        c = Counter(self.word2count)
        m = c.most_common(1)[0][1]
        c[self.PAD] = m + 4
        c[self.SOS] = m + 3
        c[self.EOS] = m + 2
        c[self.UNK] = m + 1
        
        list_of_wc = c.most_common(max_size)
        self.index2word = {i:w for i, (w, _) in enumerate(list_of_wc)}
        self.word2index = {w:i for i, (w, _) in enumerate(list_of_wc)}
        
    def buildLang(self, corpus_gen, sentenceFilterFunct=lambda x: x):
        """Creates a language from corpus txt
        
        Keyword Args:
        corpus_file -- input file. contains text data from which the vocab is to be built
        
        """
        
        def auto_id():
            """Generator function for auto-increment id(0)"""
            i = 0
            while(True):
                yield i
                i += 1
        
        ID_gen1 = auto_id()
        word2i = defaultdict(lambda: next(ID_gen1))
        wordCount = defaultdict(int)
        i2word = {}
        
        i2word[word2i[self.PAD]] = self.PAD # 0: PAD
        i2word[word2i[self.SOS]] = self.SOS # 1: SOS
        i2word[word2i[self.EOS]] = self.EOS # 2: EOS
        i2word[word2i[self.UNK]] = self.UNK # 3: UNK
        
        re_space = re.compile('[ ]+')

        #with open(corpus_gen) as fr:
        # with open(data_path + 'train.en') as fr, open(data_path+'normalized.train.en', 'w') as fw:
        fr = corpus_gen
        N = 0
        for i, line in enumerate(fr):
            N+=1
            # Build word2i and i2word
            tokens = self.normalizeSentence(line)
            token_set = set(tokens)
            for t in token_set:
                self.idf[t] += 1
            for t in sentenceFilterFunct(tokens):
                wordCount[t] += 1
                if wordCount[t] >= self.min_count:
                    i2word[word2i[t]] = t

        self.idf = dict(self.idf)
        for k, v in self.idf.items():
            if v > 0:
                self.idf[k] = N / v
            else:
                self.idf[k] = 1. # tokens like PAD, UNK etc. are treated as stop words


        self.word2index = dict(word2i)
        self.index2word = i2word
        self.word2count = dict(wordCount)
        self.VOCAB_SIZE = len(self.word2index)
        print("Vocabulary created...")
        print(f"Vocab Size: {self.VOCAB_SIZE}")
        print(f"Number of lines in corpus: {i}")

    def calc_pos_weights(self):
        self.pos_weights = np.zeros((self.VOCAB_SIZE,), dtype=np.float32)
        for i, w in self.index2word.items():
            self.pos_weights[i] = self.idf[w]

# class Metric:
#     def __init__(self):
#         self.i = 0
#         self.size = 0
#         self._L = 100
#         self.val = [0 for _ in range(self._L)]
#
#     def insert(self, v):
#         self.val[self.i] = v
#         self.i = (self.i + 1) % self._L
#         self.size = min(self._L, self.size + 1)
#
#     def __str__(self):
#         return f"{np.mean(self.val[:self.size]):0.3}"
#
#     def __repr__(self):
#         return self.__str__()

class Metric:
    def __init__(self):
        self.avg = None
        self._p = 0.2

    def insert(self, v):
        self.avg = ((1-self._p)*self.avg + self._p*v) if self.avg is not None else float(v)

    def __str__(self):
        return f"{self.avg:0.3}"

    def __repr__(self):
        return self.__str__()


# import random
# import matplotlib.pyplot as plt
# a = Metric()
#
# x = []
# y = []
# for i in range(300):
#     u = random.random()*0.1 + np.exp(-np.sqrt(i/10))
#     a.insert(u)
# #     print(i, a)
#     x.append(u)
#     y.append(a.avg)
# plt.plot(x)
# plt.plot(y)
#
# plt.legend(["true", "avg"])