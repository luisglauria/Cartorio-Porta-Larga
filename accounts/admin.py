from django.contrib import admin
from .models import Perfil


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'cpf', 'telefone']
    search_fields = ['usuario__first_name', 'usuario__last_name', 'usuario__email', 'cpf']
