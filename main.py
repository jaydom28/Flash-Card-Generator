import requests
import sys

from bs4 import BeautifulSoup

from GermanDictionary import EnglishGermanDictionary, GermanEnglishDictionary


english_german_dictionary = EnglishGermanDictionary()
german_english_dictionary = GermanEnglishDictionary()

words = sys.argv[1:]

for word in words:
    print('Here are translations for: {word}')
    for (pos, translation) in english_german_dictionary.get_word(word):
        print(f'{pos}: {translation}')


# STEP 1: Get the words to translate
# STEP 2: Scrape the definitions of all the words
# STEP 3: Format the definitions in a CSV file
# Would be cool to get pictures too for the definitions
