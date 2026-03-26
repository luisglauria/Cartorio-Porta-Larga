from django.conf import settings


def enviar_whatsapp_confirmacao(agendamento):
    print(f'=== INICIANDO ENVIO WHATSAPP ===')
    try:
        from twilio.rest import Client
        from accounts.models import Perfil

        print(f'Usuario: {agendamento.usuario}')
        perfil = Perfil.objects.get(usuario=agendamento.usuario)
        print(f'Telefone raw: {perfil.telefone}')
        
        telefone = perfil.telefone.replace('(', '').replace(')', '').replace(' ', '').replace('-', '')
        if not telefone.startswith('+'):
            telefone = '+55' + telefone
        print(f'Telefone formatado: {telefone}')

        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        print(f'Client criado. SID: {settings.TWILIO_ACCOUNT_SID}')

        nome = agendamento.usuario.get_full_name() or agendamento.usuario.username
        data = agendamento.data.strftime('%d/%m/%Y')
        hora = agendamento.hora.strftime('%H:%M')
        atendente = agendamento.atendente.nome if agendamento.atendente else 'a definir'

        mensagem = (
            f'✅ *Agendamento confirmado!*\n\n'
            f'Olá, {nome}!\n\n'
            f'Seu agendamento no *Cartório Porta Larga* foi realizado com sucesso.\n\n'
            f'📋 *Serviço:* {agendamento.servico}\n'
            f'👤 *Atendente:* {atendente}\n'
            f'📅 *Data:* {data}\n'
            f'🕐 *Horário:* {hora}\n\n'
            f'📍 Estr. da Batalha, 2305 D — Prazeres, Jaboatão dos Guararapes - PE\n\n'
            f'Em caso de dúvidas, entre em contato conosco.\n'
            f'_Cartório Porta Larga_'
        )

        msg = client.messages.create(
            from_=settings.TWILIO_WHATSAPP_FROM,
            to=f'whatsapp:{telefone}',
            body=mensagem,
        )
        print(f'Mensagem enviada! SID: {msg.sid} Status: {msg.status}')

        agendamento.email_confirmacao_enviado = True
        agendamento.save(update_fields=['email_confirmacao_enviado'])
        return True

    except Exception as e:
        print(f'ERRO ao enviar WhatsApp: {e}')
        import traceback
        traceback.print_exc()
        return False


def enviar_whatsapp_cancelamento(agendamento):
    print(f'=== INICIANDO ENVIO WHATSAPP CANCELAMENTO ===')
    try:
        from twilio.rest import Client
        from accounts.models import Perfil

        perfil = Perfil.objects.get(usuario=agendamento.usuario)
        telefone = perfil.telefone.replace('(', '').replace(')', '').replace(' ', '').replace('-', '')
        if not telefone.startswith('+'):
            telefone = '+55' + telefone

        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        nome = agendamento.usuario.get_full_name() or agendamento.usuario.username
        data = agendamento.data.strftime('%d/%m/%Y')
        hora = agendamento.hora.strftime('%H:%M')

        mensagem = (
            f'❌ *Agendamento cancelado*\n\n'
            f'Olá, {nome}!\n\n'
            f'Seu agendamento foi cancelado:\n\n'
            f'📋 *Serviço:* {agendamento.servico}\n'
            f'📅 *Data:* {data}\n'
            f'🕐 *Horário:* {hora}\n\n'
            f'Para reagendar, acesse nosso site.\n\n'
            f'_Cartório Porta Larga_'
        )

        msg = client.messages.create(
            from_=settings.TWILIO_WHATSAPP_FROM,
            to=f'whatsapp:{telefone}',
            body=mensagem,
        )
        print(f'Mensagem enviada! SID: {msg.sid}')
        return True

    except Exception as e:
        print(f'ERRO ao enviar WhatsApp cancelamento: {e}')
        import traceback
        traceback.print_exc()
        return False


def enviar_email_confirmacao(agendamento):
    return enviar_whatsapp_confirmacao(agendamento)


def enviar_email_cancelamento(agendamento):
    return enviar_whatsapp_cancelamento(agendamento)