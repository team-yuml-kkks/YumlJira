from allauth.account.utils import complete_signup
from allauth.socialaccount.models import SocialAccount

from django.contrib.auth import get_user_model

from rest_auth.serializers import JWTSerializer
from rest_auth.utils import jwt_encode
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from .serializers import GoogleLoginSerializer, UserSerializer


class GoogleLoginView(CreateAPIView):
    """
    Google login/register authentication with backend server

    First client sends token obtained after user successfully logged with Google
    account. Then this token is put under verification (Token is send to Google endpoint.
    If it's valid then response with 200 status code is returned and response field `iss`
    contains one of those: `['accounts.google.com', 'https://accounts.google.com']`). If token is not valid
    ValidationError is raised with corresponding message. When verification is successful
    we have to check if email inside response does not exist with our database. If not new
    user is created. In both cases we update or create new object of `SocialAccount`.
    """
    serializer_class = GoogleLoginSerializer
    permission_classes = []
    token = None

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.perform_create(serializer)

        return self.get_response_data(user)

    def perform_create(self, serializer):
        user, created = self.create_user(serializer.data['token'])

        if created:
            complete_signup(self.request._request, user, False, None)

        return user

    def create_user(self, idinfo):
        email = idinfo.get('email', None)

        user_data = {
            'email': email,
            'username': email,
            'first_name': idinfo.get('given_name', None),
            'last_name': idinfo.get('family_name', None),
        }

        user = get_user_model().objects.filter(email=email).first()

        if not user:
            user_serializer = UserSerializer(data=user_data)
            user_serializer.is_valid(raise_exception=True)
            user = user_serializer.save()

        self.token = jwt_encode(user)

        _, created = SocialAccount.objects.update_or_create(
            user=user,
            provider='google',
            uid=idinfo['sub'],
            extra_data=user_data
        )

        return (user, created)

    def get_response_data(self, user):
        data = {
            'user': user,
            'token': self.token,
        }

        return Response(
            JWTSerializer(data).data,
            status=status.HTTP_201_CREATED,
        )

