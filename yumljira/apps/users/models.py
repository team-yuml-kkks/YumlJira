from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.templatetags.static import static

from yumljira.apps.common.utils import get_static_url


class User(AbstractUser):
    avatar = models.ImageField(upload_to="avatars/", max_length=255, null=True, blank=True)

    @property
    def get_avatar(self):
        if self.avatar:
            return self.avatar.url
        else:
            url = settings.DEFAULT_AVATAR.split('.')

            return get_static_url(url[0], url[1]) or static(url[0])

