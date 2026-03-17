from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Agendamento, Servico
from .forms import AgendamentoForm
from .utils import enviar_email_confirmacao, enviar_email_cancelamento


# ── Páginas públicas ──────────────────────────────────────────────────────────

def home(request):
    servicos = Servico.objects.filter(ativo=True)[:6]
    return render(request, 'base/home.html', {'servicos': servicos})


def sobre(request):
    return render(request, 'base/sobre.html')


def servicos(request):
    servicos = Servico.objects.filter(ativo=True)
    return render(request, 'base/servicos.html', {'servicos': servicos})


def institucional(request):
    return render(request, 'base/institucional.html')


def contato(request):
    return render(request, 'base/contato.html')


# ── Agendamento ───────────────────────────────────────────────────────────────

@login_required
def novo_agendamento(request):
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
        form = AgendamentoForm()
    return render(request, 'agendamento/novo.html', {'form': form})


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
