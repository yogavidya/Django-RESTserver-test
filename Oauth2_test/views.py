import json
import requests
from django.http import HttpRequest, HttpResponse
from django.conf import settings
from django.shortcuts import redirect


def oauth2_get_token(request: HttpRequest):
    code = request.GET['code']
    token_endpoint_response = requests.post(
        settings.URL_SCHEME + 'localhost:8000/o/token/',
        verify=False if settings.DEBUG else True,
        data={
            'client_id': 'vtGlrl5jKEBS0i67wnSNsdx3w8ScQqsWSzkp2JzR',
            'client_secret': 'xIo6NHb0Cw44WLjYcfIg9I92OSHikaj5wTBienExzq9BBqZDXDEGMQ2YGMfdjI4Dq14M0SRl2Z2uLKPZsGPzFEwTgp1MZaf3oEdmz3Gd4M6Ixssr2RpKZUn8zp3VRMgO',
            'grant_type': 'authorization_code',
            'code': code,
            'approval_prompt': 'auto',
        })
    content = json.loads(token_endpoint_response.content)
    client_url = settings.CLIENT_APPLICATION_URL + (
        '?access_token={}' '&refresh_token={}')
    client_url = \
        client_url.format(content['access_token'], content['refresh_token'])
    if settings.DEBUG:
        return HttpResponse('access_token: {}'.format(content['access_token']))
    else:
        return redirect(client_url)


