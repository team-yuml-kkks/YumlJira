from django.utils.translation import gettext as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .choices import *
from .models import *


class TaskSerializer(serializers.ModelSerializer):
    story = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all(),
        required=False, allow_null=True)

    class Meta:
        model = Task
        fields = ('pk', 'title', 'description', 'project', 'priority',
            'created_by', 'assigned_to', 'task_type', 'story', 'time_logged')

    def validate(self, data):
        story = data.get('story', None)
        task_type = data.get('task_type', None)

        if story and task_type:
            if task_type == STORY and story.task_type == STORY:
                raise ValidationError({'story': [_('Story cannot contain another story.')]})

            if not story.task_type == STORY:
                raise ValidationError({'task_type': [_('Only story may contain subtasks.')]})

        return data


class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ('pk', 'name', 'created_by', 'tasks')


class TimeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeLog
        fields = ('pk', 'user', 'task', 'date', 'time_logged')

    def validate_task(self, task):
        if not task:
            raise ValidationError({'task': [_('You have to assign issue first.')]})

        return task

    def validate_time_logged(self, time_logged):
        if time_logged <= 0:
            raise ValidationError({'time_logged': [_('You have to log more than 0 minutes')]})

        return time_logged

