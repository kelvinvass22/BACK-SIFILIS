from django.db import models
from django.conf import settings

class Pontuacao(models.Model):
    JOGOS = (
        ('CACA', 'Caça-Palavras'),
        ('AGIL', 'Agilidade (Baratinha)'),
    )

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='pontuacoes'
    )
    jogo = models.CharField(max_length=4, choices=JOGOS)
    pontos = models.IntegerField(default=0)
    data_conquista = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Pontuações"
        ordering = ['-pontos']

    def __str__(self):
        return f"{self.usuario.username} - {self.get_jogo_display()}: {self.pontos}"