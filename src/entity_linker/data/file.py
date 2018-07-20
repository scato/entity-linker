import os


WIKIPEDIA_ROOT = 'https://dumps.wikimedia.org/enwiki/latest'
LOCAL_ROOT = 'tmp/data'


def wikipedia_file_is_present(filename):
    local_file = '{}/{}'.format(LOCAL_ROOT, filename)

    return os.path.isfile(local_file)


def download_wikipedia_file(filename):
    wikipedia_file = '{}/{}'.format(WIKIPEDIA_ROOT, filename)
    local_file = '{}/{}'.format(LOCAL_ROOT, filename)

    os.makedirs(LOCAL_ROOT, exist_ok=True)
    os.system(
        'wget {} -O {}'.format(wikipedia_file, local_file)
    )
