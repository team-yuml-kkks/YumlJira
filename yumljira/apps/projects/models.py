from django.contrib.auth import get_user_model
from django.db import models, transaction
from django.utils.translation import gettext as _

from model_utils.models import TimeStampedModel

from .choices import *


"""
Board description:
    User can create only one board per project. There are two types of board
    which user can use: Kanbad and Scrum. To represent board we use `Column` model.
    Each `Column` object has `number_in_board` field which represents the order
    of columns inside board. Those numbers have to be unique within single board.

    There is also a `Sprint` model used with Scrum board to
    keep informations about sprints in the project.

    When project is created via API 4 basic columns (and sprint (Scrum only))
    are saved to database. Those are:
        * BACKLOG
        * TO DO (Scrum) / SELECTED FOR DEVELOPMENT (Kanban)
        * IN PROGRESS
        * DONE

    `Task` has IntegerField `column` which is used to save last column task was moved to.
"""


class Project(TimeStampedModel):
    name = models.CharField(_('Project name'), max_length=255)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL,
        verbose_name=_('Created by'), null=True, blank=False)
    key = models.CharField(_('Project key'), max_length=30)

    board_type = models.CharField(max_length=50, choices=BOARD_TYPE_CHOICES, default=KANBAN)

    def __str__(self):
        return '{}'.format(self.name)

    def create_kanban_board(self):
        self._create_columns(SELECTED_FOR_DEV)

    def create_scrum_board(self, sprint_name):
        self._create_columns(TO_DO)

        Sprint.objects.create(
            project=self,
            name=sprint_name
        )

    def _create_columns(self, second_column_title):
        """Creates columns for new project.

        Args:
            second_column_title (str): Title for second column.
        """
        Column.objects.create(
            title=BACKLOG,
            project=self,
            number_in_board=1,
            should_show=False,
            removable=False,
        )

        Column.objects.create(
            title=second_column_title,
            project=self,
            number_in_board=2,
            removable=False,
        )

        Column.objects.create(
            title=IN_PROGRESS,
            project=self,
            number_in_board=3,
            removable=False,
        )

        Column.objects.create(
            title=DONE,
            project=self,
            number_in_board=4,
            removable=False,
        )


class Sprint(TimeStampedModel):
    project = models.ForeignKey(Project, models.CASCADE, related_name='sprints')
    name = models.CharField(max_length=200)
    is_closed = models.BooleanField(default=False)
    """Describes if sprint was closed by user."""


class Column(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='columns')
    title = models.CharField(max_length=100)
    number_in_board = models.PositiveSmallIntegerField()
    """This field specify the order of columns inside board."""

    should_show = models.BooleanField(default=True)
    """Determinates if column should be display in board."""

    removable = models.BooleanField(default=True)
    """Describes if column may be removed."""

    @classmethod
    @transaction.atomic
    def update_board_numbers(cls, number, action, project):
        """
        Increase or decrease `number_in_board` field.
        Used when column is created or deleted.

        Args:
            number(int) - requested `number_in_board`.
        """
        if action == 'create':
            cls.objects.filter(number_in_board__gte=number, project=project) \
                .update(number_in_board=models.F('number_in_board') + 1)

        elif action == 'destroy':
            cls.objects.filter(number_in_board__gte=number, project=project) \
                .update(number_in_board=models.F('number_in_board') - 1)

    @classmethod
    @transaction.atomic
    def update_board_numbers_exist(cls, number, old_instance):
        old_number = old_instance.number_in_board
        project = old_instance.project

        columns = project.columns.all().order_by('number_in_board') \
            .values_list('number_in_board', flat=True)

        last_number = columns.last()

        if number == old_number:
            return

        if number > last_number:
            return

        if number > old_number:
            cls.objects.filter(
                models.Q(number_in_board__gt=old_number)
                | models.Q(number_in_board__lte=number)
            ).update(number_in_board=models.F('number_in_board') - 1)

        else:
            cls.objects.filter(
                models.Q(number_in_board__lt=old_number)
                | models.Q(number_in_board__gte=number)
            ).update(number_in_board=models.F('number_in_board') + 1)


class Task(TimeStampedModel):
    title = models.CharField(_('Title'), max_length=255)
    description = models.TextField(_('Description'), null=True, blank=True)

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

    column = models.ForeignKey(Column, on_delete=models.PROTECT, related_name='tasks')

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

