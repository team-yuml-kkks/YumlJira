from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _

from model_utils.models import TimeStampedModel

from .choices import *


class Project(TimeStampedModel):
    name = models.CharField(_('Project name'), max_length=255)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL,
        verbose_name=_('Created by'), null=True, blank=False)

    def __str__(self):
        return '{}'.format(self.name)


class Task(TimeStampedModel):
    title = models.CharField(_('Title'), max_length=255)
    description = models.TextField(_('Description'), null=True, blank=True)

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')

    priority = models.CharField(_('Task priority'), max_length=40,
        choices=PRIORITIES, default=MEDIUM)

    created_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL,
        verbose_name=_('Created by'), null=True, blank=False, related_name='owner')

    assigned_to = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL,
        verbose_name=_('Assigned to'), null=True, blank=True, related_name='assigned')

    task_type = models.CharField(_('Task type'), max_length=50,
        choices=TASK_TYPES, default=SUBTASK)

    story = models.ForeignKey("self", blank=True, null=True,
        related_name="connected_tasks", on_delete=models.CASCADE)
    """Describes if task is assigned to story or not."""

    @property
    def time_logged(self):
        return sum(self.time_logs.all().values_list('time_logged', flat=True))

    def __str__(self):
        return '{}'.format(self.title)


class TimeLog(TimeStampedModel):
    task = models.ForeignKey(Task, null=True, blank=True, on_delete=models.SET_NULL,
        related_name="time_logs")
    """Task is null because we don't want to remove log objects when task is removed."""

    user = models.ForeignKey(get_user_model(), null=False, blank=False, on_delete=models.CASCADE,
        related_name="time_logs")

    time_logged = models.PositiveIntegerField(null=False, blank=False)
    """
    Time logged for task in minutes. User can create more than one
    `TimeLog` objects for single task.
    """

    date = models.DateField()


class Comment(TimeStampedModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    content = models.TextField()

