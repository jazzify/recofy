import logging
from datetime import datetime, timezone

from apps.recofy.models.artists import Artist, ArtistImage
from apps.recofy.models.common import Genre
from apps.recofy.services.spotify import SpotifyClientService

logger = logging.getLogger(__name__)


class ArtistService(SpotifyClientService):
    def __init__(self, artist_id: str):
        self._artist_id = artist_id
        self.url: str = "https://api.spotify.com/v1/artists/"  # TODO: Think a better way to handle this.

    def _prefetch_validation(self) -> bool:
        is_new_record = False
        is_outdated = False
        try:
            artist = Artist.objects.get(spotify_id=self._artist_id)

            # If more than 24H has passed since last updated_at
            is_outdated = bool((datetime.now(timezone.utc) - artist.updated_at).days)
        except Artist.DoesNotExist:
            is_new_record = True

        return any([is_new_record, is_outdated])

    def _prefetch_url(self) -> str:
        return f"{self.url}{self._artist_id}"

    def _prefetch_operation(self, data: dict) -> None:
        artist_update_or_create(data=data)

    def retrieve(self) -> Artist:
        return Artist.objects.get(spotify_id=self._artist_id)


def get_genres_by_name(genres: list[str]) -> list[Genre]:
    current_genres = list(Genre.objects.filter(name__in=genres))
    current_names = [g.name for g in current_genres]

    new_genres = [Genre(name=genre) for genre in genres if genre not in current_names]

    created_genres = Genre.objects.bulk_create(new_genres)
    return created_genres + current_genres


def artist_update_or_create(data: dict) -> None:
    spotify_id = data.pop("id")
    spotify_uri = data.pop("uri")
    images = data.pop("images")
    genres = data.pop("genres")

    artist, _ = Artist.objects.update_or_create(
        spotify_id=spotify_id,
        spotify_uri=spotify_uri,
        defaults={**data},
    )
    artist_genres = get_genres_by_name(genres=genres)
    artist.genres.set(artist_genres)

    image_urls = [image["url"] for image in images]
    current_images = list(ArtistImage.objects.filter(url__in=image_urls))
    current_urls = [image.url for image in current_images]

    new_images = []
    for artist_image in images:
        if artist_image["url"] not in current_urls:
            artist_image = ArtistImage(
                height_px=artist_image["height"],
                width_px=artist_image["width"],
                url=artist_image["url"],
                artist=artist,
            )
            artist_image.full_clean()
            new_images.append(artist_image)

    all_artist_images = current_images + new_images

    artist.artistimage_set.set(all_artist_images, bulk=False)
    artist.full_clean()
    artist.save()


def artist_retrieve(artist_spotify_id: str) -> Artist:
    artist_service = ArtistService(artist_id=artist_spotify_id)
    artist_service.update()
    artist_model = artist_service.retrieve()
    return artist_model
