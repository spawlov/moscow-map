from adminsortable2.admin import SortableAdminBase, SortableTabularInline

from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Image, Place


class PlaceInline(SortableTabularInline):
    model = Image
    fields = ["file", "get_preview"]
    readonly_fields = ["get_preview"]
    fk_name = "place"
    extra = 1

    def get_preview(self, image):
        return mark_safe(f'<img src="{image.file.url}" height="200">')

    get_preview.short_description = "Предпросмотр"


class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    model = Place
    ordering = ("pk",)
    list_display = (
        "id",
        "title",
    )
    list_display_links = ("title",)
    inlines = (PlaceInline,)


admin.site.register(Place, PlaceAdmin)
