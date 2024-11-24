from django.contrib import admin
from .models import Project, Rating

# Mendaftarkan model Project ke admin
admin.site.register(Project)

# Menggunakan dekorator @admin.register untuk Rating
@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'rating', 'created_at')
    list_filter = ('rating', 'project')
