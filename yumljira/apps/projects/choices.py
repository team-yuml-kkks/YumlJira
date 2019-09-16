from django.utils.translation import gettext as _

LOW = 'Low'
MEDIUM = 'Medium'
HIGH = 'High'

PRIORITIES = (
    (_(LOW), LOW),
    (_(MEDIUM), MEDIUM),
    (_(HIGH), HIGH),
)

PRIORITIES_KEYS = [i[0] for i in PRIORITIES]

