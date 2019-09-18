from rest_framework.serializers import ModelSerializer

from .models import *


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ('title', 'description', 'project', 'priority',
            'created_by', 'assigned_to')


class ProjectSerializer(ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ('name', 'created_by', 'tasks')

