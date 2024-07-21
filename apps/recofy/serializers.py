from rest_framework import serializers

from apps.recofy.models import Album, AlbumImage, Artist, ArtistImage, Genre, Track


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = [
            "name",
        ]


class ArtistImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistImage
        fields = ["height_px", "width_px", "url"]


class ArtistSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    images = ArtistImageSerializer(source="artistimage_set", many=True, read_only=True)

    class Meta:
        model = Artist
        fields = [
            "external_urls",
            "followers",
            "genres",
            "images",
            "href",
            "spotify_id",
            "name",
            "popularity",
            "type",
            "spotify_uri",
            "created_at",
            "updated_at",
            "is_active",
        ]


class AlbumImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlbumImage
        fields = ["height_px", "width_px", "url"]


class TrackSerializer(serializers.ModelSerializer):
    artists = ArtistSerializer(many=True, read_only=True)

    class Meta:
        model = Track
        fields = [
            "preview_url",
            "is_playable",
            "explicit",
            "type",
            "spotify_id",
            "href",
            "artists",
            "disc_number",
            "track_number",
            "duration_ms",
            "external_ids",
            "external_urls",
            "name",
            "popularity",
            "spotify_uri",
            "available_markets",
            "is_local",
            "created_at",
            "updated_at",
            "is_active",
        ]


class AlbumSerializer(serializers.ModelSerializer):
    images = AlbumImageSerializer(source="albumimage_set", many=True, read_only=True)
    tracks = TrackSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = [
            "external_urls",
            "external_ids",
            "tracks",
            "total_tracks",
            "genres",
            "images",
            "href",
            "spotify_id",
            "name",
            "popularity",
            "release_date",
            "release_date_precision",
            "type",
            "album_type",
            "spotify_uri",
            "created_at",
            "updated_at",
            "is_active",
            "label",
            "available_markets",
            "copyrights",
        ]
