from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User  # Importa o SEU modelo customizado

@admin.register(User)
class MyUserAdmin(UserAdmin):
    # Campos que aparecem na listagem
    list_display = ('username', 'email', 'role', 'is_staff', 'is_verified_professional')
    list_filter = ('role', 'is_staff', 'is_verified_professional')
    
    # Adicionando seus campos customizados na tela de edição
    fieldsets = UserAdmin.fieldsets + (
        ('Informações do Sistema', {
            'fields': ('role', 'foto', 'telefone', 'cns', 'is_verified_professional', 'data_nascimento')
        }),
    )

    # Adicionando campos na tela de criação de novo usuário
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações do Sistema', {
            'fields': ('role', 'email', 'data_nascimento'),
        }),
    )

    model = User