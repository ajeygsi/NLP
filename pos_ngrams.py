# Part of Speech N-gram model
# For a sentence S = W1 W2 W3 ... Wn,
#    Prob (S) = Sum_T (prod_i P(Wi | Ti) prod_i P(Ti | T_(i-2) T_(i-1)))

import nltk, os, re
from nltk.corpus import brown # brown corpus used as training data
import utilities
import ngrams

NUM_OF_BROWN_TAGS = 26
VOCAB = 49815

# Ruby tags to Brown corpus tags mapping
ruby_to_brown_tags = {
    'cc': ['CNJ'],
    'in': ['CNJ'],
    'cd': ['NUM'],
    'det': ['DET'],
    'pdt': ['DET'],
    'ex': ['EX'],
    'fw': ['FW'],
    'jj': ['ADJ'],
    'jjr': ['ADJ'],
    'jjs': ['ADJ'],

    'md': ['MOD'],
    'nn': ['N', 'NP'],
    'nnp': ['N', 'NP'],
    'nnps': ['N', 'NP'],
    'nns': ['N', 'NP'],

    'prp': ['PRO'],
    'prps': ['PRO'],
    'rb': ['DET', 'ADV', 'ADJ'],
    'rbr': ['DET', 'ADV', 'ADJ'],
    'rbs': ['DET', 'ADV', 'ADJ'],
    'rp': ['DET', 'ADV', 'ADJ'],

    'to': ['TO'],
    'uh': ['ADJ'],
    'vb': ['V'],
    'vbp': ['V'],
    'vbd': ['VD'],
    'vbg': ['VG'],
    'vbn': ['VBN'],
    'vbz': ['VBZ'],
    'wdt': ['WH'],
    'wp': ['WH'],
    'wps': ['WH'],
    'wrb': ['WH'],
    'pp': ['.'],
    'ppc': [','],
    'ppl': ['``'],
    'ppr': ["'", "''"],
    'pps': [':'],
    'lrb': ['('],
    'rrb': [')'],
}


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
    lst = ['<s>', '<s>']
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

# Returns the probability of this sentence
# For error correction, many sentences will be generated
# in suggestion for given misspelled sentence.
# The one with the highest probability will be the best suggestion

# sentence is a list of words, final '.' is not there
def getProbabilityOfSentence (sentence):
    test_sentence = " ".join(sentence)
    test_sentence += "."
    ruby_call_query = 'ruby pos_tagger.rb "' + test_sentence + '" outfile.txt'
    os.system(ruby_call_query)
    
    tagged_test_sent = open('outfile.txt').read()
    test_words = []
    test_tags = []
    for tagged_word in tagged_test_sent.split(' '):
        srch = re.search('<.*>(.*)</(.*)>', tagged_word)
        test_words.append(srch.group(1).lower())
        test_tags.append(srch.group(2).lower())

    # generate all possible tag sequences
#     tag_sequences = []
#     for each in ruby_to_brown_tags[test_tags[0]]:
#         tag_sequences.append([each])

#     for tag in test_tags[1:]:
#         lst_corresponding_brown_tags = ruby_to_brown_tags[tag]
#         if (len(lst_corresponding_brown_tags) == 1):
#             for seq in tag_sequences:
#                 seq.append(lst_corresponding_brown_tags[0])
#         else:
#             new_sequences = []
#             for seq in tag_sequences:
#                 for suggested_tag in lst_corresponding_brown_tags:
#                     new_list = list(seq)
#                     new_list.append(suggested_tag)
#                     new_sequences.append(new_list)
            
