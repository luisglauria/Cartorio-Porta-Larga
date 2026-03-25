from django.urls import path
from . import views

urlpatterns = [
    path('novo/', views.novo_agendamento, name='novo_agendamento'),
    path('meus/', views.meus_agendamentos, name='meus_agendamentos'),
    path('<int:pk>/', views.detalhe_agendamento, name='detalhe_agendamento'),
    path('<int:pk>/cancelar/', views.cancelar_agendamento, name='cancelar_agendamento'),
    path('retificacao/', views.retificacao, name='retificacao'),
    path('horarios-disponiveis/', views.horarios_disponiveis, name='horarios_disponiveis'),
]