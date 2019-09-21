from allauth.socialaccount.models import SocialApp

from django.contrib.auth import get_user_model
from django.conf import settings

from google.oauth2 import id_token
from google.auth.transport import requests

from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class CustomRegistrationSerializer(RegisterSerializer):
    avatar = serializers.ImageField(max_length=255, required=False, allow_null=True)

    def save(self, request):
        user = super().save(request)
        user.avatar = request.data.get('avatar', None)
        user.save()

        return user


class GoogleLoginSerializer(serializers.Serializer):
    token = serializers.CharField(write_only=True, required=True, allow_null=False)

    def validate_token(self, token):
        app = SocialApp.objects.filter(provider='google').first()

        if not app:
            raise ValidationError({'token': ['App not configured. Please configure social app first.']})

        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), settings.app.client_id)

            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValidationError({'token': ['Wrong issuer.']})

            userid = idinfo['sub']

            return idinfo
        except ValueError:
            raise ValidationError({'token': ['Invalid token.']})


class UserSerializer(UserDetailsSerializer):
    class Meta:
        model = get_user_model()
        fields = ('pk', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = []
