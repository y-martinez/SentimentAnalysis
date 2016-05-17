DEBUG = True

import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DATA_FOLDER = BASE_DIR + '/dat'
ALLOWED_EXTENSIONS = set(['tsv'])

CSRF_ENABLED     = True
CSRF_SESSION_KEY = "secret"
SECRET_KEY = "secret"

