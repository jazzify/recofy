from django.db import models

from apps.core.models import BaseModel

ARTIST_TYPE = "artist"
ARTIST_TYPE_CHOICES = ((ARTIST_TYPE, ARTIST_TYPE),)


class Artist(BaseModel):
    external_urls = models.JSONField()
    followers = models.JSONField()
    genres = models.ManyToManyField("recofy.Genre")
    href = models.URLField()
    spotify_id = models.CharField(max_length=22, unique=True)
    name = models.CharField(max_length=255)
    popularity = models.PositiveSmallIntegerField()
    type = models.CharField(choices=ARTIST_TYPE_CHOICES, max_length=6)
    spotify_uri = models.CharField(max_length=37, unique=True)

    def __repr__(self):
        return f"Artist <{self.id}> {self.spotify_id=} - {self.name=}"

    def __str__(self):
        return self.name


class ArtistImage(BaseModel):
    height_px = models.PositiveSmallIntegerField()
    width_px = models.PositiveSmallIntegerField()
    url = models.URLField(unique=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

    def __repr__(self):
        return f"ArtistImage <{self.id}>"

    def __str__(self):
        return self.url
