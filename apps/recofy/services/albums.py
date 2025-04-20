from datetime import datetime, timezone

from apps.recofy.constants import SPOTIFY_URLS
from apps.recofy.models import Album, AlbumImage
from apps.recofy.services import artists as artist_services
from apps.recofy.services import tracks as tracks_services
from apps.recofy.services.spotify import SpotifyClientService


class AlbumService(SpotifyClientService):
    def __init__(self, album_id: str, market: str) -> None:
        self.album_id = album_id
        self.market = market

    def _prefetch_validation(self) -> bool:
        is_new_record = False
        is_outdated = False
        try:
            album = Album.objects.get(spotify_id=self.album_id)

            # If more than 24H has passed since last updated_at
            is_outdated = bool((datetime.now(timezone.utc) - album.updated_at).days)
        except Album.DoesNotExist:
            is_new_record = True

        return any([is_new_record, is_outdated])

    def _prefetch_url(self) -> str:
        return f"{SPOTIFY_URLS.API.albums}{self.album_id}?market={self.market}"

    def _prefetch_operation(self, data) -> None:
        album_update_or_create(data=data, market=self.market)

    def retrieve(self) -> Album:
        return Album.objects.get(spotify_id=self.album_id)


def album_update_or_create(data: dict, market: str) -> None:
    data.pop("artists")

    spotify_id = data.pop("id")
    spotify_uri = data.pop("uri")
    images = data.pop("images")
    tracks = data.pop("tracks")
    data["genres"] = data.pop("genres", [])

    album, _ = Album.objects.update_or_create(
        spotify_id=spotify_id,
        spotify_uri=spotify_uri,
        defaults={**data},
    )

    album_artists = []
    album_tracks = []
    for track in tracks["items"]:
        track_artists_models = []

        for track_artist in track.pop("artists"):
            artist = artist_services.artist_retrieve(
                artist_spotify_id=track_artist["id"]
            )
            track_artists_models.append(artist)

            # Build Artists to Album from Tracks
            if artist not in album_artists:
                album_artists.append(artist)

        track_model = tracks_services.track_model_partial_create(
            spotify_id=track.pop("id"),
            spotify_uri=track.pop("uri"),
            market=market,
        )

        # Set Artists to Track
        track_model.artists.set(track_artists_models)
        album_tracks.append(track_model)

    image_urls = [image["url"] for image in images]
    current_images = list(AlbumImage.objects.filter(url__in=image_urls).only("url"))
    current_urls = [image.url for image in current_images]

    new_images = []
    for album_image in images:
        if album_image["url"] not in current_urls:
            album_image = AlbumImage(
                height_px=album_image["height"],
                width_px=album_image["width"],
                url=album_image["url"],
                album=album,
            )
            album_image.full_clean()
            new_images.append(album_image)
    all_album_images = current_images + new_images

    # Set Artists to Album
    album.artists.set(album_artists)
    # Set Tracks to Album
    album.tracks.set(album_tracks)
    # Set AlbumImages to Album
    album.albumimage_set.set(all_album_images, bulk=False)
    album.full_clean()
    album.save()
