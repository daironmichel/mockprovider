from authlib.common.encoding import json_loads
from authlib.integrations.django_helpers import parse_request_headers
from authlib.integrations.django_oauth1 import (CacheAuthorizationServer,
                                                ResourceProtector)
from authlib.oauth1 import OAuth1Request

from .models import Client, Token


def create_oauth_request(request, request_cls, use_json=False):
    if isinstance(request, request_cls):
        return request

    if request.method == 'POST':
        if use_json:
            body = json_loads(request.body)
        else:
            body = request.POST.dict()
    else:
        body = None

    headers = parse_request_headers(request)
    url = request.get_raw_uri()
    if '?key=' in url or '&key=' in url:
        url = url.replace('key=', 'oauth_consumer_key=')
    if '?token=' in url or '&token=' in url:
        url = url.replace('token=', 'oauth_token=')

    return request_cls(request.method, url, body, headers)


class MockEtradeAuthorizationServer(CacheAuthorizationServer):
    def create_oauth1_request(self, request):
        return create_oauth_request(request, OAuth1Request)


server = MockEtradeAuthorizationServer(Client, Token)
require_oauth = ResourceProtector(Client, Token)
