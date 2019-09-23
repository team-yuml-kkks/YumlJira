from django.http import Http404
from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from .models import *
from .serializers import *


def base_view(request):
    return render(request, 'base.html')


class ProjectViewset(viewsets.ModelViewSet):
    model = Project
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.all().order_by('id').prefetch_related('tasks')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TaskViewset(viewsets.ModelViewSet):
    model = Task
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all().order_by('id') \
        .select_related('project') \
        .prefetch_related('time_logs')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TimeLogViewset(viewsets.ModelViewSet):
    model = TimeLog
    serializer_class = TimeLogSerializer
    permission_classes = [IsAuthenticated]
    queryset = TimeLog.objects.all().order_by('id').select_related('task', 'user')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_object(self):
        obj = super().get_object()

        if not obj.user == self.request.user:
            raise Http404

        return obj

