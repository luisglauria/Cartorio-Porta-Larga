from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Agendamento, Servico
from .forms import AgendamentoForm
from .utils import enviar_email_confirmacao, enviar_email_cancelamento
from django.views.decorators.csrf import csrf_exempt
import requests as req

# ── Páginas públicas ──────────────────────────────────────────────────────────
def home(request):
    servicos = Servico.objects.filter(ativo=True).exclude(nome__icontains='retificação — ')
    return render(request, 'base/home.html', {'servicos': servicos})

@csrf_exempt
def verificacao(request):
    from django.conf import settings
    if request.method == 'POST':
        token = request.POST.get('cf-turnstile-response')
        if token:
            resp = req.post('https://challenges.cloudflare.com/turnstile/v0/siteverify', data={
                'secret': settings.TURNSTILE_SECRET_KEY,
                'response': token,
            })
            if resp.json().get('success'):
                request.session['verificado'] = True
                request.session.save()
                return redirect('home')
        return render(request, 'base/verificacao.html', {
            'site_key': settings.TURNSTILE_SITE_KEY,
            'erro': True
        })
    return render(request, 'base/verificacao.html', {
        'site_key': settings.TURNSTILE_SITE_KEY
    })

def sobre(request):
    return render(request, 'base/sobre.html')


def servicos(request):
    servicos = Servico.objects.filter(ativo=True).exclude(nome__icontains='retificação — ')
    return render(request, 'base/servicos.html', {'servicos': servicos})

def contato(request):
    return render(request, 'base/contato.html')

def retificacao(request):
    from .models import Servico
    servicos = Servico.objects.filter(nome__icontains='retificação', ativo=False).order_by('ordem')
    return render(request, 'agendamento/retificacao.html', {'servicos': servicos})

def modelos_requerimentos(request):
    return render(request, 'base/modelos_requerimentos.html')

def sites_uteis(request):
    return render(request, 'base/sites_uteis.html')

def transparencia(request):
    return render(request, 'base/transparencia.html')

def politica_privacidade(request):
    return render(request, 'base/politica_privacidade.html')

# ── Agendamento ───────────────────────────────────────────────────────────────

@login_required
def novo_agendamento(request):
    servico_id = request.GET.get('servico')
    servico_selecionado = None
    if servico_id:
        from .models import Servico
        try:
            servico_selecionado = Servico.objects.get(pk=servico_id, ativo=True)
        except Servico.DoesNotExist:
            pass

    if request.method == 'POST':
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            import datetime
            agendamento = form.save(commit=False)
            agendamento.usuario = request.user
            hora_str = form.cleaned_data['hora']
            agendamento.hora = datetime.time.fromisoformat(hora_str)
            agendamento.save()
            enviar_email_confirmacao(agendamento)
            messages.success(request, 'Agendamento realizado com sucesso! Você receberá um e-mail de confirmação.')
            return redirect('meus_agendamentos')
    else:
        initial = {}
        if servico_selecionado:
            initial['servico'] = servico_selecionado
        form = AgendamentoForm(initial=initial)

    return render(request, 'agendamento/novo.html', {
        'form': form,
        'servico_selecionado': servico_selecionado,
    })


@login_required
def meus_agendamentos(request):
    hoje = timezone.localdate()
    proximos = Agendamento.objects.filter(
        usuario=request.user,
        data__gte=hoje,
        status__in=['pendente', 'confirmado']
    ).order_by('data', 'hora')
    historico = Agendamento.objects.filter(
        usuario=request.user
    ).exclude(
        data__gte=hoje, status__in=['pendente', 'confirmado']
    ).order_by('-data', '-hora')[:20]
    return render(request, 'agendamento/meus.html', {
        'proximos': proximos,
        'historico': historico,
    })


@login_required
def cancelar_agendamento(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk, usuario=request.user)
    if not agendamento.pode_cancelar:
        messages.error(request, 'Este agendamento não pode ser cancelado (muito próximo do horário ou já finalizado).')
        return redirect('meus_agendamentos')
    if request.method == 'POST':
        agendamento.status = 'cancelado'
        agendamento.save()
        enviar_email_cancelamento(agendamento)
        messages.success(request, 'Agendamento cancelado.')
        return redirect('meus_agendamentos')
    return render(request, 'agendamento/cancelar.html', {'agendamento': agendamento})


@login_required
def detalhe_agendamento(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk, usuario=request.user)
    return render(request, 'agendamento/detalhe.html', {'agendamento': agendamento})
