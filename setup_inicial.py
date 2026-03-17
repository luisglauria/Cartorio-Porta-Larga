#!/usr/bin/env python
"""
Script de setup inicial do Cartório Porta Larga.
Execute após instalar as dependências:

    python setup_inicial.py
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cartorio.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth.models import User
from agendamento.models import Servico, HorarioDisponivel


def criar_servicos():
    servicos = [
        {'nome': 'Escritura pública', 'descricao': 'Compra e venda, doação, divórcio, inventário e outros atos notariais que exigem forma pública.', 'duracao_minutos': 60, 'preco': None, 'ordem': 1},
        {'nome': 'Procuração pública', 'descricao': 'Procuração ad judicia, ad negotia, para fins específicos e gerais com plena validade jurídica.', 'duracao_minutos': 30, 'preco': 89.00, 'ordem': 2},
        {'nome': 'Reconhecimento de firma', 'descricao': 'Reconhecimento de firma por autenticidade ou semelhança em documentos diversos.', 'duracao_minutos': 15, 'preco': 15.00, 'ordem': 3},
        {'nome': 'Autenticação de documentos', 'descricao': 'Autenticação de cópias de documentos originais com fé pública.', 'duracao_minutos': 15, 'preco': 15.00, 'ordem': 4},
        {'nome': 'Certidão de inteiro teor', 'descricao': 'Certidão de atos lavrados neste cartório para todos os fins de direito.', 'duracao_minutos': 30, 'preco': 45.00, 'ordem': 5},
        {'nome': 'Testamento público', 'descricao': 'Redação e registro de testamento com plena validade jurídica e sigilo garantido.', 'duracao_minutos': 90, 'preco': None, 'ordem': 6},
        {'nome': 'Certidão eletrônica', 'descricao': 'Emissão digital com QR Code e validade em todo o território nacional.', 'duracao_minutos': 20, 'preco': 35.00, 'ordem': 7},
        {'nome': 'Ata notarial', 'descricao': 'Lavração de ata notarial para constatação de fatos, documentos digitais e outros.', 'duracao_minutos': 45, 'preco': None, 'ordem': 8},
    ]
    criados = 0
    for s in servicos:
        obj, created = Servico.objects.get_or_create(nome=s['nome'], defaults=s)
        if created:
            criados += 1
    print(f'  ✓ {criados} serviços criados ({Servico.objects.count()} total)')


def criar_horarios():
    horarios = []
    for dia in range(5):  # 0=seg a 4=sex
        horarios.append({'dia_semana': dia, 'hora_inicio': '08:00', 'hora_fim': '12:00'})
        horarios.append({'dia_semana': dia, 'hora_inicio': '14:00', 'hora_fim': '18:00'})
    criados = 0
    for h in horarios:
        obj, created = HorarioDisponivel.objects.get_or_create(**h)
        if created:
            criados += 1
    print(f'  ✓ {criados} horários criados')


def criar_superuser():
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@cartorioportalarga.com.br',
            password='admin123',
            first_name='Administrador',
            last_name='Cartório',
        )
        print('  ✓ Superusuário criado — login: admin / senha: admin123')
        print('  ⚠  TROQUE A SENHA antes de usar em produção!')
    else:
        print('  · Superusuário já existe')


def criar_usuario_teste():
    if not User.objects.filter(username='cliente@teste.com').exists():
        user = User.objects.create_user(
            username='cliente@teste.com',
            email='cliente@teste.com',
            password='cliente123',
            first_name='Maria',
            last_name='Silva',
        )
        user.perfil.cpf = '000.000.000-00'
        user.perfil.telefone = '(81) 90000-0000'
        user.perfil.save()
        print('  ✓ Usuário de teste criado — login: cliente@teste.com / senha: cliente123')
    else:
        print('  · Usuário de teste já existe')


if __name__ == '__main__':
    print('\n=== Setup Cartório Porta Larga ===\n')

    print('[1] Rodando migrations...')
    from django.core.management import call_command
    call_command('migrate', verbosity=0)
    print('  ✓ Migrations aplicadas')

    print('\n[2] Criando serviços...')
    criar_servicos()

    print('\n[3] Criando horários disponíveis...')
    criar_horarios()

    print('\n[4] Criando superusuário...')
    criar_superuser()

    print('\n[5] Criando usuário de teste...')
    criar_usuario_teste()

    print('\n=== Tudo pronto! ===')
    print('\nPara iniciar o servidor:')
    print('  python manage.py runserver')
    print('\nAcesse:')
    print('  Site:        http://localhost:8000')
    print('  Admin:       http://localhost:8000/admin  (admin / admin123)')
    print('  API:         http://localhost:8000/api/')
    print('  API Token:   POST http://localhost:8000/api/auth/token/')
    print()
