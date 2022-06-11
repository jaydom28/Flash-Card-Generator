from src.modules.Anki import VocabularyCardMaker
from src.modules.CambridgeDictionary import CambridgeDictionaryScraper, EnglishGermanDictionary, GermanEnglishDictionary

de_en = GermanEnglishDictionary()
en_de = EnglishGermanDictionary()

translation1 = de_en.get_word('Ente')
translation2 = de_en.get_word('teuer')
translation3 = de_en.get_word('schwarz')
translation4 = de_en.get_word('nutzlich')
translation5 = de_en.get_word('schnell')

print(translation1)
print(translation2)
print(translation3)
print(translation4)
print(translation5)

# print(translation1)
# print(translation2)
