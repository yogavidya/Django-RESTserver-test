import json
import requests
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.conf import settings


def oauth2_get_token(request: HttpRequest):
    code = request.GET['code']
    token_endpoint_response = requests.post(settings.URL_SCHEME + 'localhost:8000/o/token/',
                                            verify=False if settings.DEBUG else True,
                                            data={
                                                'client_id': 'vtGlrl5jKEBS0i67wnSNsdx3w8ScQqsWSzkp2JzR',
                                                'client_secret': 'xIo6NHb0Cw44WLjYcfIg9I92OSHikaj5wTBienExzq9BBqZDXDEGMQ2YGMfdjI4Dq14M0SRl2Z2uLKPZsGPzFEwTgp1MZaf3oEdmz3Gd4M6Ixssr2RpKZUn8zp3VRMgO',
                                                'scope': 'read',
                                                'grant_type': 'authorization_code',
                                                'code': code,
                                            })
    content = json.loads(token_endpoint_response.content)
    request.session['token'] = content['access_token']
    request.session['refresh_token'] = content['refresh_token']
    request.session['time_expire'] = content['expires_in']
    request.session['scope'] = content['scope']
    # TODO : main entry point for a client application could be here
    return HttpResponse()


def test_valid_session(request: HttpRequest):
    """TODO: remove in production"""
    if 'token' in request.session:
        return HttpResponse(bytes('session authenticated: token = {}'.format(request.session['token']),'utf_8'))
    else:
        return HttpResponse(b'session invalid')
