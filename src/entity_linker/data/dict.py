import itertools
import os

from gensim.corpora import Dictionary

from entity_linker.data.file import LOCAL_ROOT
from entity_linker.data.json import read_json_data


def entity_dict_is_present():
    local_file = os.path.join(LOCAL_ROOT, 'entities.dict')

    return os.path.isfile(local_file)


def build_entity_dict():
    entities_dict_filename = os.path.join(LOCAL_ROOT, 'entities.dict')

    outgoing = itertools.chain(
        read_json_data('training', 'outgoing.json.gz'),
        read_json_data('validation', 'outgoing.json.gz'),
        read_json_data('test', 'outgoing.json.gz'),
    )

    documents = (record['outgoing_entity_ids'] for record in outgoing)
    entities_dict = Dictionary.from_documents(documents)

    entities_dict.save(entities_dict_filename)


def load_entity_dict():
    entities_dict_filename = os.path.join(LOCAL_ROOT, 'entities.dict')

    return Dictionary.load(entities_dict_filename)


def mention_dict_is_present():
    local_file = os.path.join(LOCAL_ROOT, 'mentions.dict')

    return os.path.isfile(local_file)


def build_mention_dict():
    mentions_dict_filename = os.path.join(LOCAL_ROOT, 'mentions.dict')

    mentions = itertools.chain(
        read_json_data('training', 'mentions.json.gz'),
        read_json_data('validation', 'mentions.json.gz'),
        read_json_data('test', 'mentions.json.gz'),
    )

    documents = (record['mentions'] for record in mentions)
    mentions_dict = Dictionary.from_documents(documents)

    mentions_dict.save(mentions_dict_filename)


def load_mention_dict():
    mentions_dict_filename = os.path.join(LOCAL_ROOT, 'mentions.dict')

    return Dictionary.load(mentions_dict_filename)
