import nltk, scipy
from nltk.corpus import brown, stopwords
        
categories = brown.categories()
category_tagged_words = {}
for category in categories:
    category_tagged_words[category] = brown.tagged_words(categories=category, simplify_tags=True)

simplified_tags_category_words = {}
for category in categories:
    simplified_tags_category_words[category] = [word.lower() for (word, tag) in category_tagged_words[category] if
                                                tag == 'N' or tag == 'V' or tag == 'ADJ' or tag == 'ADV']

sentence = 'Medical tretment is very expnsive nowadays The por people cannot manage the huge costs Something needs to be done to make it afordable Government needs to stwp up and take chage'

sentence1 = 'The department is very proactive in setting up the syllabus The courses can be picked in any combination You can either credit or audit a particular subject But the consent of the teacher is required in either case'

word_to_categories_map = {}
word_to_stds_map = {}
sws = stopwords.words('english')
informative_words = []
for word in sentence.split(' '):
    if word not in sws:
        word_to_categories_map[word.lower()] = [(category, simplified_tags_category_words[category].count(word))
                                                for category in categories ]
        word_to_stds_map[word.lower()] = scipy.std([simplified_tags_category_words[category].count(word)
                                                    for category in categories])
        if (word_to_stds_map[word.lower()] >= 1.0):
            informative_words.append(word)

category_rank = {}
for category in categories:
    rank = 0
    for word in informative_words:
        for pair in word_to_categories_map[word]:
            if pair[0] == category:
                rank += pair[1]
                break
    category_rank[category] = rank
