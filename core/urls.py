from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from dj_rest_auth.views import PasswordResetConfirmView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf import settings
from django.conf.urls.static import static

from apps.accounts.views import password_reset_confirm_view, registrar_usuario, gerenciar_perfil
from apps.content.views import PostEducativoViewSet
from apps.qna.views import DuvidaViewSet
from apps.gamification.views import PontuacaoViewSet

router = DefaultRouter()
router.register(r'conteudo', PostEducativoViewSet)
router.register(r'duvidas', DuvidaViewSet, basename='duvida')
router.register(r'ranking', PontuacaoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/usuarios/registrar/', registrar_usuario, name='registrar_usuario'),
    path('api/accounts/me/', gerenciar_perfil, name='gerenciar_perfil'),

    # ROTA DE RESET CORRIGIDA
    path('api/accounts/password/reset/confirm/<uidb64>/<token>/', 
         PasswordResetConfirmView.as_view(), 
         name='password_reset_confirm'),

    path('api/accounts/', include('dj_rest_auth.urls')),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)