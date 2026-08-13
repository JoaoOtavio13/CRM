# Vendas CRM

Sistema de gestão comercial e clientes para empresas, desenvolvido em Django com foco em cadastro de clientes, produtos, vendas e controle de estoque.

## Visão geral

Este projeto foi pensado para facilitar o acompanhamento de operações comerciais em uma empresa, incluindo:

- cadastro de usuários e perfis
- gestão de empresas e administradores
- cadastro de produtos por categoria
- controle de estoque
- registro de clientes
- criação e acompanhamento de vendas
- autenticação por JWT para API
- envio de e-mails

## Stack tecnológica

- Python 3.12
- Django 6.0.7
- Django REST Framework
- Simple JWT
- SQLite (ambiente local/default)
- Docker / Docker Compose
- HTML + templates do Django

## Estrutura principal

- `accounts/` — autenticação, perfis, empresas e usuários
- `produtos/` — categorias, produtos e controle de estoque
- `vendas/` — clientes, vendas, itens e cálculo de totais
- `core/` — páginas iniciais e dashboard
- `envia_email/` — integração de envio de e-mails
- `main/` — configuração principal do projeto
- `media/` — arquivos enviados pelo usuário

## Pré-requisitos

Antes de executar, certifique-se de ter instalado:

- Python 3.12+
- pip
- virtualenv (opcional, mas recomendado)
- Docker e Docker Compose (opcional, para execução em container)

## Configuração inicial

### 1) Clone o projeto

```bash
git clone <url-do-repositorio>
cd Vendas_CRM
```

### 2) Crie e ative um ambiente virtual

No Windows (PowerShell):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

No Linux/macOS:

```bash
python -m venv venv
source venv/bin/activate
```

### 3) Instale as dependências

```bash
pip install -r requirements.txt
```

### 4) Configure o arquivo de ambiente

Crie um arquivo `.env` na raiz do projeto com as variáveis abaixo:

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha-de-app
```

> Ajuste os valores de acordo com o provedor de e-mail que estiver usando. Se estiver utilizando Gmail, normalmente é necessário gerar uma senha de app.

## Execução local

### 1) Aplicar as migrações

```bash
python manage.py migrate
```

### 2) Crie um superusuário

```bash
python manage.py createsuperuser
```

### 3) Inicie o servidor

```bash
python manage.py runserver
```

A aplicação ficará disponível em:

```text
http://127.0.0.1:8000/
```

## Execução via Docker

O projeto já inclui um `Dockerfile` e um `docker-compose.yml` com configuração para subir a aplicação em container.

### 1) Subir o ambiente

```bash
docker compose up --build
```

### 2) Acesso

```text
http://localhost:8000/
```

### 3) Parar os containers

```bash
docker compose down
```

## Rotas principais

Algumas rotas importantes do sistema:

- `/admin/` — painel administrativo do Django
- `/accounts/login/` — login
- `/accounts/register/` — cadastro de usuário
- `/accounts/perfil/` — perfil do usuário
- `/produtos/` — gerenciamento de produtos
- `/vendas/` — gestão de vendas
- `/api/` — endpoints da API REST

## Funcionalidades de negócio

### Gestão de contas e empresas

- cadastro de empresa
- associação de perfis
- promoção de usuários para administradores

### Produtos

- criação de categorias
- cadastro de produtos com imagem, preço e estoque
- validação de quantidade negativa em estoque
- manutenção de preço e atualização de dados

### Vendas

- registro de clientes
- criação de vendas com números automáticos por usuário
- cálculo automático de total da venda
- controle de estoque ao adicionar, atualizar ou remover itens
- integração entre venda e produto

### API

A API do projeto inclui endpoints para autenticação e gestão de usuários, produtos e vendas, usando autenticação JWT.

## Boas práticas

- mantenha o ambiente virtual ativo durante o desenvolvimento
- nunca exponha `.env` em repositórios públicos
- execute `python manage.py migrate` sempre que houver alterações no banco
- use o painel administrativo para validar dados iniciais

## Troubleshooting

### Erro de dependências

Se ocorrer algum problema ao instalar pacotes:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Migrações com erro

```bash
python manage.py makemigrations
python manage.py migrate
```

### Problemas com email

Verifique se:

- as variáveis `EMAIL_HOST_USER` e `EMAIL_HOST_PASSWORD` estão corretas
- o provedor aceita SMTP
- a senha é uma senha de app

## Observação

Este projeto foi preparado para uso local e com Docker. O arquivo `.env` deve ser mantido localmente e nunca compartilhado publicamente.

## Licença

Este projeto não especifica uma licença em arquivo próprio. Consulte o responsável pela organização do repositório antes de redistribuir o código.
