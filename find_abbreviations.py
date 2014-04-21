#!/usr/bin/env python
# -*- coding: utf-8 -*-

######################################
#   Abbreviations Finder v. 0.1      #
#   Author: Błażej Kubiński          #
######################################

# This simple script is meant to find as many abbreviations in text as possible.
# Firstly, it splits text into words. The only rule used here is splitting
# by whitespace. Next it uses four regular expressions to find shortcuts.
# Additional features of this scripts are:
#   * comparing results to a ready list of abbreviations in a file
#   * statistics which regular expression have found the abbreviations
#   * general statistics concerning abbreviations that have been found

import sys
import re
import getopt
reload(sys)
sys.setdefaultencoding('utf-8')

# Some useful CONSTANTS which may be used a few times in the script
WHITESPACE  = [ch for ch in " \t\n\r\f\v"]          # Needed to split words
LETTERS     = [ch for ch in "aąbcćdeęfghijklłmnńoópqrsśtuvwxyzźż"]
CONSONANTS  = [ch for ch in "bcćdfghjklłmnńpqrsśtvwxzźż"]
VOWELS = [ch for ch in "aąeęioóuy"]
 
digits = re.compile("^[0-9]+$")

### Polish abbreviations patterns

# single letter, for example: "a." (stands for "albo") or "B." like in "President B. Obama"
single_letter_pattern = re.compile("^[A-Za-z]\.$")
# abbreviations with vowels, example: p.n.e. (przed naszą erą),   
vowels = re.compile("^([a-ząćęłńóśźż]\.)+$")
# only consonants (example: np. (na przykład), jw. (jak wyżej))     
only_consonants = re.compile("^[bcćdfghjklłmnńpqrsśtvwxzźż]+\.$")
# followed by punctuation, ","   
followed_by_punc = re.compile("[a-ząćęłńóśźż]+\.[,;:]$")
# two words connected with a hyphen, (e.g. "pd.-zach.")
with_hyphen = re.compile("[a-ząćęłńóśźż]+\.-[a-ząćęłńóśźż]+\.$")
# many connected abbreviations (e.g. 'dz.urz.')    
more_than_one = re.compile("([a-ząćęłńóśźż]+\.){2,}$")
# if the first word ends with a dot and the second one begins with a small letter      
bigram_rule = re.compile("^[a-z]+\. [a-ząćężźółńś]+$")   

abbr_patterns = [
    single_letter_pattern,
    vowels,
    only_consonants,
    followed_by_punc,
    with_hyphen,
    more_than_one
]

abbr_dictionary = {}    # dictionary of abbreviation and count of occurences
pattern_matches = {}    # dictionary of patterns and how many abbreviations they found
found_in_list = []
not_found_in_list= {}

""" 
Finds abbreviations in bigrams. If the first word ends with
a dot and the second one starts with a small letter,
the first one is treated as an abbreviation
"""
def bigram_find(sequence, number=3):
    for i in range(len(sequence)-number+1):
        #sys.stdout.write("%s\n" % sequence[i:i+number])
        word_to_check = sequence[i] + ' ' + sequence[i+1]
        if bigram_rule.match(word_to_check):
            abbr_dictionary[sequence[i]] = abbr_dictionary.get(sequence[i], 0) + 1
            pattern_matches[bigram_rule] = pattern_matches.get(bigram_rule, 0) + 1
"""
Creates a list of abbreviations from given file
"""            
def get_abbreviations_from_file(location):
    print 'The file with list of abbreviations was named: ' + location[0]
    abbr_file = open(location[0], 'r')
    abbr_list = []
    for line in abbr_file:
        abbr_list.append(line.strip(' \t\n\r'))
    return abbr_list

