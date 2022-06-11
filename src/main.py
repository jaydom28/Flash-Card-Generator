"""
Flash Card Generator driver file
"""
import os
import sys

from typing import List, Dict, Tuple, Iterator

from modules import CsvFlashCards
from modules import general
from modules.CambridgeDictionary import GermanEnglishDictionary, EnglishGermanDictionary


def usage() -> None:
    """
    Prints out the basic usage of the script
    """
    script_name = os.path.basename(__file__)
    print('USAGE:')
    print(f'\tpython {script_name} [WORDS]')


def get_words_from_stdin() -> List[str]:
    """
    Infinite loop that reads from stdin until EOF is reached and appends each line to a list
    """
    output = []

    for line in sys.stdin:
        output.append(line.strip())

    return output


def get_words() -> List[str]:
    """
    Return a list of strings from either STDIN if no args are passed in, or from the file paths passed in
    """
    words = []
    if len(sys.argv) < 2:
        words.extend(get_words_from_stdin())
    else:
        words = []
        for words_file in sys.argv[1:]:
            words_file = sys.argv[1]
            if not os.path.exists(words_file):
                print(f'Unable to find the file: {words_file}')
                return 1
            file_lines = general.get_lines_from_file(words_file) 
            words.extend(list(file_lines))

    return words


def get_definitions(words: Iterator[str]) -> Iterator[Dict]:
    """
    Take in an iterable sequence of words as strings and output an iterator to translations for each every word
    """
    en_de = EnglishGermanDictionary()
    de_en = GermanEnglishDictionary()

    for word in words:
        german_translations = de_en.get_word(word)
        if not german_translations:
            print(f'FAIL: {word}')
            continue

        print(f'SUCCESS: {word}')
        for translation in german_translations:
            yield translation


def create_card_tuples_from_translations(translations: Iterator[Dict]) -> Iterator[Tuple[str, str, str]]:
    return (CsvFlashCards.create_flashcard_tuple(t) for t in translations)


def main():
    # STEP 1: Get the words to translate
    words = get_words()
    print(f'Creating flashcards for {len(words)} words')

    # STEP 2: Scrape the definitions of all the words
    translations = get_definitions(words)

    # STEP 3: Format the definitions in a CSV file
    file_path = 'definitions.txt'
    flash_card_tuples = create_card_tuples_from_translations(translations)
    flash_card_tuples = (t for t in flash_card_tuples if t != ('', '', ''))
    flash_card_csv = CsvFlashCards.card_tuples_to_csv(flash_card_tuples, delim='\t')
    CsvFlashCards.write_csv(file_path, flash_card_csv)

    # Would be cool to get pictures too for the definitions

if __name__ == '__main__':
    sys.exit(main())
