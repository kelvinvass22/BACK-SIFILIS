import os
from mailjet_rest import Client
from allauth.account.adapter import DefaultAccountAdapter
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

class CustomAccountAdapter(DefaultAccountAdapter):
    def send_mail(self, template_prefix, email, context):
        # 1. Credenciais do Mailjet (Pegue a API Key e Secret no painel)
        api_key = os.environ.get('MAILJET_API_KEY')
        api_secret = os.environ.get('MAILJET_SECRET_KEY')
        mailjet = Client(auth=(api_key, api_secret), version='v3.1')

        # 2. Lógica do seu link appsifilis://
        if template_prefix == 'account/email/password_reset_key':
          user = context.get('user')
          uid = urlsafe_base64_encode(force_bytes(user.pk))
          token = default_token_generator.make_token(user)
          context['password_reset_url'] = f"https://back-sifilis.onrender.com/auth/reset-password/{uid}/{token}"
          
          context['uid'] = uid
          context['token'] = token
            
        # 3. Renderiza o conteúdo do e-mail
        subject = render_to_string(f'{template_prefix}_subject.txt', context).replace('\n', '')
        # Tenta carregar o HTML, se não existir usa o texto puro
        try:
            html_content = render_to_string(f"{template_prefix}_message.html", context)
        except:
            html_content = render_to_string(f"{template_prefix}_message.txt", context)

        # 4. Envia via API (O drible no bloqueio do Render)
        data = {
          'Messages': [
            {
              "From": {
                "Email": "kelvinvass12@gmail.com", # O e-mail que você cadastrou lá
                "Name": "App Sífilis 60+"
              },
              "To": [{"Email": email}],
              "Subject": subject,
              "HTMLPart": html_content
            }
          ]
        }

        try:
            result = mailjet.send.create(data=data)
            print(f"Mailjet Status: {result.status_code}")
        except Exception as e:
            print(f"Erro na API do Mailjet: {e}")