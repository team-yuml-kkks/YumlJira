from django.utils.translation import gettext as _

LOW = 'Low'
MEDIUM = 'Medium'
HIGH = 'High'

PRIORITIES = (
    (LOW, _(LOW)),
    (MEDIUM, _(MEDIUM)),
    (HIGH, _(HIGH)),
)

PRIORITIES_KEYS = [i[0] for i in PRIORITIES]

BUG = 'BUG'
SUBTASK = 'SUBTASK'
STORY = 'STORY'

TASK_TYPES = (
    (BUG, _('Bug')),
    (SUBTASK, _('Sub task')),
    (STORY, _('Story')),
)

TASK_TYPES_KEYS = [i[0] for i in TASK_TYPES]

HOUR = 'h'
MINUTE = 'm'
DAY = 'd'
WEEK = 'w'

AVAILABLE_TIME_OPTIONS = [HOUR, MINUTE, DAY, WEEK]

OPTION_TO_MINUTE = {
    MINUTE: 1,
    HOUR: 60,
    DAY: 1440,
    WEEK: 10080,
}

