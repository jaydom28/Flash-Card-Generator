"""
This module contains implementation for the Cambridge Dictionary web scrapers
"""
from gettext import translation
import requests

from typing import Dict, Optional, List, Tuple

from bs4 import BeautifulSoup, NavigableString, Tag

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

    def _get_definitions(self, web_page_html: str) -> List[Tuple[str, str]]:
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

    def get_word(self, word: str) -> List[Tuple[str, str]]:
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

    def _scrape_gender(self, translation_soup: BeautifulSoup) -> str:
        gender_soup = translation_soup.find('span', attrs={'class': 'gc'})
        gender = ''
        if gender_soup:
            gender = gender_soup.text

        return gender

    def _scrape_forms(self, translation_soup: BeautifulSoup) -> str:
        form_elements = translation_soup.find_all('span', attrs={'class': 'inf-group'})
        forms = []
        for form in form_elements:
            tags = (el for el in form if isinstance(el, Tag))
            f = tuple(t.text for t in tags)
            forms.append(f)

        return forms

    def _scrape_word(self, translation_soup: BeautifulSoup) -> str:
        word_soup = translation_soup.find('span', attrs={'class': 'dtrans'})
        return word_soup.text
    
    def _scrape_examples(self, translation_soup: BeautifulSoup) -> str:
        example_soups = (t for t in translation_soup.find_all('span', attrs={'class': 'eg deg'}) if isinstance(t, Tag))
        return [e.text for e in example_soups]


    def _get_definitions(self, web_page_html: str) -> List[Dict]:
        """
        Takes in HTML representing the web page of a word from the cambridge
        dictionary website and parses out the translations
        Returns a list of tuples in the form:
            (part of speech, translation)
        """
        web_page_soup = BeautifulSoup(web_page_html, 'lxml')
        translations = web_page_soup.find_all('div', attrs={'class': 'kdic'})
        parts_of_speech = set()

        output = []
        for translation_soup in translations:
            translation = {}

            translated_word = translation_soup.find('h2', attrs={'class': 'di-title'}).text
            translation['word'] = translated_word

            part_of_speech = translation_soup.find('span', attrs={'class': 'dpos'}).text
            translation['pos'] = part_of_speech
            if part_of_speech in parts_of_speech:
                break

            parts_of_speech.add(part_of_speech)

            if part_of_speech.lower() == "noun":
                gender = self._scrape_gender(translation_soup)
                translation['gender'] = gender

            translation['forms'] = self._scrape_forms(translation_soup)
            translation['english_translation'] = self._scrape_word(translation_soup)
            translation['examples'] = self._scrape_examples(translation_soup)

            output.append(translation)

        return output


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
