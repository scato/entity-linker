import os


WIKIPEDIA_ROOT = 'https://dumps.wikimedia.org/enwiki/latest'
LOCAL_ROOT = 'tmp/data'


def download_wikipedia_file(filename):
    os.makedirs(LOCAL_ROOT, exist_ok=True)

    wikipedia_file = '{}/{}'.format(WIKIPEDIA_ROOT, filename)
    local_file = '{}/{}'.format(LOCAL_ROOT, filename)

    if not os.path.isfile(local_file):
        os.system(
            'wget {} -O {}'.format(wikipedia_file, local_file)
        )
