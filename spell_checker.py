#!/usr/bin/python
import time
import sys
import nltk, time
from nltk.corpus import wordnet as wn
from nltk.corpus import brown

DICTIONARY = "/usr/share/dict/words";
#TARGET = sys.argv[1]
MAX_COST = 2

# Keep some interesting statistics
NodeCount = 0
#WordCount = 0

def train (words):
    fDist = nltk.FreqDist([w.lower() for w in words])
    return fDist


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
    for letter in trie.children:
        searchRecursive( trie.children[letter], 1, letter, '', word, currentRow, 
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

        insertCost = currentRow[column - 1] + 1
        deleteCost = previousRow[column] + 1

        if word[column - 1] != letter:
            replaceCost = previousRow[ column - 1 ] + 0.5
        else:                
            replaceCost = previousRow[ column - 1 ]

        # TODO: Is the line below needed ?
        transposeCost = min( insertCost, deleteCost, replaceCost)
        if (column > 1 and lenCurrent > 1 and word[column - 1] == prevLetter and word[column - 2] == letter):
            transposeCost = secondPreviousRow[ column - 2 ] + 0.5

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

trie = TrieNode()
WordCount = 0
# read dictionary file into a trie
for word in open(DICTIONARY, "rt").read().split():
    WordCount += 1
    trie.insert( word.lower() )
    
print "Read %d words into %d nodes" % (WordCount, NodeCount)

def correct (word1):
    word1 = word1.lower()
    threshold = 50
    training_set = brown.words()
    fDist = train(training_set)
    for word in training_set:
        if (fDist[word] > threshold):
            fDist[word] = threshold

    print max(fDist)

    start = time.time()
    results = search( word1, MAX_COST )
    #    wtd_candidates = [(word, fDist[word]/count) for (word, count) in results if count != 0]
    suggestions = sorted(results, key=lambda candidate: candidate[1])

    end = time.time()
        
    print "Search took %g s" % (end - start)
    return suggestions
