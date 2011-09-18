0. Edit distance based on length of the target word.
1. Implement SOUNDEX (Naive)
*2. Estimate P(t|c) using an errorneous data of correct and incorrect spellings.
	Rank edit distance suggestions based on these probabilities

To merge Soundex and edit distance suggestions:
 Rank each edit distance suggestion, which is there in soundex suggestion in
 increasing order of rank of edit distance suggestion before any other suggestion.

 Rank remaining suggestions in the same order.

Soundex Algorithm link:
http://www.sound-ex.com/soundex_method.htm

Github reference link:
http://gitref.org/


For each word, assign categories in which it is present
Now for each suggestion, match category with the categories of context words.
