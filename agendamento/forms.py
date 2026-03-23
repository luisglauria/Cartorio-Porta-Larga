from django import forms
from django.utils import timezone
from .models import Agendamento, Servico
import datetime


class AgendamentoForm(forms.ModelForm):
    data = forms.DateField(
        label='Data',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        help_text='Selecione uma data futura (segunda a sexta)'
    )
    hora = forms.TimeField(
        label='Horário',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    HORARIOS = [
        ('', 'Selecione...'),
        ('08:00', '08:00'), ('08:30', '08:30'), ('09:00', '09:00'), ('09:30', '09:30'),
        ('10:00', '10:00'), ('10:30', '10:30'), ('11:00', '11:00'), ('11:30', '11:30'),
        ('14:00', '14:00'), ('14:30', '14:30'), ('15:00', '15:00'), ('15:30', '15:30'),
        ('16:00', '16:00'), 
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hora'] = forms.ChoiceField(
            choices=self.HORARIOS,
            label='Horário',
            widget=forms.Select(attrs={'class': 'form-control'})
        )
        self.fields['servico'].queryset = Servico.objects.filter(ativo=True)
        self.fields['servico'].widget.attrs['class'] = 'form-control'
        self.fields['observacoes'].widget.attrs.update({
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Descreva sua demanda ou documentos que possui...'
        })

    class Meta:
        model = Agendamento
        fields = ['servico', 'data', 'hora', 'observacoes']

    def clean_data(self):
        data = self.cleaned_data['data']
        hoje = timezone.localdate()
        if data < hoje:
            raise forms.ValidationError('A data deve ser futura.')
        if data.weekday() >= 5:
            raise forms.ValidationError('Atendemos apenas de segunda a sexta-feira.')
        return data

    def clean(self):
        cleaned = super().clean()
        data = cleaned.get('data')
        hora_str = cleaned.get('hora')
        servico = cleaned.get('servico')
        if data and hora_str and servico:
            hora = datetime.time.fromisoformat(hora_str)
            if Agendamento.objects.filter(data=data, hora=hora, servico=servico).exclude(status='cancelado').exists():
                raise forms.ValidationError('Este horário já está reservado para este serviço. Escolha outro.')
        return cleaned
