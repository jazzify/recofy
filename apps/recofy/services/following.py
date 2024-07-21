from apps.recofy.models.artists import Artist
from apps.recofy.services.spotify import SpotifyClientService


class FollowingService(SpotifyClientService):
    def __init__(self, last_artist: str | None):
        self.last_artist: str | None = last_artist
        self.url: str = "https://api.spotify.com/v1/me/following?type=artist&limit=50"

    def _prefetch_validation(self):
        return True

    def _prefetch_url(self):
        if self.last_artist:
            return f"{self.url}&after={self.last_artist}"
        return self.url

    def _prefetch_operation(self, data):
        return data

    def list(self) -> list[Artist]:
        return Artist.objects.prefetch_related("artistimage_set", "genres").all()
