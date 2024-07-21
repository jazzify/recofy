from django.contrib.postgres.fields import ArrayField
from django.db import models

from apps.core.models import BaseModel
from apps.recofy.models.artists import Artist
from apps.recofy.models.tracks import Track

TYPE_STANDARD = "album"
TYPE_CHOICES = ((TYPE_STANDARD, TYPE_STANDARD),)

ALBUM_TYPE_ALBUM = "album"
ALBUM_TYPE_SINGLE = "single"
ALBUM_TYPE_COMPILATION = "compilation"
ALBUM_TYPE_CHOICES = (
    (ALBUM_TYPE_ALBUM, ALBUM_TYPE_ALBUM),
    (ALBUM_TYPE_SINGLE, ALBUM_TYPE_SINGLE),
    (ALBUM_TYPE_COMPILATION, ALBUM_TYPE_COMPILATION),
)

RELEASE_DATE_PRECISION_DAY = "day"
RELEASE_DATE_PRECISION_MONTH = "month"
RELEASE_DATE_PRECISION_YEAR = "year"

RELEASE_DATE_PRECISION_CHOICES = (
    (RELEASE_DATE_PRECISION_DAY, RELEASE_DATE_PRECISION_DAY),
    (RELEASE_DATE_PRECISION_MONTH, RELEASE_DATE_PRECISION_MONTH),
    (RELEASE_DATE_PRECISION_YEAR, RELEASE_DATE_PRECISION_YEAR),
)


class Album(BaseModel):
    type = models.CharField(choices=TYPE_CHOICES, max_length=5)
    album_type = models.CharField(choices=ALBUM_TYPE_CHOICES, max_length=11)
    href = models.URLField()
    spotify_id = models.CharField(max_length=22, unique=True)
    name = models.CharField(max_length=255, blank=True)
    release_date = models.CharField(max_length=10)
    release_date_precision = models.CharField(
        choices=RELEASE_DATE_PRECISION_CHOICES, max_length=5
    )
    spotify_uri = models.CharField(max_length=37, unique=True)
    artists = models.ManyToManyField(to=Artist, through="AlbumsArtists")
    tracks = models.ManyToManyField(to=Track, through="AlbumsTracks")
    external_urls = models.JSONField()
    external_ids = models.JSONField()
    total_tracks = models.PositiveSmallIntegerField()
    genres = ArrayField(models.CharField(max_length=255, blank=True), blank=True)
    label = models.CharField(max_length=255)
    available_markets = ArrayField(models.CharField(max_length=2))
    copyrights = ArrayField(models.JSONField())
    popularity = models.SmallIntegerField()

    def __repr__(self):
        return f"Album <{self.id}> {self.spotify_id=} - {self.name=}"

    def __str__(self):
        return self.name


class AlbumsArtists(models.Model):
    artist = models.ForeignKey(Artist, to_field="spotify_id", on_delete=models.CASCADE)
    album = models.ForeignKey(Album, to_field="spotify_id", on_delete=models.CASCADE)


class AlbumsTracks(models.Model):
    track = models.ForeignKey(Track, to_field="spotify_id", on_delete=models.CASCADE)
    album = models.ForeignKey(Album, to_field="spotify_id", on_delete=models.CASCADE)


class AlbumImage(BaseModel):
    height_px = models.PositiveSmallIntegerField()
    width_px = models.PositiveSmallIntegerField()
    url = models.URLField(unique=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

    def __repr__(self):
        return f"AlbumImage <{self.id}>"

    def __str__(self):
        return self.url
