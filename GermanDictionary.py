import requests
from bs4 import BeautifulSoup

class CambridgeDictionaryScraper:
    """
    Basic functionality for scraping definitions from: https://dictionary.cambridge.org
    """
    def __init__(self, html_definition_class: str):
        self.html_definition_class = html_definition_class
        self.base_url = f'https://dictionary.cambridge.org/us/dictionary/{html_definition_class}'

    def _get_html(self, word: str) -> str:
        """
        Scrape the webpage of a specific word from the dictionary website and
        return the html
        """
        url = f'{self.base_url}/{word}'

        res = requests.get(url, headers={"User-Agent": "XY"})
        if not res.ok:
            print(f'Unable to scrape the website for: {word}')
            return ''

        return res.content

    def _get_definitions(self, web_page_html: str) -> list[(str, str)]:
        """
        Takes in HTML representing a word definition and parses out the definitions
        Returns a list of tuples in the form: (part of speech, translation)
        """
        web_page_soup = BeautifulSoup(web_page_html, 'lxml')
        definition_tags = web_page_soup.find_all('div', attrs={'class': self.html_definition_class})
        output = []

        for definition in definition_tags:
            part_of_speech = definition.find('span', attrs={'class': 'pos'}).text
            translation = definition.find('span', attrs={'class': 'trans dtrans'}).text
            output.append((part_of_speech, translation))
        
        return output

    def get_word(self, word):
        word_html = self._get_html(word)
        return self._get_definitions(word_html)


class EnglishGermanDictionary:
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





