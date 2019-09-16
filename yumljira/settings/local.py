from .base import *

DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static', 'local')
]

WEBPACK_MANIFEST_FILE = os.path.join(BASE_DIR, '../manifest-local.json')

