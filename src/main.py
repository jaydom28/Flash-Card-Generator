"""
Flash Card Generator driver file
"""
import os
import requests
import sys

from modules.CambridgeDictionary import GermanEnglishDictionary, EnglishGermanDictionary
from modules import general
from modules.Anki import VocabularyCardMaker


def get_word_from_string(string: str) -> str:
    """
    Takes in a string and returns the first word of the string
    """
    return string.split()[0]


def usage() -> None:
    """
    Prints out the basic usage of the script
    """
    script_name = os.path.basename(__file__)
    print('USAGE:')
    print(f'\tpython {script_name} [WORDS]')


def word_loop() -> None:
    """
    Infinite loop that takes in a word that can be either German or English and then returns translations, stops when
    EOF is reached
    """
    en_de = EnglishGermanDictionary()
    de_en = GermanEnglishDictionary()

    for line in sys.stdin:
        word = line.strip()
        translations = de_en.get_word(word) or en_de.get_word(word)
        if not translations:
            print(f'Unable to get definition for: {word}')
            continue
        
        for (pos, translation) in translations:
            print(f'{pos} -> {translation}')


def main():
    # STEP 1: Get the words to translate
    if len(sys.argv) < 2:
        word_loop()
        return 0

    en_de = EnglishGermanDictionary()
    de_en = GermanEnglishDictionary()

    words_file = sys.argv[1]
    if not os.path.exists(words_file):
        print(f'Unable to find the file: {words_file}')
        return 1


    # STEP 2: Scrape the definitions of all the words
    card_maker = VocabularyCardMaker('German Vocabulary')
    file_lines = general.get_lines_from_file(words_file)
    for line in file_lines:
        english_translations = de_en.get_word(line)
        if not english_translations:
            print(f'Unable to find definition for: {line}')

        for (pos, translation) in english_translations:
            english_side = line
            german_side = f'{translation} ({pos})'
            print(f'{english_side} -> {german_side}')
            card_maker.create_and_add_note(english_side, german_side)

    card_maker.export_deck('test_deck.apkg')

    # STEP 3: Format the definitions in a CSV file

    # Would be cool to get pictures too for the definitions

if __name__ == '__main__':
    sys.exit(main())
