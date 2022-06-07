from genanki import Note, Model, Deck, Package

class VocabularyCardMaker:
    def __init__(self, name: str) -> None:
        self.name = name
        self.model = Model(
            model_id=2157302217,
            name='Vocabulary Card',
            fields=[{'name': 'Side1'},{'name': 'Side2'}],
            templates=[{
              'name': 'Card 1',
              'qfmt': '{{Side1}}',
              'afmt': '{{Side2}}',
            }]
        )
        self.deck = Deck(deck_id=2157302217, name=self.name)

    def create_note(self, side1: str, side2: str) -> Note:
        return Note(model=self.model, fields=[side1, side2])

    def create_and_add_note(self, side1: str, side2: str) -> bool:
        note = Note(model=self.model, fields=[side1, side2])
        self.deck.add_note(note)
        return True

    def export_deck(self, file_path: str) -> None: 
        Package(self.deck).write_to_file(file_path)
