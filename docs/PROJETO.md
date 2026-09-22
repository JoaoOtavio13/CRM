# 📘 CRM de Vendas — Documentação do Projeto

> **Projeto:** Vendas_CRM
> **Framework:** Django 6.0.7 + Django REST Framework 3.17.1
> **Autenticação API:** JWT (djangorestframework-simplejwt 5.5.1)
> **Frontend:** Templates Django + Bootstrap (via herança de templates)
> **Projeto acadêmico** — Trilha de Backend
> **Objetivo:** Sistema CRM para empresas de varejo, com gestão de produtos, clientes, vendas, estoque e faturamento.

---

## ⚙️ 1. Criação do Ambiente Virtual

O projeto usa Python **3.12.10** (definido em `.python-version` e no `Dockerfile` baseado em `python:3.12-slim`). Na trilha, o passo inicial é:

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
pip install -r requirements.txt
```

**Dependências principais (`requirements.txt`):**

| Pacote | Versão | Uso |
|--------|--------|-----|
| Django | 6.0.7 | Framework web |
| djangorestframework | 3.17.1 | API REST |
| djangorestframework-simplejwt | 5.5.1 | Tokens JWT |
| python-decouple | 3.8 | Variáveis de ambiente |
| dj-database-url | 3.1.2 | Conexão BD via URL |
| cloudinary | 1.46.2 | Armazenamento de imagens |
| psycopg[binary] | 3.3.5 | PostgreSQL |
| gunicorn | 26.2.0 | Servidor WSGI (produção) |
| whitenoise | 6.12.0 | Arquivos estáticos |

| **Parte 4.1 ✅** | Ambiente virtual criado com `venv`, dependências versionadas em `requirements.txt` |

---

## 📁 2. Estrutura do Projeto e Apps

```
Vendas_CRM/
├── main/                  # Projeto Django (settings, urls, wsgi)
├── accounts/              # Usuários, empresas, perfis, admins
├── produtos/              # Catálogo de produtos e categorias
├── vendas/                # Vendas, itens de venda, clientes
├── core/                  # Páginas principais (index, about, dashboard)
├── envia_email/           # Teste de envio de e-mail (SMTP)
├── render.yaml
├── Dockerfile
├── build.sh
└── manage.py
```

| App | Responsabilidade |
|-----|------------------|
| `accounts` | Autenticação, registro, perfil, empresa, admin |
| `produtos` | Produtos, categorias, estoque |
| `vendas` | Vendas, itens de venda, clientes, faturamento |
| `core` | Páginas iniciais e dashboard |
| `envia_email` | Teste/debug de envio de e-mails |

| **Parte 4.2 ✅** | Projeto `main` + apps `accounts`, `produtos`, `vendas`, `core`, `envia_email` |

---

## 🔗 3. URLs — Rotas do Projeto

Todas as URLs são incluídas em `main/urls.py`:

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('produtos/', include('produtos.urls')),
    path('vendas/', include('vendas.urls')),
    path('api/', include('accounts.api_urls')),
    path('api/', include('produtos.api_urls')),
    path('api/', include('vendas.api_urls')),
    path('email/', include('envia_email.urls')),
]
```

### 3.1 URLs HTML (`core/urls.py`)

| Rota | View | Tipo | Acesso |
|------|------|------|--------|
| `/` | `index` | FBV | Público |
| `/about/` | `about` | FBV | Público |
| `/dashboard/` | `DashboardView` | CBV | Login + Admin |

### 3.2 URLs de Contas (`accounts/urls.py`)

