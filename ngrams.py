# Phrase level spell checker

#!/usr/bin/python
import time
import sys
import nltk, time, re
from nltk.corpus import brown

sents1 = brown.sents()
sents = []
for sent in sents1:
    sents.append([word.lower() for word in sent])

bigrams = []
for sent in sents:
    bigrams.extend(nltk.bigrams(sent))
bigramDist = nltk.FreqDist(bigrams)

# Constructing the reverse table. (fig 6.10 jurafsky martin)
REVERSE_TABLE = {}
for key in bigramDist:
    r_key = bigramDist[key]
    if REVERSE_TABLE.has_key(r_key):
        REVERSE_TABLE[r_key] += 1;
    else:
        REVERSE_TABLE[r_key] = 1;

# Calculating the value of N0.
VOCAB_SIZE = 49815              # computed specifically for the brown corpus
N0  = VOCAB_SIZE*VOCAB_SIZE - len(bigramDist)
REVERSE_TABLE[0] = N0


# The following logic works only for the bigram case.
# phrase is a list of words, does not include '.' if it is a sentence
# phrase = ['the', 'power', 'is', 'good']
# k = 100
# is_sentence = false whenever called for TestCase2, true for others
def getProbabilityOfPhrase(phrase, k, is_sentence):
    if is_sentence:
        phrase.append('.')
    prob = 1.0
    for i in xrange(1, len(phrase)):
        c = bigramDist[ (phrase[i-1], phrase[i]) ]
        # Good turing adjusted count.
        if c == 0:
            c_star = float(REVERSE_TABLE[1]) / float(REVERSE_TABLE[0])
        elif c > k:
            c_star = c
        else:
            temp = float(k + 1) * float(REVERSE_TABLE[k+1]) / float(REVERSE_TABLE[1])
            c_star = (float(c+1) * float(REVERSE_TABLE[c+1]) / float(REVERSE_TABLE[c]) - float(c) * temp )/ (1 - temp)

 #       print i, c_star
        prob *= c_star

    return prob
