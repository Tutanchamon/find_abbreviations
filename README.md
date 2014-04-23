find_abbreviations
==================

A very simple python script which finds abbreviations in texts.
The result is a list of abbreviations and how many times they occured in given text.

It is possible to give a path to already prepared list of known abbreviations and do the comparison.

That is my first script bigger than 5-10 lines so it is very far from being perfect.

The scripts takes the standard input and writes the results to the standard output.

Usage: python find_abbreviations.py [-f file_with_list_of_abbreviations] [-s]

    -f    Path to the file which contains of prepared list of abbreviations for testing purposes
          Every abbreviation should be placed in a new line
    -s    Writes summary: how many abbreviations have been found, how many from them were present in test file
