from django.contrib import admin
from .models import Place, PlaceImage


class PlaceImageInline(admin.TabularInline):
    model = PlaceImage
    extra = 1
    fields = ('image', 'description', 'order')
    ordering = ('order',)


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('title', 'description_short')
    search_fields = ('title',)
    inlines = [PlaceImageInline]


@admin.register(PlaceImage)
class PlaceImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'place', 'description',)
    list_filter = ('place',)
    search_fields = ('description', 'place__title')
    ordering = ('place', 'order')
