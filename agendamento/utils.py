from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def enviar_email_confirmacao(agendamento):
    """Envia e-mail de confirmação para o cliente."""
    try:
        contexto = {
            'agendamento': agendamento,
            'usuario': agendamento.usuario,
        }
        assunto = f'Confirmação de Agendamento — Cartório Porta Larga'
        mensagem_txt = render_to_string('agendamento/email_confirmacao.txt', contexto)
        mensagem_html = render_to_string('agendamento/email_confirmacao.html', contexto)

        send_mail(
            subject=assunto,
            message=mensagem_txt,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[agendamento.usuario.email],
            html_message=mensagem_html,
            fail_silently=False,
        )
        agendamento.email_confirmacao_enviado = True
        agendamento.save(update_fields=['email_confirmacao_enviado'])
        return True
    except Exception as e:
        print(f'Erro ao enviar e-mail: {e}')
        return False


def enviar_email_cancelamento(agendamento):
    """Envia e-mail de cancelamento para o cliente."""
    try:
        assunto = f'Agendamento Cancelado — Cartório Porta Larga'
        mensagem = (
            f'Olá, {agendamento.usuario.get_full_name() or agendamento.usuario.username}!\n\n'
            f'Seu agendamento foi cancelado:\n'
            f'Serviço: {agendamento.servico}\n'
            f'Data: {agendamento.data.strftime("%d/%m/%Y")}\n'
            f'Horário: {agendamento.hora.strftime("%H:%M")}\n\n'
            f'Para reagendar, acesse nosso site.\n\n'
            f'Atenciosamente,\nCartório Porta Larga'
        )
        send_mail(
            subject=assunto,
            message=mensagem,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[agendamento.usuario.email],
            fail_silently=True,
        )
        return True
    except Exception as e:
        print(f'Erro ao enviar e-mail de cancelamento: {e}')
        return False
