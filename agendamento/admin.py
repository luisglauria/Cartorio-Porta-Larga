from django.contrib import admin
from django.utils.html import format_html
from .models import Agendamento, Servico, HorarioDisponivel, Atendente, HorarioAtendente


class HorarioAtendenteInline(admin.TabularInline):
    model = HorarioAtendente
    extra = 1
    fields = ['dia_semana', 'hora']


@admin.register(Atendente)
class AtendenteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ativo']
    list_editable = ['ativo']
    inlines = [HorarioAtendenteInline]


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'duracao_minutos', 'preco', 'ativo', 'agendavel', 'ordem']
    list_editable = ['ativo', 'agendavel', 'ordem']
    search_fields = ['nome']


@admin.register(HorarioDisponivel)
class HorarioDisponivelAdmin(admin.ModelAdmin):
    list_display = ['dia_semana', 'hora_inicio', 'hora_fim', 'ativo']
    list_editable = ['ativo']


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ['usuario_nome', 'servico', 'atendente', 'data', 'hora', 'status_badge', 'email_confirmacao_enviado', 'criado_em']
    list_filter = ['status', 'servico', 'atendente', 'data']
    search_fields = ['usuario__first_name', 'usuario__last_name', 'usuario__email', 'usuario__username']
    date_hierarchy = 'data'
    list_per_page = 30
    readonly_fields = ['criado_em', 'atualizado_em', 'email_confirmacao_enviado']
    actions = ['confirmar', 'cancelar', 'marcar_concluido']

    fieldsets = (
        ('Cliente', {'fields': ('usuario',)}),
        ('Agendamento', {'fields': ('servico', 'atendente', 'data', 'hora', 'status', 'observacoes')}),
        ('Controle', {'fields': ('email_confirmacao_enviado', 'criado_em', 'atualizado_em')}),
    )

    def usuario_nome(self, obj):
        return obj.usuario.get_full_name() or obj.usuario.username
    usuario_nome.short_description = 'Cliente'

    def status_badge(self, obj):
        cores = {
            'pendente': '#F59E0B',
            'confirmado': '#10B981',
            'cancelado': '#EF4444',
            'concluido': '#6B7280',
        }
        cor = cores.get(obj.status, '#999')
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 10px;border-radius:12px;font-size:11px;">{}</span>',
            cor, obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    def confirmar(self, request, queryset):
        updated = queryset.filter(status='pendente').update(status='confirmado')
        self.message_user(request, f'{updated} agendamento(s) confirmado(s).')
    confirmar.short_description = 'Confirmar selecionados'

    def cancelar(self, request, queryset):
        updated = queryset.filter(status__in=['pendente', 'confirmado']).update(status='cancelado')
        self.message_user(request, f'{updated} agendamento(s) cancelado(s).')
    cancelar.short_description = 'Cancelar selecionados'

    def marcar_concluido(self, request, queryset):
        updated = queryset.filter(status='confirmado').update(status='concluido')
        self.message_user(request, f'{updated} agendamento(s) marcado(s) como concluído.')
    marcar_concluido.short_description = 'Marcar como concluído'