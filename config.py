DEBUG = True

import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = BASE_DIR + '/dat'
ALLOWED_EXTENSIONS = set(['tsv', 'csv'])

