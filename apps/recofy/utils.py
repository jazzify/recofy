import requests
from django.core.cache import cache
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed

from apps.recofy.constants import REDIS_SPOTIFY_ACCESS_TOKEN, SPOTIFY_AUTH_DATA


def spotify_auth(func):
    def _spotify_authenticate():
        response = requests.post(
            url=SPOTIFY_AUTH_DATA["url"],
            headers=SPOTIFY_AUTH_DATA["headers"],
            data=SPOTIFY_AUTH_DATA["payload"],
            timeout=3.0,
        )

        if response.status_code != status.HTTP_200_OK:
            raise AuthenticationFailed("Spotify Authentication Wrapper")

        body = response.json()
        cache.set(
            key=REDIS_SPOTIFY_ACCESS_TOKEN,
            value=body["access_token"],
            timeout=body["expires_in"],
        )

    def wrapper(*args, **kwargs):
        current_token = cache.get(key=REDIS_SPOTIFY_ACCESS_TOKEN)
        if not current_token:
            _spotify_authenticate()
        return func(*args, **kwargs)

    return wrapper
