from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import (
    SpectacularAPIView, 
    SpectacularRedocView, 
    SpectacularSwaggerView
)

# ViewSets
from apps.content.views import PostEducativoViewSet
from apps.qna.views import DuvidaViewSet
from apps.gamification.views import PontuacaoViewSet

from apps.accounts.views import registrar_usuario, gerenciar_perfil
router = DefaultRouter()
router.register(r'conteudo', PostEducativoViewSet)
router.register(r'duvidas', DuvidaViewSet, basename='duvida')
router.register(r'ranking', PontuacaoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/usuarios/registrar/', registrar_usuario, name='registrar_usuario'),
    
    # ESTA É A ROTA QUE ESTAVA FALTANDO NO SEU LOG:
    path('api/accounts/me/', gerenciar_perfil, name='gerenciar_perfil'),

    path('api/', include(router.urls)),
    
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Swagger
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]