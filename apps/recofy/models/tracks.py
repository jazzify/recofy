from django.contrib.postgres.fields import ArrayField
from django.db import models

from apps.core.models import BaseModel

STANDARD_TYPE = "track"
TYPE_CHOICES = ((STANDARD_TYPE, STANDARD_TYPE),)


class Track(BaseModel):
    preview_url = models.URLField(null=True, blank=True)
    is_playable = models.BooleanField()
    explicit = models.BooleanField()
    type = models.CharField(choices=TYPE_CHOICES, max_length=5)
    spotify_id = models.CharField(max_length=22, unique=True)
    href = models.URLField()
    artists = models.ManyToManyField(to="recofy.Artist", through="TracksArtists")
    disc_number = models.PositiveSmallIntegerField()
    track_number = models.PositiveSmallIntegerField()
    duration_ms = models.PositiveIntegerField()
    external_ids = models.JSONField()
    external_urls = models.JSONField()
    name = models.CharField(max_length=255)
    popularity = models.PositiveSmallIntegerField()
    spotify_uri = models.CharField(max_length=37, unique=True)
    is_local = models.BooleanField()
    available_markets = ArrayField(models.CharField(max_length=2))

    def __repr__(self):
        return f"Track <{self.id}>  {self.spotify_id=} - {self.name=}"

    def __str__(self):
        return self.name


class TracksArtists(models.Model):
    artist = models.ForeignKey(
        "recofy.Artist", to_field="spotify_id", on_delete=models.CASCADE
    )
    track = models.ForeignKey(Track, to_field="spotify_id", on_delete=models.CASCADE)