| Rota | View | Tipo | Acesso |
|------|------|------|--------|
| `/accounts/login/` | `login_view` | FBV | Público |
| `/accounts/logout/` | `logout_view` | FBV | Login |
| `/accounts/register/` | `register` | FBV | Público |
| `/accounts/perfil/` | `perfil` | FBV | Login |
| `/accounts/perfil/editar/` | `editar_perfil` | FBV | Login |
| `/accounts/perfil/deletar/` | `deletar_perfil` | FBV | Login |
| `/accounts/redefinir-senha/` | `redefinir_senha` | FBV | Público |
| `/accounts/redefinir-senha/<uidb64>/<token>/` | `nova_senha` | FBV | Público |
| `/accounts/empresas/` | `empresa_list` | FBV | Login + Admin |
| `/accounts/empresas/nova/` | `empresa_create` | FBV | Login + Admin |
| `/accounts/empresas/<pk>/editar/` | `empresa_update` | FBV | Login + Admin |
| `/accounts/empresas/<pk>/excluir/` | `empresa_delete` | FBV | Login + Admin |
| `/accounts/promover-admin/` | `promover_admin` | FBV | Login |

| **Parte 4.3 ✅** | URLs em `main/urls.py` via `include()`, `path()`, converters e named URLs. |

---

## 🗄️ 4. Models — Definições de Dados

### 4.1 `accounts/models.py`

- `Empresa`: nome, cnpj (unique), endereco, telefone, email
- `Perfil`: user (OneToOne), nome, telefone, cargo, cpf, imagem, empresa (FK)
- `Admin`: user (OneToOne), empresa (FK) — constraint `unique_admin_per_empresa`

### 4.2 `produtos/models.py`

- `Categoria`: nome, descricao
- `Produto`: usuario (FK), nome, descricao, preco, estoque, imagem, categoria (FK), timestamps
  - Métodos: `baixar_estoque()`, `repor_estoque()`, `clean()` (estoque >= 0)

### 4.3 `vendas/models.py`

- `Cliente`: usuario (FK), nome, email, telefone, endereco
- `Venda`: usuario (FK), numero (auto), data_venda (auto), total (auto), cliente (FK)
  - Constraint `unique_venda_numero_por_usuario`; métodos `atualizar_total()`, `save()` (autonumeração), `delete()` (restaura estoque)
- `ItemVenda`: venda (FK), produto (FK), quantidade, subtotal (auto)
  - `save()` com `transaction.atomic()` + `select_for_update()` ajusta estoque; `delete()` devolve estoque

| **Parte 4.4 ✅** | Models com ForeignKey, OneToOne, UniqueConstraint, lógica de estoque transacional. |

---

## 👁️ 5. Views — FBV e CBV

- **CBV:** `core/views.py` → `DashboardView(LoginRequiredMixin, TemplateView)` com `dispatch()` customizado para admin.
- **FBV:** todo o restante, usando `@login_required` (sessão) e `@admin_required` (custom em `accounts/decorators.py`).
- **`@admin_required`:** redireciona não autenticados para login; permite superuser ou `Admin.objects.filter(user=...)`; senão, erro + redirect para index.

| **Parte 4.5 ✅** | CBV (`TemplateView`) para dashboard; FBV + decoradores para CRUD. |

---

## 🎨 6. Templates

- Backend Django templates (`render()`)
- Templates resolvidos via `APP_DIRS=True` (um `templates/` por app)
- Context processor `accounts.context_processors.is_admin_context` expõe `is_admin` a todos os templates (menus de admin)

| **Parte 4.6 ✅** | Herança, APP_DIRS e context processor customizado. |

---

## 📋 7. Forms

- **`accounts/forms.py`**: `buscar_ou_criar_empresa()` (helper, CNPJ em hash), `LoginForm`, `RegisterForm` (herda `UserCreationForm` + campos de Perfil/Empresa), `PerfilForm`, `EmpresaForm`, `AdminForm`
- **`produtos/forms.py`**: `ProdutoForm` (ModelForm)
- **`vendas/forms.py`**: `VendaForm` (filtra cliente), `ItemVendaForm` (filtra produto, valida estoque), `ItemVendaFormSet` (`inlineformset_factory`), `ClienteForm`

| **Parte 4.7 ✅** | ModelForms, UserCreationForm, inlineformset_factory e validações customizadas. |

---

## 🏗️ 8. CBV vs FBV — Comparação

