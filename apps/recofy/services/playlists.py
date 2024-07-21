from apps.recofy.models.artists import Artist
from apps.recofy.services.spotify import SpotifyClientService


class PlaylistService(SpotifyClientService):
    def __init__(self, playlist_id: str, market: str):
        self.url: str = f"https://api.spotify.com/v1/playlists/{playlist_id}"
        self.playlist_id = playlist_id
        self.market = market

    def _prefetch_validation(self):
        return True

    def _prefetch_url(self):
        if self.market:
            return f"{self.url}?market={self.market}"
        return self.url

    def _prefetch_operation(self, data):
        return data

    def list(self) -> list[Artist]:
        return Artist.objects.prefetch_related("artistimage_set", "genres").all()
