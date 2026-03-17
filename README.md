<<<<<<< HEAD
# Cartório Porta Larga — Sistema Web Django

Site institucional com sistema de agendamento online, painel admin, login de clientes e API REST.

---

## Estrutura do projeto

```
cartorio_porta_larga/
├── cartorio/               # Configurações Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── agendamento/            # App de agendamentos
│   ├── models.py           # Agendamento, Servico, HorarioDisponivel
│   ├── views.py
│   ├── forms.py
│   ├── admin.py
│   └── utils.py            # Envio de e-mail
├── accounts/               # App de usuários/login
│   ├── models.py           # Perfil (CPF, telefone)
│   ├── views.py
│   ├── forms.py
│   └── admin.py
├── api/                    # API REST (Django REST Framework)
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── templates/
│   ├── base/               # base.html, home, sobre, serviços...
│   ├── agendamento/        # novo, meus, detalhe, cancelar, e-mails
│   └── accounts/           # login, cadastro, perfil
├── static/
│   ├── css/main.css
│   └── js/main.js
├── manage.py
├── requirements.txt
└── setup_inicial.py        # Script de setup com dados de exemplo
```

---

## Instalação e execução

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Rodar o setup inicial (migrations + dados de exemplo)

```bash
python setup_inicial.py
```

Isso irá:
- Aplicar todas as migrations
- Criar os serviços do cartório
- Criar os horários disponíveis (seg–sex)
- Criar superusuário: `admin` / `admin123`
- Criar cliente de teste: `cliente@teste.com` / `cliente123`

### 3. Iniciar o servidor

```bash
python manage.py runserver
```

---

## Acessos

| URL | Descrição |
|-----|-----------|
| http://localhost:8000 | Site público |
| http://localhost:8000/admin | Painel administrativo |
| http://localhost:8000/accounts/cadastro | Criar conta de cliente |
| http://localhost:8000/agendamento/novo | Fazer agendamento |
| http://localhost:8000/api/ | API REST (browsable) |

---

## API REST

### Autenticação

```bash
# Obter token
curl -X POST http://localhost:8000/api/auth/token/ \
  -d "username=cliente@teste.com&password=cliente123"
```

### Endpoints

| Método | URL | Descrição |
|--------|-----|-----------|
| GET | /api/servicos/ | Lista serviços (público) |
| GET | /api/agendamentos/ | Lista agendamentos do usuário |
| POST | /api/agendamentos/ | Criar agendamento |
| GET | /api/agendamentos/{id}/ | Detalhe do agendamento |
| POST | /api/agendamentos/{id}/cancelar/ | Cancelar agendamento |
| GET | /api/agendamentos/proximos/ | Próximos agendamentos |
| GET | /api/perfil/ | Dados do usuário logado |

### Exemplo de criação de agendamento via API

```bash
curl -X POST http://localhost:8000/api/agendamentos/ \
  -H "Authorization: Token SEU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"servico": 1, "data": "2025-04-10", "hora": "10:00", "observacoes": ""}'
```

---

## Configurar e-mail

No arquivo `cartorio/settings.py`, configure suas credenciais SMTP:

```python
EMAIL_HOST_USER = 'seuemail@gmail.com'
EMAIL_HOST_PASSWORD = 'sua_senha_de_app'  # Senha de app do Google
```

> Para usar o Gmail, crie uma **senha de aplicativo** em:
> https://myaccount.google.com/apppasswords

Para **desenvolvimento** (ver e-mails no terminal), use:

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

---

## Painel Admin

O admin (`/admin`) permite ao cartório:
- Gerenciar agendamentos (confirmar, cancelar, marcar como concluído)
- Cadastrar e editar serviços
- Gerenciar horários disponíveis
- Ver e editar clientes

---

## Próximos passos sugeridos

- [ ] Integrar Google Calendar para sincronizar agendamentos
- [ ] Adicionar integração com WhatsApp (Twilio ou Evolution API)
- [ ] Página de pagamento online (Pagar.me, Stripe)
- [ ] Dashboard com gráficos para o admin
- [ ] Deploy em produção (Heroku, Railway, VPS)
- [ ] Trocar SQLite por PostgreSQL em produção
=======
# Cartorio-Porta-Larga
Desenvolvimento web para agendamentos e informações do cartorio de Porta Larga
>>>>>>> 0f1a75fcf23d494dcf980f5f33fed0d2fc34a757
