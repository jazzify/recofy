from django.conf import settings

REDIS_SPOTIFY_ACCESS_TOKEN = "REDIS_SPOTIFY_ACCESS_TOKEN"  # nosec: B105

SPOTIFY_AUTH_DATA = {
    "url": "https://accounts.spotify.com/api/token",
    "headers": {"Content-Type": "application/x-www-form-urlencoded"},
    "payload": {
        "grant_type": "client_credentials",
        "client_id": settings.SPOTIFY_CLIENT_ID,
        "client_secret": settings.SPOTIFY_CLIENT_SECRET,
    },
}

SPOTIFY_REQUEST_TIMEOUT = 3.0
