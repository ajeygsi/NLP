import nltk
from nltk.corpus import brown

def uniqfy (list):
    """ remove duplicates from given list """
    checked = []
    for elt in list:
        if elt not in checked:
            checked.append(elt)
    return checked

tags_words = brown.tagged_words(simplify_tags=True)
tags = [tag for (word, tag) in tags_words]
uniq_tags = uniqfy(tags)


