from adminsortable2.admin import SortableStackedInline, SortableAdminBase
from django.contrib import admin
from .models import Place, PlaceImage


class PlaceImageInline(SortableStackedInline):
    model = PlaceImage
    extra = 1
    fields = ('image', 'image_preview')
    readonly_fields = ('image_preview',)


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ('title', 'short_description')
    search_fields = ('title',)
    inlines = [PlaceImageInline]


@admin.register(PlaceImage)
class PlaceImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'place', 'image_preview')
    list_filter = ('place',)
    search_fields = ('place__title',)
    ordering = ('place', 'order')
    readonly_fields = ('image_preview',)
