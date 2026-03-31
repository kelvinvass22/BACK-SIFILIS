from django.contrib import admin
from .models import Duvida

@admin.register(Duvida)
class DuvidaAdmin(admin.ModelAdmin):
    # Nomes exatos baseados no seu models.py:
    list_display = ('texto_pergunta', 'usuario_idoso', 'status', 'data_pergunta') 
    list_filter = ('status', 'data_pergunta')
    search_fields = ('texto_pergunta', 'usuario_idoso__username')