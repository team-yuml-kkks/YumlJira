from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register(r'projects', views.ProjectViewset, basename='projects')
router.register(r'tasks', views.TaskViewset, basename='tasks')
router.register(r'timelogs', views.TimeLogViewset, basename='timelogs')

urlpatterns = [
    path('', views.base_view, name='base_view'),
] + router.urls

