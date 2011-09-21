# Implements linear interpolation of various ngrams
import nltk
from nltk.corpus import brown

sents = brown.sents()
len_training = 60 * len(sents) / 100
training_sents = sents[:len_training]
held_out_sents = sents[len_training:]

extended_sents = []
for sentence in training_sents:
    lst = ['<s>', '<s>']
    lst.extend(sentence)
    extended_sents.append(lst)

trigrams = []
for sent in extended_sents:
    trigrams.extend(nltk.trigrams(sent))
trigramDist = nltk.FreqDist(trigrams)

bigrams = []
for sent in extended_sents:
    bigrams.extend(nltk.bigrams(sent[1:]))
bigramDist = nltk.FreqDist(bigrams)

unigrams = []
for sent in extended_sents:
    unigrams.extend(sent[2:])
unigramDist = nltk.FreqDist(unigrams)

test_sentence = "Keep your friends close, and your enemies closer."

# trigram = pair of three items (the, of, in)
def prob_tigram (trigram):
    return float(trigramDist[trigram]) / float(len(trigrams))

# bigram = pair of two items
def prob_bigram (bigram):
    return float(bigramDist[bigram]) / float(len(bigrams))

# unigram = single word
def prob_unigram (unigram):
    return float(unigramDist[unigram]) / float(len(unigrams))

def estimate_parameters ():
    
    
