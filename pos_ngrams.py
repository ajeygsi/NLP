# Part of Speech N-gram model
# For a sentence S = W1 W2 W3 ... Wn,
#    Prob (S) = Sum_T (prod_i P(Wi | Ti) prod_i P(Ti | T_(i-2) T_(i-1)))

import nltk
from nltk.corpus import brown # brown corpus used as training data

# A list of (word, tag)
tagged_words = brown.tagged_words(simplify_tags=True)

# A list of (tag, word)
tags_words = [(tag, word.lower()) for (word, tag) in tagged_words]

# condFreqDist[tag][word] = count(word | tag)
condFreqDist = nltk.ConditionalFreqDist(tags_words)


### trigram pos model

# A list of tagged sentences, each sentence is a list of (word, tag)
tagged_sents = brown.tagged_sents(simplify_tags=True)

# A list of tagged sentences, each sentence is a list of tag
tags_sents = []
for sentence in tagged_sents:
    lst = ['<s>', '<s'>]
    lst.extend([tag for (word, tag) in sentence])
    tags_sents.append(lst)

# A list of all trigrams in training data
trigrams = []
for sent in tags_sents:
    trigrams.extend(nltk.trigrams(sent))

trigramDist = nltk.FreqDist(trigrams)

# A list of all bigrams in training data
bigrams = []
for sent in tags_sents:
    bigrams.extend(nltk.bigrams(sent))

bigramDist = nltk.FreqDist(bigrams)

test_sentence = 'This is now the dominant sense in ordinary use'

