from rest_framework_jwt.settings import api_settings

from yumljira.apps.users.test_factories import UserFactory


def create_token_for_user(user):
    """Creates token for user to authenticate."""
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    return jwt_encode_handler(jwt_payload_handler(user))


def user_strategy():
    """Creates user with JWT token."""
    user = UserFactory()

    return (user, create_token_for_user(user))

