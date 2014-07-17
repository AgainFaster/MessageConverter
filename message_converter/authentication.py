from rest_framework import authentication
from rest_framework import exceptions
from message_converter.models import ApiToken

import logging

logger = logging.getLogger(__name__)

class WombatAuthentication(authentication.BaseAuthentication):

    def _log_headers(self, request):

        headers = 'DUMPING HEADERS:\n'

        for key in request.META:
            headers += '\t%s: %s\n' % (key, request.META[key])

        logger.info(headers)

    def authenticate(self, request):
        client_id = request.META.get('HTTP_X_HUB_STORE')
        key = request.META.get('HTTP_X_HUB_TOKEN')

        if not client_id or not key:
            logger.info('Authentication credentials were not provided.')
            self._log_headers(request)
            return None

        try:
            token = ApiToken.objects.get(client_id=client_id, key=key)
        except ApiToken.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such token.')

        return (token.user, None)