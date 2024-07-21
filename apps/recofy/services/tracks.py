import logging
from datetime import datetime, timezone

from apps.recofy.models.tracks import Track
from apps.recofy.services import albums as albums_services
from apps.recofy.services.spotify import SpotifyClientService

logger = logging.getLogger(__name__)


class TrackService(SpotifyClientService):
    def __init__(self, track_id: str, market: str) -> None:
        self.url: str = (
            f"https://api.spotify.com/v1/tracks/{track_id}"  # TODO: Move to constants
        )
        self.track_id = track_id
        self.market = market

    def _prefetch_validation(self) -> bool:
        is_new_record = False
        is_outdated = False
        try:
            track = Track.objects.get(spotify_id=self.track_id)

            # If more than 24H has passed since last updated_at
            is_outdated = bool((datetime.now(timezone.utc) - track.updated_at).days)
        except Track.DoesNotExist:
            is_new_record = True

        return any([is_new_record, is_outdated])

    def _prefetch_url(self) -> str:
        if self.market:
            return f"{self.url}?market={self.market}"
        return self.url

    def _prefetch_operation(self, data: dict) -> None:
        album = data.pop("album")
        album_service = albums_services.AlbumService(
            album_id=album["id"], market=self.market
        )
        album_service.update()

    def retrieve(self):
        return Track.objects.get(spotify_id=self.track_id)


def track_model_partial_create(
    spotify_id: str,
    spotify_uri: str,
):
    track_service = TrackService(
        track_id=spotify_id, market="CO"
    )  # TODO: Pass Market dynamically
    data = track_service.get_json_response()
    data.pop("artists")
    data.pop("album")
    data.pop("id")
    data.pop("uri")
    data["available_markets"] = [
        "CO",
    ]  # TODO: Pass Market dynamically

    track, _ = Track.objects.get_or_create(
        spotify_id=spotify_id, spotify_uri=spotify_uri, defaults={**data}
    )

    track.full_clean()
    return track
