from django.db import models

class PostEducativo(models.Model):
    CATEGORIAS = (
        ('OQUE', 'O que é?'),
        ('PREV', 'Prevenção'),
        ('TRAT', 'Tratamento'),
    )
    categoria = models.CharField(max_length=4, choices=CATEGORIAS)
    titulo = models.CharField(max_length=200)
    texto = models.TextField()
    referencia = models.CharField(max_length=255, default="MARTINS et al, 2024")

    def __str__(self):
        return self.titulo