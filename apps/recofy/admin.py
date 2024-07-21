from django.contrib import admin
from django.utils.html import format_html

from apps.recofy.models.album import Album
from apps.recofy.models.artists import Artist
from apps.recofy.models.tracks import Track


class RecofyAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Track)
class TrackAdmin(RecofyAdmin):
    pass  # TODO:


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
    def images(self, obj):  # TODO: Duplicated code logic, fix this
        full_html = ""

        for image in list(obj.albumimage_set.all()):
            heading = f"<h4>Width: {image.width_px}px - Height:{image.height_px}px</h4>"
            a_image = f'<img src="{image.url}" style="max-width:{image.width_px}px; max-height:{image.height_px}px"/>'
            container = f"<div>{heading}{a_image}</div>"
            full_html += container

        return format_html(full_html)


class ArtistAlbumInlineAdmin(admin.TabularInline):
    model = Album.artists.through


@admin.register(Artist)
class ArtistAdmin(RecofyAdmin):
    # list
    search_fields = ("name",)
    list_display = (
        "name",
        "popularity",
        "is_active",
        "created_at",
        "updated_at",
        "followers",
    )
    list_filter = ("genres", "is_active")

    # detail
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "spotify_uri",
                    "spotify_id",
                    "href",
                    "name",
                    "popularity",
                    "genres",
                    "external_urls",
                    "followers",
                    "images",
                )
            },
        ),
        ("Information", {"fields": ("is_active", "created_at", "updated_at")}),
    )
    inlines = (ArtistAlbumInlineAdmin,)

    @admin.display(description="Artist images")
    def images(self, obj):  # TODO: Duplicated code logic, fix this
        full_html = ""

        for image in list(obj.artistimage_set.all()):
            heading = f"<h4>Width: {image.width_px}px - Height:{image.height_px}px</h4>"
            a_image = f'<img src="{image.url}" style="max-width:{image.width_px}px; max-height:{image.height_px}px"/>'
            container = f"<div>{heading}{a_image}</div>"
            full_html += container

        return format_html(full_html)
