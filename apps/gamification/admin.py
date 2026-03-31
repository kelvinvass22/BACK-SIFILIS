from django.contrib import admin
from .models import Pontuacao

@admin.register(Pontuacao)
class PontuacaoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'get_jogo_display', 'pontos', 'data_conquista')
    list_filter = ('jogo',)