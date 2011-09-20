import spell_checker            # Assuming it is in the same directory.
from xml.etree import ElementTree as ET
import re


MAX_UNIGRAM_SUGGESTIONS = 10
MAX_SUGGESTIONS = 5

# function to read the input file which is in xml format
# and write the output to the output file.
def test(input_file_name,output_file_name):
    file = open(input_file_name)
    data = file.read()
    element = ET.XML(data)

    outfile = open(output_file_name,"w")
    
    # regex for single word.
    regex_single = re.compile('\w+')
    
    # creating the regex obj.
    regex = re.compile('\w+|[.|,|:|(|)|\'|\"]')


    
    for subelement in element:
        outfile.write(subelement.attrib['id'])

        if(subelement.attrib['id'][0] == '1'): # testcase1.xml
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

                
        else:
            sentences = subelement.text.split('.')             # dot is the sentence separator.
            
            for each_sentence in sentences:
                words_in_sentence = regex.findall(each_sentence) # a list is returned.
                
                lolists = []
                for each_word in words_in_sentence:
                    
                    # Check whether the word is present in the dictionary.
                    suggestions = spell_checker.correct(each_word)
                    new_suggestions = []
                    for each_suggestion in suggestions:
                        new_suggestions.append(each_suggestion[0])
                        
                    lolists.append(new_suggestions[:MAX_UNIGRAM_SUGGESTIONS])
                    
                print lolists

                
                        
    file.close()
    outfile.close()

                        
                        
        