"""
Writes short statistics about abbreviations found in given file
"""
def write_abbreviations_from_file_stats(abbr_file_list, abbr_dictionary):
    for abbr in sorted(abbr_dictionary):
        if abbr in abbr_file_list:
            found_in_list.append(abbr)
        else:
            not_found_in_list[abbr] = abbr_dictionary[abbr]
    tp = len(found_in_list) # found in list
    fp = len(not_found_in_list)
    if tp > 0:
        precision = float(tp) / float(tp + fp)
        coverage = float(tp) / float(len(abbr_file_list))
    print '\n'
    print '==============================='
    print 'Number of abbreviations in abbreviations list file: ' + str(len(abbr_file_list))
    print 'Number of abbreviations found by script: ' + str(len(abbr_dictionary))
    print 'Precision = ', str(tp), '/ (', str(tp), ' + ', str(fp), ') = ', str(precision)
    print 'Coverage = ', str(tp), ' / ', str(len(abbr_file_list)), ' = ', str(coverage)
    print '==============================='
    
def main(argv):
    abbr_list_file_location = ''
    is_summary = False
    abbr_file_list = []
    ### Parsing options and arguments
    try:
      opts, args = getopt.getopt(argv, "hfs", ["abbr_file="])
    except getopt.GetoptError:
        print 'Usage: find_abbreviations.py [-f file_with_abbreviations.txt]'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'Usage: find_abbreviations.py [-f file_with_abbreviations.txt]'
            print '\n'
            print '\t -f \t file containing list of abbreviations to compare'
            sys.exit(0)
        if opt == '-f':
            abbr_list_file_location = args
        if opt == '-s':
            is_summary = True
    
    for line in sys.stdin:
        line = line.decode('utf-8')
        tokens = line.encode('utf-8').split()
        if tokens:
            for token in tokens:
                for pattern in abbr_patterns:
                    if pattern.match(token):
                        # not effective - Delete last chars of abbreviations found by followed_by_punc
                        if pattern == followed_by_punc:
                            token = token[:-1]
                        abbr_dictionary[token] = abbr_dictionary.get(token, 0) + 1
                        pattern_matches[pattern] = pattern_matches.get(pattern, 0) + 1
        # testing bigram_rule
        bigram_find(tokens)
        
    #for abbr in sorted(abbr_dictionary):
    #    print(abbr + "\t " + str(abbr_dictionary[abbr]))
    
    # For debug purposes - how many abbrevietions were found by each pattern
    
    
    # Delete last chars of abbreviations found by followed_by_punc, so
    # abbreviations like 'np.,' become 'np.'
    # TODO: rename keys followed by puncts and delete wrong abbreviations
    #       for now every word is checked
    #for abbr in abbr_dictionary:
    #    if followed_by_punc.match(abbr):
    #        abbr_dictionary[abbr[:-1]] = abbr_dictionary.get(abbr[:-1], 0) + abbr_dictionary[abbr]
    #        del abbr_dictionary[abbr]
    
    # Simple print of results - abbreviations       number of occurences
    for sorted_item in sorted(abbr_dictionary, key=abbr_dictionary.get, reverse=True):
        print sorted_item, "\t\t", abbr_dictionary[sorted_item]
      
    if abbr_list_file_location:
        abbr_file_list = get_abbreviations_from_file(abbr_list_file_location)
        if is_summary:
            write_abbreviations_from_file_stats(abbr_file_list, abbr_dictionary)
        
    if is_summary:
        print '\n'
        print '==============================='
        print 'How many abbreviations were found by each pattern:'
        print '==============================='
        for patt in sorted(pattern_matches.iterkeys()):
            print(patt.pattern + "\t " + str(pattern_matches[patt]))
            
    if is_summary & (len(abbr_file_list) > 0):
        
        #print 'elements from file'
        #for element in abbr_file_list:
            #print element
        print '\n'
        print '==============================='
        print 'Abbreviations which were found on the list'
        print '==============================='
        for abbr in found_in_list:
            print abbr
        print '\n'
        print '==============================='
        print 'Abbreviations which were not found on the list'
        print '==============================='
        for sorted_item in sorted(not_found_in_list, key=not_found_in_list.get, reverse=True):
            print sorted_item, "\t\t", not_found_in_list[sorted_item]
        

if __name__ == "__main__":
    main(sys.argv[1:])
        
        
        

