from django.db import models
from django.conf import settings

class Duvida(models.Model):
    STATUS_CHOICES = (('PENDENTE', 'Pendente'), ('RESPONDIDA', 'Respondida'))
    
    usuario_idoso = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='minhas_duvidas')
    texto_pergunta = models.TextField()
    data_pergunta = models.DateTimeField(auto_now_add=True)
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDENTE')
    
    texto_resposta = models.TextField(blank=True, null=True)
    respondido_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'PROFISSIONAL_SUS'})
    data_resposta = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Dúvida"
        ordering = ['-data_pergunta']