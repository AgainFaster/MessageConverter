from rest_framework import authentication
from rest_framework import exceptions
from message_converter.models import ApiToken


class WombatAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        client_id = request.META.get('HTTP_X_HUB_STORE')
        key = request.META.get('HTTP_X_HUB_TOKEN')

        if not client_id or not key:
            return None

        try:
            token = ApiToken.objects.get(client_id=client_id, key=key)
        except ApiToken.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such token.')

        return (token.user, None)