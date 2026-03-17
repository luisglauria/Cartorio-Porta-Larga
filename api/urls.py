from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServicoViewSet, AgendamentoViewSet, MeuPerfilView, CustomObtainToken

router = DefaultRouter()
router.register('servicos', ServicoViewSet, basename='api-servicos')
router.register('agendamentos', AgendamentoViewSet, basename='api-agendamentos')
router.register('perfil', MeuPerfilView, basename='api-perfil')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', CustomObtainToken.as_view(), name='api-token'),
]
