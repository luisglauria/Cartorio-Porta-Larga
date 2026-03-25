from django import forms
from django.utils import timezone
from .models import Agendamento, Servico, Atendente
import datetime


class AgendamentoForm(forms.ModelForm):
    data = forms.DateField(
        label='Data',
        widget=forms.HiddenInput(),
    )
    hora = forms.CharField(
        label='Horário',
        widget=forms.HiddenInput(),
    )
    atendente = forms.ModelChoiceField(
        queryset=Atendente.objects.filter(ativo=True),
        widget=forms.HiddenInput(),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['servico'].queryset = Servico.objects.filter(ativo=True, agendavel=True)
        self.fields['servico'].widget.attrs['class'] = 'form-control'
        self.fields['observacoes'].widget.attrs.update({
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Descreva sua demanda ou documentos que possui...'
        })

    class Meta:
        model = Agendamento
        fields = ['servico', 'atendente', 'data', 'hora', 'observacoes']

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
        atendente = cleaned.get('atendente')
        if data and hora_str and atendente:
            try:
                hora = datetime.time.fromisoformat(hora_str)
                if Agendamento.objects.filter(
                    data=data,
                    hora=hora,
                    atendente=atendente
                ).exclude(status='cancelado').exists():
                    raise forms.ValidationError('Este horário já está reservado. Escolha outro horário ou atendente.')
            except ValueError:
                raise forms.ValidationError('Horário inválido.')
        return cleaned