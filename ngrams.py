#!/usr/bin/python
import time
import sys
import nltk, time, re
from nltk.corpus import wordnet as wn
from nltk.corpus import brown

N = 2

words = []
for word in brown.words():
    words.append(word.lower())

ngrams = nltk.ngrams(words,N)
FreqDist = nltk.FreqDist(ngrams)

# Constructing the reverse table. (fig 6.10 jurafsky martin)
REVERSE_TABLE = {}
for key in FreqDist:
    r_key = FreqDist[key]
    if REVERSE_TABLE.has_key(r_key):
        REVERSE_TABLE[r_key] += 1;
    else:
        REVERSE_TABLE[r_key] = 1;

# Calculating the value of N0.
VOCAB_SIZE = 49815              # computed specifically for the brown corpus.
N0  = VOCAB_SIZE*VOCAB_SIZE - len(FreqDist)
REVERSE_TABLE[0] = N0


# The following logic works only for the bigram case.
def correctPhrase(phrase, k):
    phrase = phrase.lower()
    pwords = phrase.split(' ')

    prob = 1.0
    for i in xrange(1, len(pwords)):
        c = FreqDist[ (pwords[i-1], pwords[i]) ]
        # Good turing adjusted count.
        if c == 0:
            c_star = float(REVERSE_TABLE[1]) / float(REVERSE_TABLE[0])
        elif c > k:
            c_star = c
        else:
            temp = float(k + 1) * float(REVERSE_TABLE[k+1]) / float(REVERSE_TABLE[1])
            c_star = (float(c+1) * float(REVERSE_TABLE[c+1]) / float(REVERSE_TABLE[c]) - float(c) * temp )/ (1 - temp)

        print i, c_star
        prob *= c_star

    return prob
