#!/bin/sh

# 1. VALIDAÇÃO DE AMBIENTE
echo "--- Verificando Ambiente ---"
if [ -z "$DATABASE_URL" ]; then
    echo "AVISO: DATABASE_URL não encontrada. Usando configurações padrão (Local/Docker)."
else
    echo "DATABASE_URL detectada. Preparando conexão com o banco remoto..."
fi

# 2. ESPERA PELO BANCO (OPCIONAL MAS SEGURO)
# Se estiver no Render, ele costuma esperar o banco subir, mas via código é mais garantido.
echo "Aguardando banco de dados ficar disponível..."

# 3. MIGRAÇÕES
echo "Executando: python manage.py migrate"
# O --noinput evita que o script pare pedindo confirmação
python manage.py migrate --noinput || { echo "ERRO: Falha ao rodar migrações. Verifique a DATABASE_URL."; exit 1; }

# 4. ARQUIVOS ESTÁTICOS
echo "Executando: collectstatic"
mkdir -p /app/staticfiles  # Garante que a pasta existe
python manage.py collectstatic --noinput --clear # O --clear limpa lixo antigo

# 5. SUPERUSER AUTOMÁTICO
# Note que usei variáveis ou valores padrão para evitar erros de sintaxe no shell
echo "Verificando superusuário..."
echo "from django.contrib.auth import get_user_model; \
User = get_user_model(); \
username = 'admin'; \
email = 'admin@email.com'; \
password = 'sua_senha_aqui'; \
not User.objects.filter(username=username).exists() and \
User.objects.create_superuser(username, email, password); \
print('Usuário admin verificado/criado')" | python manage.py shell

# 6. START DO SERVIDOR
echo "--- Iniciando Gunicorn ---"
PORT_NUMBER=${PORT:-8000}
echo "Servidor subindo na porta: $PORT_NUMBER"

exec gunicorn core.wsgi:application --bind 0.0.0.0:$PORT_NUMBER