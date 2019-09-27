from django_filters import rest_framework as filters

from .models import Comment, TimeLog


class TimeLogFilter(filters.FilterSet):
    date_before = filters.DateFilter(field_name='date', lookup_expr='lte')
    date_after = filters.DateFilter(field_name='date', lookup_expr='gte')

    class Meta:
        model = TimeLog
        fields = ['task', 'user', 'task__project', 'date_after', 'date_before']


class CommentFilter(filters.FilterSet):
    date_before = filters.DateFilter(field_name='date', lookup_expr='lte')
    date_after = filters.DateFilter(field_name='date', lookup_expr='gte')

    class Meta:
        model = Comment
        fields = ['task', 'owner', 'date_after', 'date_before']

