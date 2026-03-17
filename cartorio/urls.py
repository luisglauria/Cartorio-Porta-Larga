from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from agendamento import views as ag_views

admin.site.site_header = 'Cartório Porta Larga — Administração'
admin.site.site_title = 'Cartório Porta Larga'
admin.site.index_title = 'Painel Administrativo'

urlpatterns = [
    path('', ag_views.home, name='home'),
    path('sobre/', ag_views.sobre, name='sobre'),
    path('servicos/', ag_views.servicos, name='servicos'),
    path('institucional/', ag_views.institucional, name='institucional'),
    path('contato/', ag_views.contato, name='contato'),
    path('agendamento/', include('agendamento.urls')),
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
