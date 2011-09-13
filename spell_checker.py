#!/usr/bin/python
import time
import sys
import nltk, time, re
from nltk.corpus import wordnet as wn
from nltk.corpus import brown

DICTIONARY = "/usr/share/dict/words";
#TARGET = sys.argv[1]
MAX_COST = 2

# Keep some interesting statistics
NodeCount = 0
#WordCount = 0

# The soundex lookup table.
SOUNDEX_TABLE = {'a':-1, 'e':-1, 'h':-1, 'i':-1, 'o':-1, 'u':-1, 'w':-1, 'y':-1,
                'b':1, 'f':1, 'v':1, 'p':1,
                'c':2, 'g':2, 'j':2, 'k':2, 'q':2, 's':2, 'x':2, 'z':2,
                'd':3, 't':3,
                'l':4,
                'm':5, 'n':5,
                'r':6 }

# returns simillar sounding charaters to the 'letter'
def getSimillarSoundCharaters (letter):
    result = []
    for key in SOUNDEX_TABLE.keys():
        if SOUNDEX_TABLE[key] == SOUNDEX_TABLE[letter]:
            result.append(key)
    return result

# The Trie data structure keeps a set of words, organized with one node for
# each letter. Each node has a branch for each letter that may follow it in the
# set of words.
class TrieNode:
    def __init__(self):
        self.word = None
        self.children = {}

        global NodeCount
        NodeCount += 1

    def insert( self, word ):
        node = self
        for letter in word:
            if letter not in node.children: 
                node.children[letter] = TrieNode()

            node = node.children[letter]

        node.word = word

# Reads a matrix from the given file, and returns a normalized matrix (0-1)
def getMatrix (file):
    mat = []
    f = open(file)
    for line in f:
        mat.append([int(num) for num in line.split()])

    maximum = 0
    for row in mat:
        if max(row) > maximum:
            maximum = max(row)

    matrix = [[1 - float(entry)/maximum for entry in row] for row in mat]
    return matrix

# Global execution, one time executed
trie = TrieNode()
WordCount = 0
# read dictionary file into a trie
words = open(DICTIONARY, "rt").read().split()
for word in words[:-15]:
    WordCount += 1
    trie.insert( re.sub(r'\W+', '', word.lower()) )    
print "Read %d words into %d nodes" % (WordCount, NodeCount)
deleteConfusionMat = getMatrix('delete.txt')
insertConfusionMat = getMatrix('insert.txt')
substituteConfusionMat = getMatrix('substitute.txt')
transposeConfusionMat = getMatrix('transpose.txt')

# Computes frequency distribution of each word in given training set
def train (words):
    fDist = nltk.FreqDist([w.lower() for w in words])
    return fDist


# Returns the soundex code for a given word.
def getSoundexCode(word):
    code = word[0]

    for i in xrange(1, len(word) ):
        if (SOUNDEX_TABLE[word[i]] != -1):
            if ((str(SOUNDEX_TABLE[word[i]]) != code[-1] )):
                code += str(SOUNDEX_TABLE[word[i]])
                
                if( len(code) >= 4):
                    return code

    return code

# Returns a integer mapping to the letter, 'a' -> 0, 'b' -> 1, so on, ' ' -> 26
def getCode (letter):
    alphabets = 'abcdefghijklmnopqrstuvwxyz'
    code = alphabets.find(letter)
    if code >= 0:
        return code
    else:
        return 26


# The search function returns a list of all words that are less than the given
# maximum distance from the target word
def search( word, maxCost ):

    # previous row
    previousRow = []
    for i in range( len(word) + 1):
        previousRow.append(0)

    # build first row
    currentRow = range( len(word) + 1 )

    results = []

    # recursively search each branch of the trie
    #for letter in trie.children:
    for letter in getSimillarSoundCharaters(word[0]):
        searchRecursive( trie.children[letter], 1, letter, ' ', word, currentRow, 
            previousRow, results, maxCost )

    return results

# This recursive helper is used by the search function above. It assumes that
# the previousRow has been filled in already.
def searchRecursive( node, lenCurrent, letter, prevLetter, word, previousRow, secondPreviousRow, results, maxCost ):

    columns = len( word ) + 1
    currentRow = [ previousRow[0] + 1 ]

    # Build one row for the letter, with a column for each letter in the target
    # word, plus one for the empty string at column 0
    for column in xrange( 1, columns ):

        if column > 1:
            insertCost = currentRow[column - 1] + insertConfusionMat[getCode(word[column-2])][getCode(word[column-1])]
        else:
            insertCost = currentRow[column - 1] + insertConfusionMat[getCode(' ')][getCode(word[column-1])]
        
        deleteCost = previousRow[column] + deleteConfusionMat[getCode(word[column-1])][getCode(letter)]

        if word[column - 1] != letter:
            substitutionCost = substituteConfusionMat[getCode(word[column-1])][getCode(letter)]
            # If simillar sounding alphabet is substituted, weight it lesser.
            if SOUNDEX_TABLE[word[column - 1]] == SOUNDEX_TABLE[letter]:
                substitutionCost /= 2.0
            replaceCost = previousRow[ column - 1 ] + substitutionCost
        else:                
            replaceCost = previousRow[ column - 1 ]

        transposeCost = min( insertCost, deleteCost, replaceCost)
        if (column > 1 and lenCurrent > 1 and word[column - 1] == prevLetter and word[column - 2] == letter):
            transposeCost = secondPreviousRow[ column - 2 ] + transposeConfusionMat[getCode(prevLetter)][getCode(letter)]/2

        currentRow.append( min( insertCost, deleteCost, replaceCost, transposeCost ) )

    # if the last entry in the row indicates the optimal cost is less than the
    # maximum cost, and there is a word in this trie node, then add it.
    if currentRow[-1] <= maxCost and node.word != None:
        results.append( (node.word, currentRow[-1] ) )

    # if any entries in the row are less than the maximum cost, then 
    # recursively search each branch of the trie
    if min( currentRow ) <= maxCost:
        for letter1 in node.children:
            searchRecursive( node.children[letter1], lenCurrent + 1, letter1, letter, word, currentRow, 
                previousRow, results, maxCost )


# Returns the max distance for a given length.
def getMaxCost(word_length):
    if( word_length <= 4):
        return 1
    elif( word_length <= 8):
        return 2
    else:
        return 3

def correct (word1):
    word1 = word1.lower()
    soundexCode = getSoundexCode(word1)
#    threshold = 50
#    training_set = brown.words()
#    fDist = train(training_set)
#    for word in training_set:
#        if (fDist[word] > threshold):
#            fDist[word] = threshold

#    print max(fDist)

    start = time.time()
    results = search( word1, getMaxCost(len(word1)) )
#    wtd_candidates = [(word, fDist[word]/count) for (word, count) in results if count != 0]
    i = 1
    while len(results) < 5:
        results = search( word1, getMaxCost(len(word1)) + i)
        i = i + 1
    suggestions = sorted(results, key=lambda candidate: candidate[1])
    end = time.time()
    
    return (suggestions, end - start)
