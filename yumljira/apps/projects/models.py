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

    def __str__(self):
        return '{}'.format(self.title)

