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
        {'nome': 'Nascimento', 'resumo': 'Registro de nascimento e emissão de certidão. Serviço gratuito, emitido na hora.', 'descricao': 'Registro de Nascimento\n\nDOCUMENTAÇÃO NECESSÁRIA:\n• Declaração de Nascido Vivo (DNV-papel amarelo dado pelo hospital em que a criança nasceu);\n• RG e CPF ORIGINAL dos pais;\n• Certidão de casamento dos pais, caso sejam casados;\n\nCaso não tenha RG, poderá apresentar os seguintes documentos:\n• Reservista;\n• CTPS física;\n• CNH, acompanhada de certidão de nascimento ou casamento, para que possamos verificar a NATURALIDADE;\n\nServiço GRATUITO\nPRAZO DE ENTREGA: Emitimos a certidão na hora\nSOLICITAÇÕES: Apenas em nosso balcão de atendimento presencialmente.\n\nATENÇÃO: Para registrar uma pessoa no Cartório Porta Larga, é preciso que ela tenha nascido nos bairros de COMPORTAS, CAJUEIRO SECO, PRAZERES, JARDIM JORDÃO, GUARARAPES, PIEDADE, CANDEIAS, BARRA DE JANGADA, MARCOS FREIRE ou MURIBECA, ou que um dos genitores resida em um desses bairros.', 'duracao_minutos': 30, 'preco': None, 'ativo': True, 'ordem': 1},
        {'nome': 'Casamento Civil', 'resumo': 'Habilitação e celebração de casamento civil com plena validade jurídica.', 'descricao': 'Documentos necessários para casamento civil\n\nBRASILEIROS SOLTEIROS\n• Certidão de Nascimento ORIGINAL E ATUALIZADA COM NO MÁXIMO 90 DIAS DE EMISSÃO;\n• RG e CPF;\n• Comprovante de residência.\n\nBRASILEIROS DIVORCIADOS\n• Certidão de Casamento com Averbação de Divórcio ORIGINAL E ATUALIZADA COM NO MÁXIMO 90 DIAS DE EMISSÃO;\n• RG e CPF;\n• Comprovante de residência.\n\nBRASILEIROS VIÚVOS\n• Certidão de Casamento com Averbação do Óbito ORIGINAL E ATUALIZADA;\n• Certidão de ÓBITO do falecido(a);\n• RG e CPF;\n• Comprovante de residência.\n\nATENÇÃO: Pelo menos 1 dos nubentes precisa residir nos bairros: COMPORTAS, CAJUEIRO SECO, PRAZERES, JARDIM JORDÃO, GUARARAPES, PIEDADE, CANDEIAS, BARRA DE JANGADA, MARCOS FREIRE e MURIBECA.', 'duracao_minutos': 60, 'preco': None, 'ativo': True, 'ordem': 2},
        {'nome': 'Casamento Religioso com Civil', 'resumo': 'Casamento religioso com registro civil. Processo em 7 etapas com prazo de até 7 dias.', 'descricao': 'Documentos necessários para casamento civil\n\nBRASILEIROS SOLTEIROS\n• Certidão de Nascimento ORIGINAL E ATUALIZADA COM NO MÁXIMO 90 DIAS DE EMISSÃO;\n• RG e CPF;\n• Comprovante de residência.\n\nBRASILEIROS DIVORCIADOS\n• Certidão de Casamento com Averbação de Divórcio ORIGINAL E ATUALIZADA COM NO MÁXIMO 90 DIAS DE EMISSÃO;\n• RG e CPF;\n• Comprovante de residência.\n\nBRASILEIROS VIÚVOS\n• Certidão de Casamento com Averbação do Óbito ORIGINAL E ATUALIZADA;\n• Certidão de ÓBITO do falecido(a);\n• RG e CPF;\n• Comprovante de residência.', 'duracao_minutos': 60, 'preco': None, 'ativo': False, 'ordem': 3},
        {'nome': 'Conversão de União Estável em Casamento', 'resumo': 'Converta sua união estável em casamento civil com segurança jurídica.', 'descricao': 'Documentos necessários para casamento civil\n\nBRASILEIROS SOLTEIROS\n• Certidão de Nascimento ORIGINAL E ATUALIZADA COM NO MÁXIMO 90 DIAS DE EMISSÃO;\n• RG e CPF;\n• Comprovante de residência.\n\nATENÇÃO: Pelo menos 1 dos nubentes precisa residir nos bairros atendidos pelo cartório.', 'duracao_minutos': 60, 'preco': None, 'ativo': False, 'ordem': 4},
        {'nome': 'Óbitos', 'resumo': 'Registro de óbito e emissão de certidão com atendimento ágil.', 'descricao': 'Registro de Óbito\n\nDOCUMENTAÇÃO NECESSÁRIA:\n• RG e CPF do declarante (podendo ser CNH);\n• Atestado de óbito;\n• RG e CPF e/ou certidão de nascimento do falecido.', 'duracao_minutos': 30, 'preco': None, 'ativo': True, 'ordem': 5},
        {'nome': '2º Vias DE CERTIDÕES', 'resumo': 'Emissão de segunda via de certidões de nascimento, casamento e óbito.', 'descricao': 'Emissão de segunda via de certidões diversas de nascimento, casamento e óbito lavrados neste cartório.', 'duracao_minutos': 20, 'preco': None, 'ativo': True, 'ordem': 6},
        {'nome': 'Reconhecimento de firmas', 'resumo': 'Autenticação de assinatura por autenticidade ou semelhança. Atendimento rápido.', 'descricao': 'Reconhecimento de firma por autenticidade ou semelhança em documentos diversos.', 'duracao_minutos': 15, 'preco': 15.00, 'ativo': True, 'ordem': 7},
        {'nome': 'Autenticação de documentos', 'resumo': 'Autenticação de cópias de documentos com fé pública cartorária.', 'descricao': 'Autenticação de cópias de documentos originais com fé pública cartorária.', 'duracao_minutos': 15, 'preco': 15.00, 'ativo': True, 'ordem': 8},
        {'nome': 'Apostila de Haia', 'resumo': 'Valide seus documentos para uso internacional com o apostilamento.', 'descricao': 'Apostilamento de documentos para validade internacional conforme a Convenção de Haia.', 'duracao_minutos': 30, 'preco': None, 'ativo': True, 'ordem': 9},
        {'nome': 'Retificações', 'resumo': 'Correção de erros em registros civis. Mudança de prenome, sobrenome, gênero e nome de recém-nascido diretamente no cartório.', 'descricao': 'Retificação de registros civis.', 'duracao_minutos': 30, 'preco': None, 'ativo': True, 'ordem': 10},
        {'nome': 'Retificação — Mudança de Prenome', 'resumo': 'Alteração do primeiro nome diretamente no cartório, sem precisar ir à Justiça. Feita uma única vez.', 'descricao': 'REQUISITOS E DOCUMENTOS NECESSÁRIOS PARA A MUDANÇA DE PRENOME:\n• Pedido pessoalmente ou mediante procurador;\n• Alteração em cartório só pode ser feita uma única vez;\n• Identidade, CPF, Passaporte (se tiver), Título de eleitor;\n• Certidão de nascimento atualizada;\n• Comprovante de residência.', 'duracao_minutos': 30, 'preco': None, 'ativo': False, 'ordem': 11},
        {'nome': 'Retificação — Mudança de Sobrenome', 'resumo': 'Inclusão ou exclusão de sobrenomes familiares diretamente no cartório, sem processo judicial.', 'descricao': 'REQUISITOS E DOCUMENTOS NECESSÁRIOS PARA A MUDANÇA DE SOBRENOME:\n• Identidade e CPF;\n• Certidão de nascimento e de casamento se for o caso;\n• Documentos que comprovem a relação de parentesco/filiação.', 'duracao_minutos': 30, 'preco': None, 'ativo': False, 'ordem': 12},
        {'nome': 'Retificação — Mudança de Prenome e Gênero', 'resumo': 'Adequação do prenome e gênero à identidade autopercebida para pessoas transgênero.', 'descricao': 'REQUISITOS E DOCUMENTOS NECESSÁRIOS PARA A MUDANÇA DE PRENOME E GÊNERO:\n• Pessoa maior de 18 anos;\n• Não pode ser realizado por procurador;\n• Identidade, CPF, Passaporte (se tiver), Título de eleitor;\n• Certidão de nascimento atualizada;\n• Comprovante de residência;\n• Certidões dos distribuidores cível e criminal dos últimos 5 anos.', 'duracao_minutos': 30, 'preco': None, 'ativo': False, 'ordem': 13},
        {'nome': 'Retificação — Alteração de Nome de Recém-Nascido', 'resumo': 'Alteração do nome do recém-nascido em até 15 dias após o registro de nascimento.', 'descricao': 'Em até 15 dias após o registro do nascimento, qualquer dos genitores poderá apresentar oposição fundamentada ao prenome e sobrenomes indicados pelo declarante.\n\nSe houver manifestação consensual dos genitores, será realizado o procedimento de retificação do registro diretamente no cartório.', 'duracao_minutos': 30, 'preco': None, 'ativo': False, 'ordem': 14},
        {'nome': 'Restaurações', 'resumo': 'Restauração de registros danificados ou extraviados no cartório.', 'descricao': 'Restauração de registros danificados ou extraviados no cartório.', 'duracao_minutos': 45, 'preco': None, 'ativo': True, 'ordem': 15},
        {'nome': 'Reconhecimento de Paternidade', 'resumo': 'Registro voluntário de paternidade com validade jurídica imediata.', 'descricao': 'Registro e reconhecimento voluntário de paternidade com validade jurídica imediata.', 'duracao_minutos': 30, 'preco': None, 'ativo': True, 'ordem': 16},
        {'nome': 'Comunicado de venda de veículo - Detran', 'resumo': 'Comunicado de venda de veículo ao Detran para transferência de responsabilidade.', 'descricao': 'Comunicado de venda de veículo ao Detran para transferência de responsabilidade ao novo proprietário.', 'duracao_minutos': 20, 'preco': None, 'ativo': True, 'ordem': 17},
    ]
    criados = 0
    for s in servicos:
        obj, created = Servico.objects.get_or_create(nome=s['nome'], defaults=s)
        if created:
            criados += 1
    print(f'  ✓ {criados} serviços criados ({Servico.objects.count()} total)')


def criar_horarios():
    horarios = []
    for dia in range(5):
        horarios.append({'dia_semana': dia, 'hora_inicio': '08:00', 'hora_fim': '12:00'})
        horarios.append({'dia_semana': dia, 'hora_inicio': '14:00', 'hora_fim': '16:00'})
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

    print('\n=== Tudo pronto! ===')
    print('\nPara iniciar o servidor:')
    print('  python manage.py runserver')
    print('\nAcesse:')
    print('  Site:        http://localhost:8000')
    print('  Admin:       http://localhost:8000/admin  (admin / admin123)')
    print('  API:         http://localhost:8000/api/')
    print()