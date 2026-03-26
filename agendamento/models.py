from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Atendente(models.Model):
    DIAS_SEMANA = [
        (0, 'Segunda-feira'), (1, 'Terça-feira'), (2, 'Quarta-feira'),
        (3, 'Quinta-feira'), (4, 'Sexta-feira'),
    ]

    nome = models.CharField('Nome', max_length=100)
    ativo = models.BooleanField('Ativo', default=True)

    class Meta:
        verbose_name = 'Atendente'
        verbose_name_plural = 'Atendentes'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class HorarioAtendente(models.Model):
    DIAS_SEMANA = [
        (0, 'Segunda-feira'), (1, 'Terça-feira'), (2, 'Quarta-feira'),
        (3, 'Quinta-feira'), (4, 'Sexta-feira'),
    ]

    atendente = models.ForeignKey(Atendente, on_delete=models.CASCADE, related_name='horarios')
    dia_semana = models.IntegerField('Dia da semana', choices=DIAS_SEMANA)
    hora = models.TimeField('Hora')

    class Meta:
        verbose_name = 'Horário da Atendente'
        verbose_name_plural = 'Horários das Atendentes'
        ordering = ['dia_semana', 'hora']
        unique_together = ['atendente', 'dia_semana', 'hora']

    def __str__(self):
        return f'{self.atendente.nome} — {self.get_dia_semana_display()} às {self.hora.strftime("%H:%M")}'


class Servico(models.Model):
    nome = models.CharField('Nome do serviço', max_length=100)
    descricao = models.TextField('Descrição', blank=True)
    duracao_minutos = models.PositiveIntegerField('Duração (min)', default=30)
    preco = models.DecimalField('Preço (R$)', max_digits=8, decimal_places=2, null=True, blank=True)
    ativo = models.BooleanField('Ativo', default=True)
    agendavel = models.BooleanField('Disponível para agendamento', default=False)
    ordem = models.PositiveIntegerField('Ordem de exibição', default=0)
    resumo = models.CharField('Resumo (exibido no card)', max_length=200, blank=True)

    class Meta:
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'
        ordering = ['ordem', 'nome']

    def __str__(self):
        return self.nome


class HorarioDisponivel(models.Model):
    DIAS_SEMANA = [
        (0, 'Segunda-feira'), (1, 'Terça-feira'), (2, 'Quarta-feira'),
        (3, 'Quinta-feira'), (4, 'Sexta-feira'),
    ]
    dia_semana = models.IntegerField('Dia da semana', choices=DIAS_SEMANA)
    hora_inicio = models.TimeField('Hora de início')
    hora_fim = models.TimeField('Hora de fim')
    ativo = models.BooleanField('Ativo', default=True)

    class Meta:
        verbose_name = 'Horário disponível'
        verbose_name_plural = 'Horários disponíveis'
        ordering = ['dia_semana', 'hora_inicio']

    def __str__(self):
        return f'{self.get_dia_semana_display()} — {self.hora_inicio.strftime("%H:%M")} às {self.hora_fim.strftime("%H:%M")}'


class Agendamento(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
        ('concluido', 'Concluído'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='agendamentos', verbose_name='Cliente')
    servico = models.ForeignKey(Servico, on_delete=models.PROTECT, verbose_name='Serviço')
    atendente = models.ForeignKey(Atendente, on_delete=models.PROTECT, verbose_name='Atendente', null=True, blank=True)
    data = models.DateField('Data')
    hora = models.TimeField('Hora')
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='pendente')
    observacoes = models.TextField('Observações', blank=True)
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    email_confirmacao_enviado = models.BooleanField('E-mail enviado', default=False)
    lembrete_enviado = models.BooleanField('Lembrete enviado', default=False)

    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'
        ordering = ['-data', '-hora']
        unique_together = ['data', 'hora', 'atendente']

    def __str__(self):
        return f'{self.usuario.get_full_name() or self.usuario.username} — {self.servico} em {self.data.strftime("%d/%m/%Y")} às {self.hora.strftime("%H:%M")}'

    @property
    def pode_cancelar(self):
        from datetime import datetime, timedelta
        agendamento_dt = timezone.make_aware(datetime.combine(self.data, self.hora))
        return agendamento_dt > timezone.now() + timedelta(hours=2) and self.status in ['pendente', 'confirmado']
