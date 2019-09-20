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
        fields = ('title', 'description', 'project', 'priority',
            'created_by', 'assigned_to', 'task_type', 'story')

    def validate(self, data):
        story = data.get('story', None)
        task_type = data.get('task_type', None)

        if story and task_type:
            if task_type == STORY and story.task_type == STORY:
                raise ValidationError({'story':([_('Story cannot contain another story.')])})

            if not story.task_type == STORY:
                raise ValidationError({'task_type':([_('Only story may contain subtasks.')])})

        return data


class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ('name', 'created_by', 'tasks')

