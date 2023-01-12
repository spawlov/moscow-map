from django.contrib import admin

from .models import Place, Image


class PlaceInline(admin.TabularInline):
    model = Image
    readonly_fields = ('get_preview',)
    fk_name = 'place'
    extra = 3


class PlaceAdmin(admin.ModelAdmin):
    model = Place
    ordering = ('pk',)
    list_display = ('id', 'title',)
    list_display_links = ('title',)
    inlines = (PlaceInline,)


admin.site.register(Place, PlaceAdmin)
admin.site.register(Image)
