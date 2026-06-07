from django.contrib import admin
from .models import Vest, Video, Rec, Artwork, Film

admin.site.register(Vest)
admin.site.register(Video)
admin.site.register(Rec)

@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ('title', 'screening_date', 'ticket_price', 'tag', 'featured')
    list_editable = ('featured', 'tag')
    list_filter = ('tag', 'featured')
    ordering = ('screening_date',)


@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'title', 'created_at')
    search_fields = ('author_name', 'title')
    prepopulated_fields = {'slug': ('author_name', 'title')}
    ordering = ('-created_at',)
