from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Place, Image


class PlaceInline(admin.TabularInline):
    model = Image
    readonly_fields = ('get_preview',)
    fk_name = 'place'
    extra = 1

    def get_preview(self, obj):
        return mark_safe(f'<img src="{obj.file.url}" height="200">')
    get_preview.short_description = 'Предпросмотр'


class PlaceAdmin(admin.ModelAdmin):
    model = Place
    ordering = ('pk',)
    list_display = ('id', 'title',)
    list_display_links = ('title',)
    inlines = (PlaceInline,)


admin.site.register(Place, PlaceAdmin)
