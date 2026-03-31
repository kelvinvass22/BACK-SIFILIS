from django.contrib import admin
from .models import PostEducativo

@admin.register(PostEducativo)
class PostEducativoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'referencia')
    list_filter = ('categoria',)
    search_fields = ('titulo', 'texto')