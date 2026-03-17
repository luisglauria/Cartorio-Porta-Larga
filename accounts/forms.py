from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Perfil


class CadastroForm(UserCreationForm):
    first_name = forms.CharField(label='Nome', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu nome'}))
    last_name = forms.CharField(label='Sobrenome', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu sobrenome'}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'seu@email.com'}))
    cpf = forms.CharField(label='CPF', max_length=14, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '000.000.000-00'}))
    telefone = forms.CharField(label='Telefone', max_length=15, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(81) 90000-0000'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'cpf', 'telefone', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este e-mail já está cadastrado.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            user.perfil.cpf = self.cleaned_data['cpf']
            user.perfil.telefone = self.cleaned_data['telefone']
            user.perfil.save()
        return user


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'seu@email.com'})
        self.fields['username'].label = 'E-mail'
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': '••••••••'})


class PerfilForm(forms.ModelForm):
    first_name = forms.CharField(label='Nome', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Sobrenome', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Perfil
        fields = ['cpf', 'telefone']
        widgets = {
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
        }
