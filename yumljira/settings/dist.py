from .base import *

DEBUG = False

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static', 'dist')
]

WEBPACK_MANIFEST_FILE = os.path.join(BASE_DIR, '../manifest-dist.json')

