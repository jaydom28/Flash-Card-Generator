import codecs

from pprint import pprint as pp

from src.modules.Anki import VocabularyCardMaker
from src.modules.CambridgeDictionary import CambridgeDictionaryScraper, EnglishGermanDictionary, GermanEnglishDictionary
from src.modules import CsvFlashCards

de_en = GermanEnglishDictionary()
en_de = EnglishGermanDictionary()

translations = []
translations.extend(de_en.get_word('Ente'))
translations.extend(de_en.get_word('teuer'))
translations.extend(de_en.get_word('schnell'))
translations.extend(de_en.get_word('sprechen'))

pp(translations)
# print(translation2)
# print(translation3)
# print(translation4)
# print(translation5)

print(de_en.get_word('blah'))

exit()

card_tuples = []
for translation in translations:
    # pp(CsvFlashCards.create_flashcard(translation))
    card_tuples.append(CsvFlashCards.create_flashcard(translation))

csv_data = CsvFlashCards.to_csv(card_tuples, delim='\t')
print(csv_data)

with codecs.open('test_csv.csv', 'w', 'utf-8') as handle:
    handle.write(csv_data)

# print(translation1)
# print(translation2)
