from django.conf import settings

REDIS_SPOTIFY_ACCESS_TOKEN = "REDIS_SPOTIFY_ACCESS_TOKEN"  # nosec: B105


class SPOTIFY_URLS:
    auth = "https://accounts.spotify.com/api/token"

    class API:
        _base = "https://api.spotify.com/v1/"
        albums = f"{_base}albums/"
        artists = f"{_base}artists/"
        tracks = f"{_base}tracks/"


SPOTIFY_AUTH_DATA = {
    "url": SPOTIFY_URLS.auth,
    "headers": {"Content-Type": "application/x-www-form-urlencoded"},
    "payload": {
        "grant_type": "client_credentials",
        "client_id": settings.SPOTIFY_CLIENT_ID,
        "client_secret": settings.SPOTIFY_CLIENT_SECRET,
    },
}

SPOTIFY_REQUEST_TIMEOUT = 3.0
