import codecs

from pprint import pprint as pp
from typing import Tuple, List, Dict, Iterator


GERMAN_ARTICLE_MAP = {
    'feminine': 'die',
    'plural': 'die',
    'masculine': 'der',
    'neuter': 'das',
}

TAGS_FIELD = '{{Tags}}'


def get_examples_string(examples: Iterator[str]) -> str:
    """
    Creates a string that represents a sequence of examples that can be imported into Anki from a CSV file
    """
    examples_list = list(examples)
    if not examples_list:
        return ''
    
    output = '\n'.join((f'<li class="example-list-item">{e}</li>' for e in examples_list))

    return '<ol class="example-list">\n' + 'Examples\n' + output + '\n</ol>'



def get_tags_string(tags: List[str], delim=' ') -> str:
    """
    Takes in a list of tags and formats it into a string which can be imported into Anki from a CSV file
    """
    return delim.join(tags)


def get_noun_plural(translation: Dict) -> str:
    """
    Takes in a dictionary representing a German noun from Cambridge Dictionary and returns the plural form of the word
    """
    return next((word for (case, p_form, word, *_) in translation['forms']
                if (case, p_form) == ('nominative', 'plural')), '')


def create_noun_flashcard(translation: Dict) -> List[Tuple[str, str, str]]:
    """
    Takes in a dictionary representing German noun and exports a tuple representing sides of a flash card
    """
    pos = translation['pos']
    front_side = f'{translation["english_translation"]} (en)'

    article = GERMAN_ARTICLE_MAP.get(translation['gender'].split('-')[0], '')
    plural_form = get_noun_plural(translation)
    if not (article and plural_form):
        return ('', '', '')

    back_side = f'{article} {translation["word"]}, {GERMAN_ARTICLE_MAP["plural"]} {plural_form}\n\n'

    examples = get_examples_string(translation['examples'][:3])
    if examples:
        back_side += examples + '\n'

    tags = get_tags_string(['noun', 'english-german'])
    return (front_side, back_side, tags)


def create_verb_flashcard(translation: Dict) -> List[Tuple[str, str, str]]:
    """
    Takes in a dictionary representing German verb and exports a tuple representing sides of a flash card
    """
    front_side = f'{translation["english_translation"]} (en)'
    back_side = translation['word'] + '\n'

    forms = []
    for form in translation['forms']:
        if len(form) == 4:
            _, _, tense, word = form
        else:
            tense, word = form
        if tense == 'present':
            continue

        forms.append(f'{tense} {word}')
        back_side += f'{tense} {word}\n'

    examples = get_examples_string(translation['examples'][:3])
    if examples:
        back_side += examples + '\n'

    tags = get_tags_string(['verb', 'english-german'])
    return (front_side, back_side, tags)


def create_adjective_flashcard(translation: Dict) -> List[Tuple[str, str, str]]:
    """
    Takes in a dictionary representing a German adjective and exports a tuple representing sides of a flash card
    """
    front_side = f'{translation["english_translation"]} (en)'
    back_side = translation['word'] + '\n'

    for (case, word) in translation['forms']:
        back_side += f'{case} {word}\n'

    examples = get_examples_string(translation['examples'][:3])
    if examples:
        back_side += examples + '\n'

    tags = get_tags_string(['adjective', 'english-german'])
    return (front_side, back_side, tags)


def create_adverb_flashcard(translation: Dict) -> List[Tuple[str, str, str]]:
    """
    Takes in a dictionary representing a German adverb and exports a tuple representing sides of a flash card
    """
    front_side = f'{translation["english_translation"]} (en)'

    back_side = translation['word'] + '\n'

    examples = get_examples_string(translation['examples'][:3])
    if examples:
        back_side += examples + '\n'

    tags = get_tags_string(['adverb', 'english-german'])
    return (front_side, back_side, tags)


def create_flashcard_tuple(translation: Dict) -> List[Tuple[str, str, str]]:
    """
    Takes in a dictionary representing a German translation and creates a tuple representing sides of a flash card
    Returns the tuple in the form:
        (front side, back side, tags)
    """
    pos = translation['pos']
    
    if pos == 'noun':
        return create_noun_flashcard(translation)
    elif pos == 'verb':
        return create_verb_flashcard(translation)
    elif pos == 'adverb':
        return create_adverb_flashcard(translation)
    elif pos == 'adjective':
        return create_adjective_flashcard(translation)
    else:
        print('{pos} words are not supported')
        return ('', '', '')


def card_tuples_to_csv(card_tuples: Iterator[Tuple[str, str, str]], delim=',') -> str:
    """
    Takes in an iterable sequence of tuples representing sides of a flash card and outputs a CSV representation of the tuple
    """
    output = ''

    for card_tuple in card_tuples:
        card_tuple = (f.replace('"', '""') for f in card_tuple)
        card_tuple = (f.replace('\n', '<br>') for f in card_tuple)
        tmp = delim.join([f'"{field}"' for field in card_tuple])
        output += tmp + '\n'

    return output


def write_csv(file_path: str, data: str) -> None:
    with codecs.open(file_path, 'w', 'utf-8') as handle:
        handle.write(data)