from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLES = (
        ('IDOSO', 'Idoso'),
        ('PROFISSIONAL_SUS', 'Profissional SUS'),
        ('ADMIN', 'Administrador'),
    )
    role = models.CharField(max_length=20, choices=ROLES, default='IDOSO')
    data_nascimento = models.DateField(null=True, blank=True)
    telefone = models.CharField(max_length=20, null=True, blank=True) # ADICIONE ISSO
    cns = models.CharField(max_length=15, null=True, blank=True)
    is_verified_professional = models.BooleanField(default=False)