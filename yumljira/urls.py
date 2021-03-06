"""yumljira URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.renderers import JSONOpenAPIRenderer
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('allauth.urls')),
    path('', include('yumljira.apps.projects.urls')),
    path('', include('yumljira.apps.users.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),

    path('openapi', get_schema_view(
        title="YumlJira API",
        description="YumlJira API",
        version="0.0.1",
        renderer_classes=[JSONOpenAPIRenderer]
    ), name='openapi-schema'),

    path('docs/', TemplateView.as_view(
        template_name='redocs.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

