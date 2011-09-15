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
sentence = "recent primary election produced no evidence that"
t_words = sentence.lower().split(' ')
sentence_length = len(t_words)

BIGRAM_TABLE = {}               
for i in xrange(0,sentence_length):
    BIGRAM_TABLE[t_words[i]] = {}
    


for i in xrange(0,sentence_length):
    for j in xrange(0,sentence_length):

        c = FreqDist[ (t_words[i],t_words[j]) ]

        # Good turing adjusted count.
        c_star = float(c+1) * float(REVERSE_TABLE[c+1]) / float(REVERSE_TABLE[c])
        BIGRAM_TABLE[t_words[i]][t_words[j]] = c_star


    

            

