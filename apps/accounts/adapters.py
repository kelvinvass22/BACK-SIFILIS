from allauth.account.adapter import DefaultAccountAdapter
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

class CustomAccountAdapter(DefaultAccountAdapter):
    def send_mail(self, template_prefix, email, context):
        if template_prefix == 'account/email/password_reset_key':
            user = context.get('user')
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            # Link para o teu App Expo rodando na porta 8081 no local
            # context['password_reset_url'] = f"http://localhost:8081/auth/reset-password/{uid}/{token}"

            #produção 
            context['password_reset_url'] = f"appsifilis://auth/reset-password/{uid}/{token}"
        msg = self.render_mail(template_prefix, email, context)
        html_template = f"{template_prefix}_message.html"
        
        try:
            html_content = render_to_string(html_template, context)
            if isinstance(msg, EmailMultiAlternatives):
                msg.attach_alternative(html_content, "text/html")
            else:
                msg = EmailMultiAlternatives(msg.subject, msg.body, msg.from_email, msg.to)
                msg.attach_alternative(html_content, "text/html")
        except Exception as e:
            print(f"Erro ao renderizar HTML: {e}")
            
        msg.send()