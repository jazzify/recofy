from django.contrib import admin
from django.utils.html import format_html

from apps.recofy.admin.common import RecofyAdmin
from apps.recofy.models import Album, Artist


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
    def images(self, obj):
        images_formatted = self.image_queryset_format(list(obj.artistimage_set.all()))
        return format_html(format_string=images_formatted)
