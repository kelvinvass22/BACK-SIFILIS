#!/bin/sh

# Espera o banco de dados ficar pronto (opcional mas bom)
echo "Aguardando migrações..."

# Roda as migrações para criar as tabelas no banco do Render
python manage.py migrate --noinput

# Coleta arquivos estáticos
python manage.py collectstatic --noinput

# Tenta criar um superusuário automaticamente (Troque os dados se quiser)
# Usamos o shell do python para não travar pedindo senha
echo "from django.contrib.auth import get_user_model; User = get_user_model(); \
User.objects.filter(username='admin').exists() or \
User.objects.create_superuser('admin', 'admin@email.com', 'sua_senha_forte')" | python manage.py shell

echo "Iniciando o servidor Gunicorn..."
exec gunicorn core.wsgi:application --bind 0.0.0.0:$PORT