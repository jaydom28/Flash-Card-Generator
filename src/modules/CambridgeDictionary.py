"""
This module contains implementation for the Cambridge Dictionary web scrapers
"""
import requests

from typing import Optional

from bs4 import BeautifulSoup

class CambridgeDictionaryScraper:
    """
    Basic functionality for scraping definitions from: https://dictionary.cambridge.org
    """
    def __init__(self, language: str):
        self.language = language
        self.base_url = f'https://dictionary.cambridge.org/us/dictionary/{self.language}'

    def _get_html(self, word: str) -> str:
        """
        Scrape the webpage of a specific word from the dictionary website and
        return the html as a string
        """
        url = f'{self.base_url}/{word}'

        res = requests.get(url, headers={"User-Agent": "XY"})
        if not res.ok:
            print(f'Unable to scrape Cambridge Dictionary for: {word}')
            return ''

        return res.content

    def _get_definitions(self, web_page_html: str) -> list[tuple[str, str]]:
        """
        Takes in HTML representing the web page of a word from the cambridge
        dictionary website and parses out the translations
        Returns a list of tuples in the form:
            (part of speech, translation)
        """
        web_page_soup = BeautifulSoup(web_page_html, 'lxml')
        translation_soups = web_page_soup.find_all('div', attrs={'class': self.language})
        output = []

        for soup in translation_soups:
            part_of_speech = soup.find('span', attrs={'class': 'pos'}).text
            word = soup.find('span', attrs={'class': 'trans dtrans'}).text
            output.append((part_of_speech, word))
        
        return output

    def get_word(self, word: str) -> list[tuple[str, str]]:
        """
        Takes in a word as a string and then returns a list of translations for the word
        Returns a list of tuples in the form:
            (part of speech, translation)
        """
        word_html = self._get_html(word)
        return self._get_definitions(word_html)


class EnglishGermanDictionary(CambridgeDictionaryScraper):
    """
    Scrapes definitions from the cambridge dictionary website for English - German translations
    """
    def __init__(self):
        super().__init__('english-german')


class GermanEnglishDictionary(CambridgeDictionaryScraper):
    """
    Scrapes definitions from the cambridge dictionary website for German - English translations
    """
    def __init__(self):
        super().__init__('german-english')


def get_dictionary(from_language: str, to_language: str) -> Optional[CambridgeDictionaryScraper]:
    """
    Takes in two languages and returns the correct dictionary to be used
    """
    language_tuple = (from_language, to_language)

    if language_tuple == ('en', 'de'):
        return EnglishGermanDictionary()

    if language_tuple == ('de', 'en'):
        return GermanEnglishDictionary()

    print('There is no currently implemented dictionary object with the type: {from_language} -> {to_language}') 
    return None
