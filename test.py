from src.modules.Anki import VocabularyCardMaker


card_maker = VocabularyCardMaker('German-English')
card_maker.create_and_add_note('Bird', 'Der Vogel')
card_maker.export_deck('test_deck.apkg')
