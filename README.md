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

O projeto inclui um arquivo **`.env.example`** na raiz, que serve como **modelo das variáveis de ambiente** necessárias para a aplicação. Veja abaixo o que ele é, para que serve e como utilizá-lo.

#### O que é o `.env.example`?

É um arquivo de exemplo que lista todas as variáveis que o projeto espera no ambiente, acompanhadas de *placeholders* (valores fictícios) e comentários explicativos:

```env
# --- Django core ---
SECRET_KEY=change-me-a-secure-random-string
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# --- Email (SMTP) ---
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@example.com
EMAIL_HOST_PASSWORD=tu-contraseña-de-app
```

#### Para que serve?

- **Documenta as configurações esperadas**: mostra a quem for configurar o projeto exatamente quais variáveis existem (segredos do Django, modo de depuração, hosts permitidos e credenciais de e-mail) e seus significados.
- **Serve de ponto de partida**: ao invés de digitar tudo do zero, você copia este arquivo e apenas preenche os valores reais.
- **É seguro de versionar**: contém apenas valores de exemplo, sem dados reais, então pode ficar no repositório. Já o `.env`, com dados reais, **nunca** deve ser versionado.

#### Como utilizar?

1. **Copie** o `.env.example` para um arquivo chamado `.env` na raiz do projeto:

   No Windows (PowerShell):

   ```powershell
   copy .env.example .env
   ```

   No Linux/macOS:

   ```bash
   cp .env.example .env
   ```

2. **Edite** o `.env` preenchendo cada variável com seus valores reais:

   - `SECRET_KEY` — chave secreta do Django; use um valor aleatório seguro (ex.: gere em <https://djecrety.herokuapp.com/>).
   - `DEBUG` — `True` apenas em desenvolvimento; em produção use **sempre** `False`.
   - `ALLOWED_HOSTS` — hosts permitidos, separados por vírgula e sem espaços (ex.: `localhost,127.0.0.1`).
   - `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USE_TLS`, `EMAIL_HOST_USER` e `EMAIL_HOST_PASSWORD` — credenciais SMTP do provedor de e-mail (ex.: Gmail, usando uma senha de app).

   > Ajuste os valores de acordo com o provedor de e-mail que estiver usando. Se estiver utilizando Gmail, normalmente é necessário gerar uma senha de app.

3. **Mantenha o `.env` fora do versionamento**: ele é ignorado pelo git e pelo Docker e deve ficar somente no ambiente local, **nunca** compartilhado publicamente.

> **Dica:** se precisar usar múltiplos ambientes (local, staging, produção), crie um `.env` específico para cada um, baseado sempre no `.env.example`.

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

O projeto já inclui os arquivos de Docker versionados no repositório:

- `Dockerfile` — imagem da aplicação (Python 3.12)
- `docker-compose.yml` — orquestração do ambiente
- `.dockerignore` — arquivos excluídos do build da imagem

> **Importante:** o `docker-compose.yml` usa `env_file: .env`. Antes de subir o ambiente, crie o arquivo `.env` na raiz do projeto conforme a seção [Configuração inicial](#configuração-inicial) — caso contrário o compose falhará por variáveis de ambiente ausentes.

### 1) Subir o ambiente

```bash
docker compose up --build
```

O comando aplica as migrações do banco e sobe o servidor de desenvolvimento, montando a pasta do projeto em `/app` e expondo a porta `8000`.

### 2) Acesso

```text
http://localhost:8000/
```

### 3) Parar os containers

```bash
docker compose down
```

> O arquivo `.env` **não é versionado** e fica apenas no ambiente local (ele é ignorado pelo git e pelo Docker).

## Execução dos testes

Para rodar a suíte de testes unitários do projeto (usa um banco em memória):

```bash
python manage.py test
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
