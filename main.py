import os
import requests
import sys

from CambridgeDictionary import get_dictionary


def get_word_of_string(string: str) -> str:
    """
    Takes in a string and returns the first word of the string
    """
    return string.split()[0]


def usage() -> None:
    script_name = os.path.basename(__file__)
    print('USAGE:')
    print(f'\tpython {script_name} [WORDS]')
    sys.exit(1)


def word_loop() -> None:
    en_de_dictionary = get_dictionary('en', 'de')
    de_en_dictionary = get_dictionary('de', 'en')
    for line in sys.stdin:
        word = get_word_of_string(line)
        translations = de_en_dictionary.get_word(word) or en_de_dictionary.get_word(word)
        if not translations:
            print(f'Unable to get definition for: {word}')
            continue
        
        for (pos, translation) in translations:
            print(f'{pos} -> {translation}')


def main():
    # STEP 1: Get the words to translate
    if len(sys.argv) <= 2:
        word_loop()
        sys.exit(0)

    english_german_dictionary = get_dictionary('en', 'de')
    german_english_dictionary = get_dictionary('de', 'en')
    words_file = sys.argv[1]

    # STEP 2: Scrape the definitions of all the words

    # STEP 3: Format the definitions in a CSV file

    # Would be cool to get pictures too for the definitions
    print('AYO')

if __name__ == '__main__':
    main()