| Critério | CBV | FBV |
|----------|-----|-----|
| Onde | `core/views.py` → `DashboardView` | Apps `accounts`, `produtos`, `vendas` |
| Decorator | `LoginRequiredMixin` (classe) | `@login_required` |
| Herança | `TemplateView`, `LoginRequiredMixin` | Nenhuma |
| Acesso admin | `dispatch()` customizado | `@admin_required` externo |
| Melhor uso | Páginas estáticas simples | Formulários com POST/GET |

| **Parte 4.8 ✅** | Projeto usa FBV como padrão (CRUD) e CBV (`TemplateView`) apenas para o dashboard. |

---

## 💼 9. Projeto CRM — Requisitos (Parte 4)

| Requisito | Implementação |
|-----------|---------------|
| Cadastrar/remover/editar produtos | ✅ `produto_create`, `produto_update_view`, `produto_delete` (FBV + `@admin_required`) |
| Definir quantidade em estoque | ✅ Campo `estoque` em `Produto` (validado `>= 0`) |
| Atualizar estoque em venda | ✅ `ItemVenda.save()` (`transaction.atomic` + `select_for_update`) → `produto.baixar_estoque(qtd)` |
| Atualizar faturamento total | ✅ `Venda.atualizar_total()` via `Sum('itens__subtotal')`; campo `total` (DecimalField) |

> 💡 O faturamento no projeto é **por usuário**, não global por empresa. Para obter faturamento por empresa, filtrar por `Perfil.empresa`.

| **Parte 4.9 ✅** | MVP CRM: CRUD de produtos com estoque transacional e faturamento. |

---

# 🌐 Parte 5 — Django REST Framework

## 🔍 1. Requests e Responses

- `request.data` (parsed JSON/Form) substitui `request.POST`/`request.body`
- `Response()` serializa dados Python e negocia media type (JSON por padrão)

| **Parte 5.1 ✅** | Uso de `request.data` e `Response` em todas as views API. |

---

## 📡 2. API REST

Endpoints sob `/api/`:

```
POST /api/register/   → cria conta
POST /api/login/      → retorna tokens JWT
GET  /api/produtos/   → lista produtos (autenticado)
GET  /api/faturamento/ → faturamento do dono (autenticado + admin)
GET  /api/vendas/     → lista vendas (autenticado)
```

| **Parte 5.2 ✅** | Estrutura REST sob `/api/` com verbos CRUD. |

---

## 📦 3. Model Serializers

### `accounts/serializers.py`

- `UserSerializer`: id, username, email, first_name, last_name
- `RegisterSerializer`: id, username, email, password (write_only), nome, empresa_nome → `create()` faz `User.objects.create_user` + `Perfil.objects.create`

### `produtos/serializers.py`

- `ProdutoSerializer`: id, nome, descricao, preco, estoque, imagem, timestamps — `validate_estoque()` (>=0), `validate_preco()` (>0)

### `vendas/serializers.py`

- `ItemVendaSerializer`: produto (ProdutoSerializer read_only) + produto_id (write_only PrimaryKeyRelatedField)
- `VendaSerializer`: numero, usuario, data_venda, total, cliente, cliente_nome (source), itens (nested read_only)

| **Parte 5.3 ✅** | Serializers com validações field-level e nested serialization. |

---

## 🖐️ 4. APIView e @api_view

- **FBV + `@api_view`** (`accounts/api_views.py`): `register_api` (POST, `AllowAny`), `login_api` (POST, `AllowAny`) — emitem JWT
- **CBV + `APIView`** (`vendas/api_views.py`): `VendaListAPIView` (GET, `IsAuthenticated`), `FaturamentoAPIView` (GET, `IsAuthenticated + IsEmpresaAdmin`)

| **Parte 5.4 ✅** | Mix de `@api_view` (auth) e `APIView` (relatórios). |

---

## 🎯 5. ViewSets e Routers

`produtos/api_urls.py` registra `ProdutoViewSet` via `DefaultRouter`:

