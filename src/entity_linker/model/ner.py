import functools
import re

import spacy


ENTITY_LABEL_BLACKLIST = (
    'TIME',
    'PERCENT',
    'MONEY',
    'QUANTITY',
    'ORDINAL',
    'CARDINAL',
)


@functools.lru_cache(maxsize=None)
def load_spacy_model():
    return spacy.load('en_core_web_sm', disable=['tagger', 'parser'])


def mentions(text):
    nlp = load_spacy_model()
    doc = nlp(re.sub('\\s+', ' ', text))

    return [ent.text for ent in doc.ents if ent.label_ not in ENTITY_LABEL_BLACKLIST]
