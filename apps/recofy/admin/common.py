from django.contrib import admin

from apps.recofy.models.album import AlbumImage
from apps.recofy.models.artists import ArtistImage

RecofyImagesModelsType = ArtistImage | AlbumImage


class RecofyAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False

    def image_queryset_format(self, images: list[RecofyImagesModelsType]) -> str:
        full_html = ""

        for image in images:
            heading = f"<h4>Width: {image.width_px}px - Height:{image.height_px}px</h4>"
            a_image = f'<img src="{image.url}" style="max-width:{image.width_px}px; max-height:{image.height_px}px"/>'
            container = f"<div>{heading}{a_image}</div>"
            full_html += container

        return full_html