```python
router = DefaultRouter()
router.register(r'produtos', ProdutoViewSet, basename='produto')
```

`ProdutoViewSet` (ModelViewSet):
- `permission_classes = [IsAuthenticated]`
- `get_queryset()`: apenas produtos de `request.user`
- `perform_create()`: salva com `usuario=request.user`

Rotas geradas automaticamente:

| Verbo | Rota |
|-------|------|
| GET | `/api/produtos/` (list) |
| POST | `/api/produtos/` (create) |
| GET | `/api/produtos/<pk>/` (retrieve) |
| PUT | `/api/produtos/<pk>/` (update) |
| DELETE | `/api/produtos/<pk>/` (destroy) |

| **Parte 5.5 ✅** | ViewSet + Router geram CRUD completo para produtos. |

---

## ✏️ 6. CRUD com POST/GET/PUT/DELETE

| Recurso | Endpoints | Métodos | Auth |
|---------|-----------|---------|------|
| Conta | `/api/register/`, `/api/login/`, `/api/token/refresh/` | POST | Público (`AllowAny`) |
| Produtos | `/api/produtos/`, `/api/produtos/<pk>/` | GET/POST/PUT/DELETE | `IsAuthenticated` |
| Vendas | `/api/vendas/` | GET | `IsAuthenticated` |
| Faturamento | `/api/faturamento/` | GET | `IsAuthenticated + IsEmpresaAdmin` |

| **Parte 5.6 ✅** | CRUD completo em produtos (ViewSet); listagens em vendas/faturamento (APIView). |

---

## 🔐 7. Autenticação

| Tipo | Onde | Implementação |
|------|------|---------------|
| Sessão (HTML) | `/accounts/login/` | Django auth — cookies de sessão |
| JWT (API) | `/api/login/` | `RefreshToken.for_user()` → access + refresh; `/api/token/refresh/` |
| OAuth2 | — | Não implementado |

Tokens: access = 60 min; refresh = 1 dia (`SIMPLE_JWT` em `settings.py`).

| **Parte 5.7 ✅** | Sessão (HTML) + JWT (API). |

---

## 🔑 8. Permissões (DRF)

| Permissão | Onde | Quem permite |
|-----------|------|--------------|
| `AllowAny` | `accounts/api_views.py` | Register/login |
| `IsAuthenticated` | `ProdutoViewSet`, `VendaListAPIView` | Usuário logado |
| `IsEmpresaAdmin` (custom) | `vendas/api_views.py` | Dono da empresa (perfil → empresa → Admin) |

`IsEmpresaAdmin` (`accounts/permissions.py`): superuser ou `Admin.objects.filter(user, empresa_id=perfil.empresa_id)`.

| **Parte 5.8 ✅** | Permissões: AllowAny → IsAuthenticated → IsEmpresaAdmin. |

---

## 💼 9. Projeto CRM — API (Parte 5)

| Requisito | Implementação |
|-----------|---------------|
| Criar conta e login | ✅ `POST /api/register/` + `POST /api/login/` (JWT) |
| Listar/cadastrar/editar/remover produtos (logado) | ✅ `ProdutoViewSet` (CRUD completo, `IsAuthenticated`) |
| Detalhes do produto + estoque | ✅ `ProdutoSerializer` expõe `estoque`; detalhe em `GET /api/produtos/<pk>/` |
| Faturamento da empresa (dono) | ✅ `FaturamentoAPIView` com `IsEmpresaAdmin` |

| **Parte 5.9 ✅** | API CRM completa: auth JWT, CRUD de produtos e faturamento restrito ao dono. |

---

## 📝 Observações Finais

- **`variaveis_ambiente.py`**: script de debug (`print(os.environ)`) — não versionado, pode ser adicionado ao `.gitignore`.
- **`envia_email/views.py`**: hardcodeia e-mails — usado apenas para teste. Corrigido com `try/except` e logging para evitar 500.
- **Faturamento**: implementado **por usuário**. Para faturamento **por empresa**, alterar a query para filtrar por `Perfil.empresa`.
