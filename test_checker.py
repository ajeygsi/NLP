import spell_checker            # Assuming it is in the same directory.
from xml.etree import ElementTree as ET
import re
import utilities
import pos_ngrams
import ngrams


MAX_UNIGRAM_SUGGESTIONS = 6
MAX_SUGGESTIONS = 5

regex_punct = re.compile('[,|:|\'|\"|.|?|!]')
def isPunctuation(str):
    if(( len(str) == 1) and (regex_punct.match(str))):
        return True
    return False

def getSecond(tuple):
    return tuple[1]

# function to read the input file which is in xml format
# and write the output to the output file.
def test(input_file_name,output_file_name):
    file = open(input_file_name)
    data = file.read()
    element = ET.XML(data)

    outfile = open(output_file_name,"w")
    
    # regex for single word.
    regex_single = re.compile('\w+')

    # regex for phrase.
    regex_phrase = re.compile('\w+|[,|:|(|)|\'|\"]')
    
    # creating the regex obj.
    regex = re.compile('\w+|[.|,|:|(|)|\'|\"]')


    
    for subelement in element:


        if(subelement.attrib['id'][0] == '1'): # testcase1.xml
            outfile.write(subelement.attrib['id'])

            single_word = regex_single.findall(subelement.text)
            
            suggestions = spell_checker.correct(single_word[0])
            
            # printing the misspelled word.
            outfile.write(", "+single_word[0])

            i = 1
            # printing the suggestions.
            for each_suggestion in suggestions:
                outfile.write(", ")
                outfile.write(each_suggestion[0])

                i += 1
                if( i > MAX_SUGGESTIONS):
                    outfile.write("\n")
                    break

        elif( subelement.attrib['id'][0] == '2'): # testcase2.xml
            words_in_phrase = regex_phrase.findall( subelement.text)  

            # identifying the incorrect words in the phrase.
            i = 0;
            for i in xrange(0,len(words_in_phrase)):
                
                # if it is a punctuations then we should not query the dictionary.
                if( isPunctuation(words_in_phrase[i])):
                    continue

                suggestions = spell_checker.correct(words_in_phrase[i])
                if( len(suggestions) == 1): # correct word.
                    continue

                outfile.write(subelement.attrib['id'])
                incorrect_word = words_in_phrase[i]
                outfile.write(", "+incorrect_word)

                temp_list = []
                for each_suggestion in suggestions[:MAX_UNIGRAM_SUGGESTIONS] :
                    words_in_phrase[i] = each_suggestion[0]
                    temp_list.append( ( each_suggestion[0], ngrams.getProbabilityOfPhrase(words_in_phrase,100,False)))


                temp_list.sort( key = getSecond, reverse=True)

                j = 1
                # printing the suggestions.
                for each_temp in temp_list:
                    outfile.write(", ")
                    outfile.write(each_temp[0])

                    j += 1
                    if( j > MAX_SUGGESTIONS):
                        outfile.write("\n")
                        break

        # handling the testcases3
        elif(subelement.attrib['id'][0] == '3'): # testcases3.xml
            sentence = subelement.text

            words_in_sentence = regex.findall(sentence) # TODO: dot is added here.

            # identifying the incorrect words in the sentence.
            i = 0;
            for i in xrange(0,len(words_in_sentence)):
                
                # if it is a punctuations then we should not query the dictionary.
                if( isPunctuation(words_in_sentence[i])):
                    continue

                suggestions = spell_checker.correct(words_in_sentence[i])
                if( len(suggestions) == 1): # correct word.
                    continue

                # patch.
                for k in xrange(0,len(suggestions)):
                    suggestions[k] = suggestions[k][0]


                outfile.write(subelement.attrib['id'])
                incorrect_word = words_in_sentence[i]
                outfile.write(", "+incorrect_word)

                # creating a new list to call the correctSentences function.
                aux_list = []
                for t in xrange(0,(len(words_in_sentence)-1)):
                    aux_list.append([words_in_sentence[t]])
                    
                aux_list[i] = suggestions[:MAX_SUGGESTIONS]
                print aux_list
                sorted_suggestions = pos_ngrams.correctSentences(aux_list)
                
                j = 1
                # printing the suggestions.
                for each_sorted_suggestion in sorted_suggestions:
                    outfile.write(", ")
                    outfile.write(each_sorted_suggestion)

                    j += 1
                    if( j > MAX_SUGGESTIONS):
                        outfile.write("\n")
                        break

                
        # handling the testcases4
        elif(subelement.attrib['id'][0] == '4'): # testcases4.xml

            sentences = subelement.text.split('.')             # dot is the sentence separator.
            
            for each_sentence in sentences:
                words_in_sentence = regex.findall(each_sentence) # a list is returned.
                
                # identifying the incorrect words in the sentence.
                i = 0;
                for i in xrange(0,len(words_in_sentence)):
                
                    # if it is a punctuations then we should not query the dictionary.
                    if( isPunctuation(words_in_sentence[i])):
                        continue

                    suggestions = spell_checker.correct(words_in_sentence[i])
                    if( len(suggestions) == 1): # correct word.
                        continue

                    # patch.
                    for k in xrange(0,len(suggestions)):
                        suggestions[k] = suggestions[k][0]

                    outfile.write(subelement.attrib['id'])
                    incorrect_word = words_in_sentence[i]
                    outfile.write(", "+incorrect_word)

                    # creating a new list to call the correctSentences function.
                    aux_list = []
                    for t in xrange(0,len(words_in_sentence)):
                        aux_list.append([words_in_sentence[t]])
                        
                    aux_list[i] = suggestions[:MAX_SUGGESTIONS]
                    print aux_list
                    sorted_suggestions = pos_ngrams.correctSentences(aux_list)
                    
                    j = 1
                    # printing the suggestions.
                    for each_sorted_suggestion in sorted_suggestions:
                        outfile.write(", ")
                        outfile.write(each_sorted_suggestion)

                        j += 1
                        if( j > MAX_SUGGESTIONS):
                            outfile.write("\n")
                            break

                
                        
    file.close()
    outfile.close()

                        
                        
        
