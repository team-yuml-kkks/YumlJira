from django.http import Http404
from django.shortcuts import render

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets
from rest_framework.generics import CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from .choices import KANBAN
from .filters import *
from .models import *
from .serializers import *


def base_view(request):
    return render(request, 'base.html')


class ProjectViewset(viewsets.ModelViewSet):
    model = Project
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.all().order_by('id') \
        .prefetch_related('sprints', 'columns', 'columns__tasks') \
        .prefetch_related('columns__tasks__comments')
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProjectFilter

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProjectDetailSerializer
        else:
            return ProjectSerializer

    def perform_create(self, serializer):
        sprint_name = serializer.validated_data.pop('sprint_name', None)
        project = serializer.save(created_by=self.request.user)

        if project.board_type == KANBAN:
            project.create_kanban_board()
        else:
            project.create_scrum_board(sprint_name)


class TaskViewset(viewsets.ModelViewSet):
    model = Task
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all().order_by('id') \
        .select_related('column', 'story') \
        .prefetch_related('time_logs')
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TimeLogViewset(viewsets.ModelViewSet):
    model = TimeLog
    serializer_class = TimeLogSerializer
    permission_classes = [IsAuthenticated]
    queryset = TimeLog.objects.all().order_by('id').select_related('task', 'user')
    filter_backends = [DjangoFilterBackend]
    filterset_class = TimeLogFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_object(self):
        obj = super().get_object()

        if not obj.user == self.request.user:
            raise Http404

        return obj


class CommentViewset(viewsets.ModelViewSet):
    model = Comment
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all().order_by('-created').select_related('task', 'owner')
    filter_backends = [DjangoFilterBackend]
    fiterset_class = CommentFilter

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_object(self):
        obj = super().get_object()

        if not obj.owner == self.request.user:
            raise Http404

        return obj


class ColumnCreateUpdate(viewsets.ViewSet, CreateAPIView, DestroyAPIView, UpdateAPIView):
    serializer_class = ColumnSerializer
    permission_classes = [IsAuthenticated]
    queryset = Column.objects.all().order_by('number_in_board').select_related('project')

    def perform_create(self, serializer):
        number = serializer.validated_data['number_in_board']
        project = serializer.validated_data['project']
        Column.update_board_numbers(number, self.action, project)

        super().perform_create(serializer)

    def perform_update(self, serializer):
        number = serializer.validated_data.get('number_in_board', None)

        if number:
            Column.update_board_numbers_exist(number, self.get_object())

        super().perform_update(serializer)

    def perform_destroy(self, instance):
        Column.update_board_numbers(instance.number_in_board, self.action, instance.project)

        super().perform_destroy(instance)

    def get_object(self):
        obj = super().get_object()

        if self.action == 'destroy' and not obj.removable:
            raise Http404

        return obj

