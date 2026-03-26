from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Envia lembretes de WhatsApp 3 horas antes do agendamento'

    def handle(self, *args, **kwargs):
        from agendamento.models import Agendamento

        agora = timezone.localtime()
        em_3h = agora + timedelta(hours=3)

        agendamentos = Agendamento.objects.filter(
            data=em_3h.date(),
            hora__gte=(em_3h - timedelta(minutes=5)).time(),
            hora__lte=(em_3h + timedelta(minutes=5)).time(),
            status__in=['pendente', 'confirmado'],
            lembrete_enviado=False,
        )

        self.stdout.write(f'Verificando lembretes... {agendamentos.count()} encontrado(s)')

        for ag in agendamentos:
            self.enviar_lembrete(ag)

    def enviar_lembrete(self, agendamento):
        from django.conf import settings
        from twilio.rest import Client
        from accounts.models import Perfil

        try:
            perfil = Perfil.objects.get(usuario=agendamento.usuario)
            telefone = perfil.telefone.replace('(', '').replace(')', '').replace(' ', '').replace('-', '')
            if not telefone.startswith('+'):
                telefone = '+55' + telefone

            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

            nome = agendamento.usuario.get_full_name() or agendamento.usuario.username
            data = agendamento.data.strftime('%d/%m/%Y')
            hora = agendamento.hora.strftime('%H:%M')
            atendente = agendamento.atendente.nome if agendamento.atendente else 'a definir'

            mensagem = (
                f'⏰ *Lembrete de agendamento!*\n\n'
                f'Olá, {nome}!\n\n'
                f'Você tem um agendamento em *3 horas* no Cartório Porta Larga.\n\n'
                f'📋 *Serviço:* {agendamento.servico}\n'
                f'👤 *Atendente:* {atendente}\n'
                f'📅 *Data:* {data}\n'
                f'🕐 *Horário:* {hora}\n\n'
                f'📍 Estr. da Batalha, 2305 D — Prazeres, Jaboatão dos Guararapes - PE\n\n'
                f'Por favor, confirme sua presença respondendo:\n'
                f'✅ *SIM* — para confirmar\n'
                f'❌ *NÃO* — para cancelar\n\n'
                f'_Cartório Porta Larga_'
            )

            msg = client.messages.create(
                from_=settings.TWILIO_WHATSAPP_FROM,
                to=f'whatsapp:{telefone}',
                body=mensagem,
            )

            agendamento.lembrete_enviado = True
            agendamento.save(update_fields=['lembrete_enviado'])

            self.stdout.write(self.style.SUCCESS(f'Lembrete enviado para {nome} ({telefone}) — SID: {msg.sid}'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao enviar lembrete: {e}'))
