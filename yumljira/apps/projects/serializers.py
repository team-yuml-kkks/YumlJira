from decimal import Decimal, InvalidOperation

from django.utils.translation import gettext as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .choices import *
from .models import *


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('pk', 'content', 'owner', 'task', 'created', 'modified')


class TaskSerializer(serializers.ModelSerializer):
    story = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all(),
        required=False, allow_null=True)

    comments = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = Task
        fields = ('pk', 'title', 'description', 'priority',
            'created_by', 'assigned_to', 'task_type', 'story', 'time_logged',
            'comments', 'created', 'modified', 'column')
        extra_kwargs = {
            'created': {'read_only': True},
            'modified': {'read_only': True},
        }

    def validate(self, data):
        story = data.get('story', None)
        task_type = data.get('task_type', None)

        if story and task_type:
            if task_type == STORY and story.task_type == STORY:
                raise ValidationError({'story': [_('Story cannot contain another story.')]})

            if not story.task_type == STORY:
                raise ValidationError({'task_type': [_('Only story may contain subtasks.')]})

        return data


class ColumnSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Column
        fields = ('pk', 'title', 'number_in_board', 'should_show', 'project', 'tasks')
        extra_kwargs = {
            'project': {'write_only': True}
        }


class SprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sprint
        fields = ('pk', 'name', 'is_closed', 'created')


class ProjectSerializer(serializers.ModelSerializer):
    sprint_name = serializers.CharField(max_length=200, write_only=True,
        allow_null=True, required=False)

    class Meta:
        model = Project
        fields = ('pk', 'name', 'created_by', 'key', 'board_type', 'sprint_name')

    def validate(self, data):
        sprint_name = data.get('sprint_name', None)
        board_type = data.get('board_type', None)

        if board_type == KANBAN and sprint_name:
            raise ValidationError({'sprint_name': [_('Kanban board do not contain sprints')]})

        if board_type == SCRUM and not sprint_name:
            raise ValidationError({'sprint_name': [_('Sprint name is required for scrum board.')]})

        return data


class ProjectDetailSerializer(ProjectSerializer):
    sprints = SprintSerializer(many=True, read_only=True)
    columns = ColumnSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ('pk', 'name', 'created_by', 'key', 'board_type',
            'sprint_name', 'sprints', 'columns')


class TimeLogSerializer(serializers.ModelSerializer):
    time_logged = serializers.CharField(required=True, allow_null=False)

    class Meta:
        model = TimeLog
        fields = ('pk', 'user', 'task', 'date', 'time_logged')

    def validate_task(self, task):
        if not task:
            raise ValidationError({'task': [_('You have to assign issue first.')]})

        return task

    def validate_time_logged(self, time_logged):
        """
        Validation of `time_logged` properties may depends on value which is send to the API.
        There are 2 possibilities:
            * as minutes e.g. '20'
            * as periods e.g. '2h 30m'

        For the first option we check if user has send more then 0 minutes to the API if not
        error is raised.

        The second option is a little harder. We are doing the following to validated data:
            1. First we divide string into dict with periods as keys and their time as values.
                In addition in this step we check if values we put inside the dict are convertable
                to float. If any value is not valid error is raised. If value is negative then we change it to 0.

            2. Next we check the keys. Keys are valid when:
                * do not repeat
                * correct character is used

            To make sure those two conditions have been fulfilled first we make set
            of periods and check if keys inside the dict are the same as new set.
            If this is not correct then error is raised. Second condition is checked
            with help of `issubset` method with `AVAILABLE_TIME_OPTIONS` argument used
            for periods set.

            The last check is used to make sure first value is not 0.

            If all of those conditions are correct then we calculate sum of minutes
            by specific period and returns the value.
        """
        try:
            time_logged = int(time_logged)

            if time_logged <= 0:
                raise ValidationError({'time_logged': [_('You have to log more than 0 minutes')]})

            return time_logged
        except ValueError:
            try:
                time_dict = dict([(option[-1], self._get_value(option[:-1])) for option in time_logged.split(' ')])
            except InvalidOperation:
                raise ValidationError({'time_logged': [_('Wrong values')]})

            time_values = list(time_dict.values())
            time_options = time_dict.keys()
            options = set(time_options)

            # Check if options do not repeat e.g. ['d', 'd'].
            if len(options) != len(time_options):
                raise ValidationError({'time_logged': [_('You cannot repeat periods')]})

            # Check if options are correct e.g. ['d', 'x'].
            if not options.issubset(AVAILABLE_TIME_OPTIONS):
                raise ValidationError({'time_logged': [_('You can only use those characters to describe periods: m, h, d, w')]})

            # First value cannot be less or equal 0.
            if time_values[0] == 0:
                raise ValidationError({'time_logged': [_('You can only use those characters to describe periods: m, h, d, w')]})

            time_logged = sum(OPTION_TO_MINUTE[option] * time for option, time in time_dict.items())

        return time_logged

    def _get_value(self, value):
        return max(Decimal(value), 0)

