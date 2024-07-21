from django.contrib import admin

from apps.recofy.admin.common import RecofyAdmin
from apps.recofy.models.album import Album
from apps.recofy.models.tracks import Track


class ArtistTrackInlineAdmin(admin.TabularInline):
    verbose_name = "ARTIST"
    model = Track.artists.through


class TrackAlbumInlineAdmin(admin.TabularInline):
    verbose_name = "ALBUM"
    model = Album.tracks.through


@admin.register(Track)
class TrackAdmin(RecofyAdmin):
    # list
    search_fields = ("name", "artists__name", "album__name")
    list_display = (
        "name",
        "is_playable",
        "popularity",
        "explicit",
        "is_active",
        "created_at",
        "updated_at",
    )
    list_filter = ("is_active", "is_playable", "explicit")

    # detail
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "spotify_id",
                    "spotify_uri",
                    "href",
                    "type",
                    "external_urls",
                    "external_ids",
                    "is_local",
                    "available_markets",
                )
            },
        ),
        (
            "Track",
            {"fields": ("disc_number", "track_number", "duration_ms", "popularity")},
        ),
        ("Information", {"fields": ("is_active", "created_at", "updated_at")}),
    )
    inlines = (ArtistTrackInlineAdmin, TrackAlbumInlineAdmin)
