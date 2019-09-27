from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register(r'projects', views.ProjectViewset, basename='projects')
router.register(r'tasks', views.TaskViewset, basename='tasks')
router.register(r'timelogs', views.TimeLogViewset, basename='timelogs')
router.register(r'comments', views.CommentViewset, basename='comments')

urlpatterns = [
    path('', views.base_view, name='base_view'),
    path('register', views.base_view, name='base_view'),
    path('login', views.base_view, name='base_view'),
    path('project-list', views.base_view, name='base_view'),
] + router.urls

