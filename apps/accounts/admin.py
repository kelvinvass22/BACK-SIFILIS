from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class MyUserAdmin(UserAdmin):
    # Campos que aparecem na LISTA de usuários
    list_display = ('username', 'email', 'role', 'is_staff')
    
    # Campos que aparecem ao EDITAR um usuário
    fieldsets = UserAdmin.fieldsets + (
        ('Informações do TCC', {'fields': ('role', 'data_nascimento')}),
    )

    # AQUI ESTÁ O SEGREDO: Campos que aparecem ao ADICIONAR um novo usuário
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações do TCC', {
            'classes': ('wide',),
            'fields': ('role', 'data_nascimento'),
        }),
    )

    # Garante que o Django use o seu modelo customizado
    model = User