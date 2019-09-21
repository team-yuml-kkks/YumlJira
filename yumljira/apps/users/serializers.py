from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

class CustomRegistrationSerializer(RegisterSerializer):
    avatar = serializers.ImageField(max_length=255, required=False, allow_null=True)

    def save(self, request):
        user = super().save(request)
        user.avatar = request.data.get('avatar', None)
        user.save()

        return user

