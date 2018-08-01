import logging
import sys
from itertools import islice

from sklearn.model_selection import train_test_split

from entity_linker.data.dict import entity_dict_is_present, build_entity_dict, \
    mention_dict_is_present, build_mention_dict
from entity_linker.data.file import download_wikipedia_file, wikipedia_file_is_present
from entity_linker.data.wiki import write_features, feature_files_are_present
from entity_linker.data.xml import read_redirects, read_pages


def create_data_sets():
    logger = logging.getLogger('entity_linker')

    # FILENAME = 'enwiki-latest-pages-articles.xml.bz2'
    FILENAME = 'enwiki-latest-pages-articles1.xml-p10p30302.bz2'

    if not wikipedia_file_is_present(FILENAME):
        logger.info('Downloading XML...')

        download_wikipedia_file(FILENAME)

    if not feature_files_are_present('training', 'validation', 'test'):
        logger.info('Extracting features...')

        logger.debug('Loading redirects...')
        redirects = read_redirects(FILENAME)
        aliases = dict(redirects)

        # pages = list(read_pages(FILENAME))
        pages = list(islice(read_pages(FILENAME), 100))
        pages_training, pages_other = train_test_split(pages, test_size=0.5)
        pages_validation, pages_test = train_test_split(pages_other, test_size=0.5)

        logger.debug('Writing training data set...')
        write_features(pages_training, aliases, 'training')

        logger.debug('Writing validation data set...')
        write_features(pages_validation, aliases, 'validation')

        logger.debug('Writing test data set...')
        write_features(pages_test, aliases, 'test')

    if not entity_dict_is_present():
        logger.info('Preparing entity dictionary...')

        build_entity_dict()

    if not mention_dict_is_present():
        logger.info('Preparing mention dictionary...')

        build_mention_dict()


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    create_data_sets()