#             tag_sequences = list(new_sequences)
    brown_tags = []
    for each in test_tags:
        brown_tags.append(ruby_to_brown_tags[each])

    tag_sequences = utilities.unpackAList(brown_tags)

    # rank each generated tag sequence with trigram pos model
    tag_seq_rank = []
    for tag_seq in tag_sequences:
        prob_sent_tag = 1.0
        for i in xrange(0, len(tag_seq)):
            prob_sent_tag *= float(condFreqDist[tag_seq[i]][test_words[i]] + 1) / float(len(condFreqDist[tag_seq[i]]) + VOCAB)    
            
        trigram_tag_seq = ['<s>', '<s>']
        trigram_tag_seq.extend(tag_seq)
        trigrams = nltk.trigrams(trigram_tag_seq)
        prob_trigram = 1.0
        for each in trigrams:
            prob_trigram *= float(trigramDist[each] + 1) / float(bigramDist[each[:-1]] + NUM_OF_BROWN_TAGS)
            
        tag_seq_rank.append(prob_sent_tag * prob_trigram)
    
    return sum(tag_seq_rank)


# lst_sentences = [['the'], ['power', 'pour', 'powers'], ['is'], ['goad']],
# only one is multilist
# returns = ['power', 'powers', 'pour'] -- ranked suggestions
def correctSentences (lst_sentences):
    for i in xrange(0, len(lst_sentences)):
        if (len(lst_sentences[i]) > 1):
            break

    list_prefix_words = lst_sentences[:i]
    list_suffix_words = lst_sentences[i+1:]
    suggestions = lst_sentences[i]

    suggestion_to_sentence = {}
    suggestion_pos = {}
    for each_suggestion in suggestions:
        sentence = []
        sentence = [word for [word] in list_prefix_words]
        sentence.append(each_suggestion)
        sentence.extend([word for [word] in list_suffix_words])
        suggestion_to_sentence[each_suggestion] = sentence
        
        test_sentence = " ".join(sentence)
        test_sentence += "."
        ruby_call_query = 'ruby pos_tagger.rb "' + test_sentence + '" outfile.txt'
        os.system(ruby_call_query)
        
        tagged_test_sent = open('outfile.txt').read()
        test_words = []
        test_tags = []
        for tagged_word in tagged_test_sent.split(' '):
            srch = re.search('<.*>(.*)</(.*)>', tagged_word)
            test_words.append(srch.group(1).lower())
            test_tags.append(srch.group(2).lower())

        found = False
        for ruby_pos in suggestion_pos:
            if ruby_to_brown_tags[ruby_pos] == ruby_to_brown_tags[test_tags[i]]:
                suggestion_pos[ruby_pos].append(each_suggestion)
                found = True
                break
                
        if (found == False):
            suggestion_pos[test_tags[i]] = [each_suggestion]


#    print suggestion_to_sentence
#    print suggestion_pos

    pos_probability = []
    for each_pos in suggestion_pos:
        sentence = []
        sentence = [word for [word] in list_prefix_words]
        sentence.append(suggestion_pos[each_pos][0])
        sentence.extend([word for [word] in list_suffix_words])
        pos_probability.append((each_pos, getProbabilityOfSentence(sentence)))

#    print pos_probability

    sorted_pos_probability = sorted(pos_probability, key=lambda candidate: -candidate[1])
#    print sorted_pos_probability

    ranked_suggestions = []
    for pair in sorted_pos_probability:
        if len(suggestion_pos[pair[0]]) == 1:
            ranked_suggestions.append(suggestion_pos[pair[0]][0])
        else:
            posssible_suggestions = suggestion_pos[pair[0]]
            posssible_suggestions_prob = []
            for each_suggestion in posssible_suggestions:
                sentence = []
                sentence = [word for [word] in list_prefix_words]
                sentence.append(each_suggestion)
                sentence.extend([word for [word] in list_suffix_words])
                posssible_suggestions_prob.append((each_suggestion, ngrams.getProbabilityOfPhrase(sentence, 100, True)))

            sorted_possible_suggestions_prob = sorted(posssible_suggestions_prob, key=lambda candidate: -candidate[1])
            for each in sorted_possible_suggestions_prob:
                ranked_suggestions.append(each[0])
                
#            print sorted_possible_suggestions_prob

    return ranked_suggestions
