from django.contrib import admin
from django.utils.html import format_html

from apps.recofy.admin.common import RecofyAdmin
from apps.recofy.models.album import Album


class AlbumArtistInlineAdmin(admin.TabularInline):
    model = Album.artists.through


class AlbumTracksInlineAdmin(admin.TabularInline):
    model = Album.tracks.through


@admin.register(Album)
class AlbumAdmin(RecofyAdmin):
    # list
    search_fields = ("name",)
    list_display = (
        "name",
        "popularity",
        "is_active",
        "created_at",
        "updated_at",
    )
    list_filter = ("is_active", "album_type")

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
                    "album_type",
                    "release_date",
                    "release_date_precision",
                    "popularity",
                    "genres",
                    "external_urls",
                    "external_ids",
                    "images",
                    "copyrights",
                    "available_markets",
                )
            },
        ),
        ("Information", {"fields": ("is_active", "created_at", "updated_at")}),
    )

    inlines = (AlbumArtistInlineAdmin, AlbumTracksInlineAdmin)

    @admin.display(description="Album images")
    def images(self, obj):
        images_formatted = self.image_queryset_format(list(obj.albumimage_set.all()))
        return format_html(format_string=images_formatted)
