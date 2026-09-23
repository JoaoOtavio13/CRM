# 📘 CRM de Vendas — Documentação do Projeto

> **Projeto:** Vendas_CRM  
> **Framework:** Django 6.0.7 + Django REST Framework 3.17.1  
> **API Auth:** JWT (djangorestframework-simplejwt 5.5.1)  
> **Docs API:** drf-spectacular 0.28.0 (OpenAPI 3.0 + Swagger UI)  
> **Frontend:** Templates Django + Bootstrap  
> **Tipo:** Projeto acadêmico — Trilha de Backend  
> **Objetivo:** CRM para empresas de varejo: produtos, clientes, vendas, estoque e faturamento.

---

## 📋 Visão Geral

Sistema completo de gestão comercial para PMEs de varejo:

- Autenticação: login/logout, registro, perfil com empresa
- Gestão de empresas/admins (dono controla produtos, vendas, faturamento)
- Catálogo de produtos (CRUD) com estoque e imagem
- Vendas com atualização automática de estoque e faturamento
- API REST com JWT + Swagger/OpenAPI
- Email: teste SMTP via `/email/`

| **Parte 0 ✅** | Visão geral do sistema — autenticação, produtos, vendas, faturamento, API, Swagger. |

---

## 🗂 Índice

| # | Seção |
|---|-------|
| 1 | Criação do Ambiente Virtual |
| 2 | Estrutura do Projeto e Apps |
| 3 | URLs — Rotas do Projeto |
| 4 | Models — Dados do Sistema |
| 5 | Views — CBV e FBV |
| 6 | Templates |
| 7 | Forms |
| 8 | CBV vs FBV |
| 9 | Projeto CRM — Requisitos Atendidos (Django) |
| 10 | DRF — Requests e Responses |
| 11 | DRF — API REST |
| 12 | DRF — Model Serializers |
| 13 | DRF — `@api_view` e `APIView` |
| 14 | DRF — ViewSets e Routers |
| 15 | DRF — CRUD (POST/GET/PUT/PATCH/DELETE) |
| 16 | Autenticação (Sessão + JWT) |
| 17 | Permissões (DRF) |
| 18 | Projeto CRM — Requisitos da API |
| 19 | Documentação da API (Swagger / OpenAPI) |
| 20 | Configuração de Ambiente e Deploy |
| 21 | Solução de Problemas (Troubleshooting) |
| 22 | Checklist Final de Entrega |
| 23 | Referência Rápida de Arquivos |


---
## ⚙️ 1. Criação do Ambiente Virtual

O projeto usa Python **3.12.10** (definido em `.python-version` e no Dockerfile).

### Passo a passo

```bash
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
```

### Dependências (requirements.txt)

| Pacote | Versão | Uso |
|--------|--------|-----|
| Django | 6.0.7 | Framework web principal |
| djangorestframework | 3.17.1 | API REST |
| djangorestframework-simplejwt | 5.5.1 | Tokens JWT para autenticação |
| drf-spectacular | 0.28.0 | Schema OpenAPI 3.0 + Swagger UI |
| python-decouple | 3.8 | Variáveis de ambiente (.env) |
| dj-database-url | 3.1.2 | Conexão DB via URL (PostgreSQL no Render) |
| cloudinary | 1.46.2 | Armazenamento de imagens (produção) |
| psycopg[binary] | 3.3.5 | Driver PostgreSQL |
| gunicorn | 26.2.0 | Servidor WSGI (produção) |
| whitenoise | 6.12.0 | Arquivos estáticos (produção) |
| Pillow | 12.3.0 | Manipulação de imagens |
| PyJWT | 2.13.0 | Tokens JWT |
| asgiref | 3.12.1 | Compatibilidade ASGI |
| sqlparse | 0.5.5 | Parser SQL |
| tzdata | 2026.3 | Fusos horários |

| **Parte 1 ✅** | Ambiente virtual com Python 3.12.10, dependências versionadas em requirements.txt. |

---

## 📁 2. Estrutura do Projeto e Apps

O projeto está organizado em apps Django independentes, cada um com responsabilidade única (domínio do negócio).

```text
Vendas_CRM/
├── main/                        # Configurações do projeto
│   ├── settings.py              # DB, templates, middleware, REST_FRAMEWORK, SIMPLE_JWT, e-mail
│   ├── urls.py                  # URL raiz (HTML + API + Swagger)
│   ├── storage_backends.py      # Backend de storage para Cloudinary
│   └── wsgi.py                  # Entrada WSGI (produção)
├── accounts/                    # Autenticação, perfis, empresas e admins
│   ├── models.py                # Empresa, Perfil, Admin
│   ├── views.py                 # Views HTML (login, register, perfil, empresas, admin)
│   ├── api_views.py             # register_api, login_api
│   ├── serializers.py           # UserSerializer, RegisterSerializer
│   ├── forms.py                 # LoginForm, RegisterForm, PerfilForm, EmpresaForm, AdminForm
│   ├── urls.py                  # Rotas HTML
│   ├── api_urls.py              # Rotas da API (register, login, token/refresh)
│   ├── permissions.py           # IsEmpresaAdmin
│   ├── decorators.py            # admin_required
│   └── context_processors.py    # is_admin_context
├── produtos/                    # Catálogo de produtos
│   ├── models.py                # Categoria, Produto (estoque)
│   ├── views.py                 # CRUD de produtos e categorias (HTML)
│   ├── api_views.py             # ProdutoViewSet (ModelViewSet)
│   ├── serializers.py           # ProdutoSerializer
│   ├── forms.py                 # ProdutoForm
│   ├── urls.py                  # Rotas HTML
│   └── api_urls.py              # Router da API de produtos
├── vendas/                      # Vendas, clientes e faturamento
│   ├── models.py                # Cliente, Venda, ItemVenda
│   ├── views.py                 # registrar_venda, vendas_list, faturamento, clientes
│   ├── api_views.py             # VendaListAPIView, FaturamentoAPIView
│   ├── serializers.py           # VendaSerializer, ItemVendaSerializer
│   ├── forms.py                 # VendaForm, ItemVendaForm, ItemVendaFormSet, ClienteForm
│   ├── urls.py                  # Rotas HTML
│   └── api_urls.py              # Rotas da API (vendas, faturamento)
├── core/                        # Páginas genéricas
│   ├── views.py                 # index, about, DashboardView (CBV)
│   └── urls.py                  # Rotas (/, /about/, /dashboard/)
├── envia_email/                 # Utilitário de teste de e-mail
│   ├── views.py                 # envia_email_view
│   └── urls.py                  # /email/
├── docs/PROJETO.md              # Esta documentação
├── manage.py                    # CLI do Django
├── requirements.txt             # Dependências fixadas
├── Dockerfile                   # Imagem Docker (python:3.12-slim)
├── build.sh                     # Script de build (Render)
├── render.yaml                  # Blueprint do Render
├── .env.example                 # Modelo das variáveis de ambiente
└── .gitignore
```

### Responsabilidade de cada app

| App | Domínio | Models | Views HTML | Views API |
|-----|---------|--------|-----------|-----------|
| `main` | Configuração | — | — | — |
| `accounts` | Usuários/empresas | `Empresa`, `Perfil`, `Admin` | login, register, perfil, empresas, promover_admin, redefinir senha | `register_api`, `login_api` |
| `produtos` | Catálogo | `Categoria`, `Produto` | CRUD produto + CRUD categoria | `ProdutoViewSet` |
| `vendas` | Vendas/faturamento | `Cliente`, `Venda`, `ItemVenda` | registrar_venda, list, detail, delete, faturamento, clientes | `VendaListAPIView`, `FaturamentoAPIView` |
| `core` | Páginas gerais | — | index, about, dashboard | — |
| `envia_email` | E-mail (debug) | — | envia_email_view | — |

| **Parte 2 ✅** | Arquitetura modular por domínio: cada app concentra models, views (HTML + API), forms e serializers do seu contexto. |

---

## 🔗 3. URLs — Rotas do Projeto

A URL raiz (`main/urls.py`) centraliza tudo e delega para os apps via `include()`:

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),                 # index, about, dashboard
    path('accounts/', include('accounts.urls')),    # login, perfil, empresas
    path('produtos/', include('produtos.urls')),    # produtos, categorias
    path('vendas/', include('vendas.urls')),        # vendas, clientes, faturamento
    # API REST
    path('api/', include('accounts.api_urls')),     # register, login, token/refresh
    path('api/', include('produtos.api_urls')),     # produtos (ViewSet)
    path('api/', include('vendas.api_urls')),       # vendas, faturamento
    # Swagger / OpenAPI
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='api-schema'), name='swagger-ui'),
    path('email/', include('envia_email.urls')),    # teste de e-mail
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### 3.1 Rotas HTML — `core/urls.py`

| Rota | View | Tipo | Acesso |
|------|------|------|--------|
| `/` | `index` | FBV | Público |
| `/about/` | `about` | FBV | Público |
| `/dashboard/` | `DashboardView` | CBV (TemplateView) | Login + Admin |

### 3.2 Rotas HTML — `accounts/urls.py`

| Rota | View | Acesso |
|------|------|--------|
| `/accounts/login/` | `login_view` | Público |
| `/accounts/logout/` | `logout_view` | Público |
| `/accounts/register/` | `register` | Público |
| `/accounts/perfil/` | `perfil` | Login |
| `/accounts/perfil/editar/` | `editar_perfil` | Login |
| `/accounts/perfil/deletar/` | `deletar_perfil` | Login |
| `/accounts/redefinir-senha/` | `redefinir_senha` | Público |
| `/accounts/redefinir-senha/<uidb64>/<token>/` | `nova_senha` | Público |
| `/accounts/empresas/` | `empresa_list` | Login |
| `/accounts/empresas/nova/` | `empresa_create` | Login |
| `/accounts/empresas/<int:pk>/editar/` | `empresa_update` | Login |
| `/accounts/empresas/<int:pk>/excluir/` | `empresa_delete` | Login |
| `/accounts/promover-admin/` | `promover_admin` | Login |

### 3.3 Rotas HTML — `produtos/urls.py`

| Rota | View | Acesso |
|------|------|--------|
| `/produtos/` | `produto_list_view` | Login |
| `/produtos/novo/` | `produto_create` | Login + Admin |
| `/produtos/<int:pk>/` | `produto_detail_view` | Login |
| `/produtos/<int:pk>/editar/` | `produto_update_view` | Login + Admin |
| `/produtos/<int:pk>/excluir/` | `produto_delete` | Login + Admin |
| `/produtos/categorias/` | `categoria_list_view` | Login |
| `/produtos/categorias/novo/` | `categoria_create` | Login + Admin |
| `/produtos/categorias/<int:pk>/editar/` | `categoria_update_view` | Login + Admin |
| `/produtos/categorias/<int:pk>/excluir/` | `categoria_delete` | Login + Admin |

### 3.4 Rotas HTML — `vendas/urls.py`

| Rota | View | Acesso |
|------|------|--------|
| `/vendas/` | `vendas_list` | Login |
| `/vendas/nova/` | `registrar_venda` | Login |
| `/vendas/<int:pk>/` | `venda_detail` | Login |
| `/vendas/<int:pk>/excluir/` | `venda_delete` | Login |
| `/vendas/faturamento/` | `faturamento` | Login + Admin |
| `/vendas/clientes/` | `listar_clientes` | Login |
| `/vendas/clientes/cadastro/` | `cadastro_cliente` | Login |
| `/vendas/clientes/<int:pk>/editar/` | `editar_cliente` | Login |
| `/vendas/clientes/<int:pk>/excluir/` | `deletar_cliente` | Login |

### 3.5 Rotas da API REST

| Grupo | Método e Rota | View | Acesso |
|-------|---------------|------|--------|
| Auth | `POST /api/register/` | `register_api` (`@api_view`) | Público |
| Auth | `POST /api/login/` | `login_api` (`@api_view`) | Público |
| Auth | `POST /api/token/refresh/` | `TokenRefreshView` (SimpleJWT) | Público |
| Produtos | `GET /api/produtos/` | `ProdutoViewSet.list` | Autenticado (JWT) |
| Produtos | `POST /api/produtos/` | `ProdutoViewSet.create` | Autenticado (JWT) |
| Produtos | `GET /api/produtos/<pk>/` | `ProdutoViewSet.retrieve` | Autenticado (JWT) |
| Produtos | `PUT/PATCH /api/produtos/<pk>/` | `ProdutoViewSet.update` | Autenticado (JWT) |
| Produtos | `DELETE /api/produtos/<pk>/` | `ProdutoViewSet.destroy` | Autenticado (JWT) |
| Vendas | `GET /api/vendas/` | `VendaListAPIView` | Autenticado (JWT) |
| Faturamento | `GET /api/faturamento/` | `FaturamentoAPIView` | JWT + `IsEmpresaAdmin` |
| Docs | `GET /api/schema/` | `SpectacularAPIView` | Público |
| Docs | `GET /api/docs/` | `SpectacularSwaggerView` | Público |
| Debug | `GET /email/` | `envia_email_view` | Público |

| **Parte 3 ✅** | URLs centralizadas com `include()`, rotas nomeadas e separação clara entre HTML (`/produtos/`, `/vendas/`) e API (`/api/`). |
---

## 🗄 4. Models — Dados do Sistema

### 4.1 Relacionamentos (visão geral)

```text
User (django.contrib.auth)
 ├─1:1─ Perfil ──── N:1 ──┐
 ├─1:1─ Admin ───── N:1 ──┤──> Empresa
 ├─1:N─ Produto ── N:1 ──> Categoria
 ├─1:N─ Cliente
 └─1:N─ Venda ─┬─ N:1 ──> Cliente
               └─1:N─> ItemVenda ── N:1 ──> Produto
```

### 4.2 `accounts/models.py`

| Model | Campos | Regras |
|-------|--------|--------|
| `Empresa` | `nome` (Char 100), `cnpj` (Char 14, **unique**), `endereco` (Char 255, null), `telefone` (Char 11, null), `email` (EmailField, null) | `__str__` → `nome` |
| `Perfil` | `user` (OneToOne → User), `nome` (Char 100, default ''), `telefone`, `cargo`, `cpf`, `imagem` (ImageField → `perfis/`), `empresa` (FK → Empresa, null, `related_name='perfis'`) | Vincula o usuário a uma empresa |
| `Admin` | `user` (OneToOne → User), `empresa` (FK → Empresa, `related_name='admins'`) | `UniqueConstraint(fields=['empresa'], name='unique_admin_per_empresa')` → **apenas 1 admin por empresa** |

> A existência de um registro em `Admin` é o que define o "dono da empresa" no sistema.

### 4.3 `produtos/models.py`

| Model | Campos | Regras |
|-------|--------|--------|
| `Categoria` | `nome` (Char 100), `descricao` (Text, null) | `__str__` → `nome` |
| `Produto` | `usuario` (FK → User, `related_name='produtos'`), `nome` (Char 100), `descricao` (Text), `preco` (Decimal 10,2), `estoque` (PositiveInteger), `imagem` (ImageField → `produtos/`), `categoria` (FK → Categoria, `on_delete=SET_NULL`), `data_criacao` (auto_now_add), `data_atualizacao` (auto_now) | Isolamento por usuário: cada produto pertence a um usuário |

Métodos de negócio do `Produto`:

- `clean()` → valida que `estoque >= 0`.
- `baixar_estoque(quantidade)` → valida `quantidade > 0` e estoque suficiente; subtrai e salva com `update_fields=['estoque', 'data_atualizacao']`.
- `repor_estoque(quantidade)` → valida `quantidade > 0`; soma e salva.

### 4.4 `vendas/models.py`

| Model | Campos | Regras |
|-------|--------|--------|
| `Cliente` | `usuario` (FK → User, `related_name='clientes'`), `nome` (Char 100), `email` (EmailField), `telefone` (Char 15, null), `endereco` (Text, null) | `__str__` → `nome` |
| `Venda` | `usuario` (FK → User, `related_name='vendas'`), `numero` (PositiveInteger, `editable=False`), `data_venda` (auto_now_add), `total` (Decimal 10,2, `editable=False`, default `0.00`), `cliente` (FK → Cliente, `on_delete=SET_NULL`, null) | `ordering=['-data_venda']`; `UniqueConstraint(['usuario','numero'])` |
| `ItemVenda` | `venda` (FK → Venda, `related_name='itens'`), `produto` (FK → Produto), `quantidade` (PositiveInteger), `subtotal` (Decimal 10,2, `editable=False`) | Item pertence a uma venda e aponta para um produto |

**Regras de negócio implementadas em `Venda`:**

```python
def save(self, *args, **kwargs):
    if self.pk is None:
        self.total = Decimal('0.00')
        if self.numero is None:
            ultima = Venda.objects.filter(usuario=self.usuario).order_by('-numero').first()
            self.numero = (ultima.numero + 1) if ultima else 1
    super().save(*args, **kwargs)

def atualizar_total(self):
    total = self.itens.aggregate(total=Sum('subtotal'))['total'] or Decimal('0.00')
    if self.total != total:
        self.total = total
        super().save(update_fields=['total'])

def delete(self, *args, **kwargs):
    with transaction.atomic():
        for item in self.itens.select_related('produto').all():
            produto = Produto.objects.select_for_update().get(pk=item.produto_id)
            produto.repor_estoque(item.quantidade)   # devolve estoque ao excluir a venda
        super().delete(*args, **kwargs)
```

- **Numeração automática** por usuário (`#1`, `#2`, ...) garantida pelo `UniqueConstraint`.
- **Total recalculado** a partir da soma dos subtotais dos itens.
- **Exclusão devolve estoque** ao produto (transação atômica + lock).

**Regras de negócio implementadas em `ItemVenda`:**

```python
def save(self, *args, **kwargs):
    if self.quantidade <= 0:
        raise ValidationError({'quantidade': 'A quantidade deve ser maior que zero.'})
    with transaction.atomic():
        produto = Produto.objects.select_for_update().get(pk=self.produto_id)
        item_antigo = ItemVenda.objects.select_for_update().get(pk=self.pk) if self.pk else None
        if item_antigo:   # edição de item existente
            if item_antigo.produto_id == produto.pk:
                diferenca = self.quantidade - item_antigo.quantidade
                produto.baixar_estoque(diferenca) if diferenca > 0 else produto.repor_estoque(abs(diferenca))
            else:          # troca de produto
                item_antigo.produto.repor_estoque(item_antigo.quantidade)
                produto.baixar_estoque(self.quantidade)
        else:              # item novo
            produto.baixar_estoque(self.quantidade)
        self.subtotal = Decimal(produto.preco) * self.quantidade
        self.produto = produto
        super().save(*args, **kwargs)
        self.venda.atualizar_total()

def delete(self, *args, **kwargs):
    with transaction.atomic():
        produto = Produto.objects.select_for_update().get(pk=self.produto_id)
        produto.repor_estoque(self.quantidade)   # devolve estoque ao remover o item
        venda = self.venda
        super().delete(*args, **kwargs)
        venda.atualizar_total()
```

| **Parte 4 ✅** | Models com `OneToOne`, `ForeignKey`, `UniqueConstraint`, validações (`clean`) e lógica transacional de estoque (`transaction.atomic` + `select_for_update`). |
---

## 👁 5. Views — CBV e FBV

### 5.1 Class-Based Views (CBV)

**`core/views.py` → `DashboardView(LoginRequiredMixin, TemplateView)`**

```python
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "core/dashboard.html"

    def dispatch(self, request, *args, **kwargs):
        # Apenas admin (superuser ou registrado no modelo Admin) pode acessar
        if not (request.user.is_superuser or Admin.objects.filter(user=request.user).exists()):
            messages.error(request, 'Acesso restrito. Apenas administradores podem acessar o dashboard.')
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["total_produtos"] = Produto.objects.filter(usuario=user).count()
        context["total_vendas"] = Venda.objects.filter(usuario=user).count()
        return context
```

- `LoginRequiredMixin` → bloqueia usuários anônimos (redireciona para o login).
- `dispatch()` sobrescrito → aplica a regra de admin antes de renderizar.
- `get_context_data()` → injeta os totais exibidos nos cards do dashboard.

### 5.2 Function-Based Views (FBV)

A maior parte do projeto usa FBV por causa da necessidade de controle explícito de fluxo (formulários + formsets + mensagens).

**`registrar_venda` (venda com itens via formset) — `vendas/views.py`:**

```python
@login_required
def registrar_venda(request):
    form_kwargs = {'user': request.user}
    venda = Venda(usuario=request.user)
    venda_form = VendaForm(request.POST or None, instance=venda, user=request.user)
    formset = ItemVendaFormSet(request.POST or None, instance=venda, form_kwargs=form_kwargs)
    if request.method == 'POST' and venda_form.is_valid() and formset.is_valid():
        try:
            with transaction.atomic():
                venda = venda_form.save()
                formset.instance = venda
                formset.save()
                venda.refresh_from_db()
        except ValidationError as exc:
            messages.error(request, exc.messages[0])
            return render(request, 'vendas/registrar_venda.html', {...})
        return redirect('venda_detail', pk=venda.pk)
    return render(request, 'vendas/registrar_venda.html', {'formset': formset, 'venda_form': venda_form})
```

**`faturamento` (restrito ao admin):**

```python
@login_required
@admin_required
def faturamento(request):
    vendas = Venda.objects.filter(usuario=request.user)
    total_faturamento = sum((venda.total for venda in vendas), Decimal('0.00'))
    return render(request, 'vendas/faturamento.html', {
        'total_faturamento': total_faturamento,
        'nome_usuario': request.user.username,
    })
```

**Padrão de CRUD de produtos (`produtos/views.py`):**

| View | Decorators | Responsabilidade |
|------|-----------|------------------|
| `produto_list_view` | `@login_required` | Lista produtos do usuário |
| `produto_detail_view` | `@login_required` | Detalha produto (`get_object_or_404(..., usuario=request.user)`) |
| `produto_create` | `@login_required` + `@admin_required` | Cria e vincula `usuario=request.user` |
| `produto_update_view` | `@login_required` + `@admin_required` | Atualiza produto do usuário |
| `produto_delete` | `@login_required` + `@admin_required` | Exclui via POST (com tela de confirmação) |

> **Padrão importante:** todas as consultas filtram por `usuario=request.user`, garantindo isolamento de dados entre contas.

### 5.3 Decorador `@admin_required` (`accounts/decorators.py`)

```python
def admin_required(view_func):
    """Permite acesso apenas a superuser ou usuário registrado no modelo Admin."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.is_superuser or Admin.objects.filter(user=request.user).exists():
            return view_func(request, *args, **kwargs)
        messages.error(request, 'Acesso restrito. Apenas administradores podem acessar esta página.')
        return redirect('index')
    return _wrapped_view
```

### 5.4 Views da API

| View | Arquivo | Tipo | Comportamento |
|------|---------|------|---------------|
| `register_api` | `accounts/api_views.py` | `@api_view(['POST'])` + `AllowAny` | Valida `RegisterSerializer`, cria o usuário, vincula a empresa no `Perfil` e devolve `201` com `user` + tokens JWT |
| `login_api` | `accounts/api_views.py` | `@api_view(['POST'])` + `AllowAny` | Autentica via `authenticate()`; `200` com tokens; `400` sem credenciais; `401` credenciais inválidas |
| `ProdutoViewSet` | `produtos/api_views.py` | `ModelViewSet` | CRUD completo; `get_queryset()` filtra por `usuario`; `perform_create()` grava `usuario=request.user` |
| `VendaListAPIView` | `vendas/api_views.py` | `APIView` | `GET` lista as vendas do usuário logado (`IsAuthenticated`) |
| `FaturamentoAPIView` | `vendas/api_views.py` | `APIView` | `GET` soma o faturamento (`IsAuthenticated` + `IsEmpresaAdmin`) |

| **Parte 5 ✅** | CBV (`TemplateView` + mixin) no dashboard e FBV no restante; API com `@api_view`, `APIView` e `ModelViewSet`; acesso controlado por `@login_required` e `@admin_required`. |
---

## 🎨 6. Templates

O projeto usa o **Django Template Language (DTL)** renderizado pelas views HTML.

### 6.1 Configuração (`settings.py`)

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],            # nenhum diretório global: usa só os templates dos apps
        'APP_DIRS': True,      # busca templates dentro de cada app instalada
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'accounts.context_processors.is_admin_context',
            ],
        },
    },
]
```

Como `APP_DIRS=True`, cada app guarda seus templates em `<app>/templates/<app>/...`:

| App | Templates |
|-----|-----------|
| `accounts` | login, register, perfil, editar_perfil, deletar_perfil, redefinir_senha, nova_senha, empresa_list, empresa_form, empresa_confirm_delete, promover_admin |
| `produtos` | produto_list, produto_detail, produto_form, produto_confirm_delete, categoria_list, categoria_form, categoria_confirm_delete |
| `vendas` | vendas_list, registrar_venda, venda_detail, venda_confirm_delete, faturamento, clientes_list, cadastro_cliente, editar_cliente, deletar_cliente |
| `core` | base.html, index, about, dashboard |

### 6.2 Herança de templates (`core/templates/core/base.html`)

Todos os templates estendem `core/base.html`, que define o layout comum (topbar, navegação, mensagens e o bloco de conteúdo):

```django
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <title>{% block title %}Vendas CRM{% endblock %}</title>
    {% load static %}
    <link rel="stylesheet" href="{% static 'core/app.css' %}">
</head>
<body>
    <!-- topbar + nav -->
    <nav class="nav-links">
        <a href="{% url 'index' %}">Inicio</a>
        {% if is_admin %}<a href="{% url 'dashboard' %}">Dashboard</a>{% endif %}
        {% if user.is_authenticated %}<a href="{% url 'perfil' %}">Perfil</a>{% endif %}
        ...
    </nav>

    {% if messages %}
        <section class="messages">
            {% for message in messages %}
                <div class="message {{ message.tags }}">{{ message }}</div>
            {% endfor %}
        </section>
    {% endif %}

    <main class="content-card">
        {% block content %}{% endblock %}
    </main>
</body>
</html>
```

Padrão usado em cada página filha:

```django
{% extends 'core/base.html' %}
{% block title %}Produtos | Vendas CRM{% endblock %}

{% block content %}
    ...conteúdo específico...
{% endblock %}
```

### 6.3 Context processor `is_admin`

`accounts/context_processors.py` injeta `is_admin` em **todos** os templates, permitindo esconder/mostrar links administrativos (Dashboard, Faturamento, criar/editar/excluir):

```python
def is_admin_context(request):
    """Disponibiliza 'is_admin' para todos os templates."""
    if not request.user.is_authenticated:
        return {'is_admin': False}
    is_admin = request.user.is_superuser or Admin.objects.filter(user=request.user).exists()
    return {'is_admin': is_admin}
```

### 6.4 Recursos de front-end

- **Estilos:** um único CSS global em `core/static/core/app.css` (carregado com `{% static %}`).
- **Mensagens (`django.contrib.messages`):** feedback de sucesso/erro exibido no topo via `base.html`.
- **JavaScript:** pequeno script inline no `base.html` para o botão "mostrar/ocultar senha" (`.password-toggle`).
- **URLs nomeadas:** navegação sempre via `{% url 'nome-da-rota' %}` (nunca paths hardcoded).

| **Parte 6 ✅** | Templates com herança a partir de `base.html`, `{% static %}` para CSS, mensagens do Django e context processor `is_admin` para renderização condicional. |
---

## 📋 7. Forms

### 7.1 `accounts/forms.py`

**`buscar_ou_criar_empresa(nome)`** (função utilitária):

```python
def buscar_ou_criar_empresa(nome):
    """
    Busca uma empresa pelo nome (case-insensitive, sem espaços extras).
    Se não existir, cria uma nova com CNPJ único gerado via hash.
    """
    nome = nome.strip()
    if not nome:
        return None
    empresa = Empresa.objects.filter(nome__iexact=nome).first()
    if not empresa:
        cnpj = hashlib.md5(nome.encode()).hexdigest()[:14]
        empresa = Empresa.objects.create(nome=nome, cnpj=cnpj)
    return empresa
```

- Normaliza o nome (`strip`) e busca com `nome__iexact` (evita duplicatas por diferença de caixa).
- Se não existir, gera um `cnpj` determinístico via `md5` (14 chars) — permite cadastrar empresas sem informar CNPJ real e sem violar o `unique=True`.

| Form | Base | Campos |
|------|------|--------|
| `LoginForm` | `AuthenticationForm` | `username`, `password` (herdados) |
| `RegisterForm` | `UserCreationForm` | `username`, `email`, `password1`, `password2` + `nome`, `telefone`, `cargo`, `cpf`, `imagem` + `empresa_nome` (obrigatório), `cnpj`, `endereco`, `telefone_empresa`, `email_empresa` |
| `PerfilForm` | `ModelForm(Perfil)` | `nome`, `telefone`, `cargo`, `cpf`, `imagem` + campo extra `empresa_nome` |
| `EmpresaForm` | `ModelForm(Empresa)` | `nome`, `cnpj`, `endereco`, `telefone`, `email` |
| `AdminForm` | `ModelForm(Admin)` | `user`, `empresa` |

**`PerfilForm`** — preenche a empresa atual e a resolve no `save()`:

```python
class PerfilForm(forms.ModelForm):
    empresa_nome = forms.CharField(max_length=100, required=True, help_text='...')

    class Meta:
        model = Perfil
        fields = ('nome', 'telefone', 'cargo', 'cpf', 'imagem')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.empresa:
            self.fields['empresa_nome'].initial = self.instance.empresa.nome

    def save(self, commit=True):
        perfil = super().save(commit=False)
        nome_empresa = self.cleaned_data.get('empresa_nome', '').strip()
        if nome_empresa:
            perfil.empresa = buscar_ou_criar_empresa(nome_empresa)
        if commit:
            perfil.save()
        return perfil
```

### 7.2 `produtos/forms.py`

```python
class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'preco', 'estoque', 'imagem', 'categoria']
        widgets = {'descricao': forms.Textarea(attrs={'rows': 3})}
```

### 7.3 `vendas/forms.py`

| Form | Base | Detalhes |
|------|------|----------|
| `VendaForm` | `ModelForm(Venda)` | Campos `['cliente']`; `__init__(user=...)` filtra o queryset de clientes do usuário |
| `ItemVendaForm` | `ModelForm(ItemVenda)` | Campos `['produto', 'quantidade']`; filtra produtos do usuário e valida estoque no `clean()` |
| `ItemVendaFormSet` | `inlineformset_factory` | `extra=1`, `can_delete=False` |
| `ClienteForm` | `ModelForm(Cliente)` | `['nome', 'email', 'telefone', 'endereco']` |

**Validação de estoque no `ItemVendaForm.clean()`:**

```python
def clean(self):
    cleaned_data = super().clean()
    produto = cleaned_data.get('produto')
    quantidade = cleaned_data.get('quantidade')

    if not produto or quantidade is None:
        return cleaned_data
    if quantidade <= 0:
        raise forms.ValidationError({'quantidade': 'A quantidade deve ser maior que zero.'})
    if produto.estoque < quantidade:
        raise forms.ValidationError({
            'quantidade': f'Estoque insuficiente para {produto.nome}. Disponível: {produto.estoque}.'
        })
    return cleaned_data
```

**Formset de itens (`vendas/forms.py`):**

```python
ItemVendaFormSet = inlineformset_factory(
    Venda,
    ItemVenda,
    form=ItemVendaForm,
    extra=1,          # um item em branco por padrão
    can_delete=False, # exclusão é feita pela view de excluir venda (restaura estoque)
)
```

| **Parte 7 ✅** | `ModelForm`, `UserCreationForm`, `AuthenticationForm` e `inlineformset_factory`; validações customizadas (estoque insuficiente, quantidade inválida) e CNPJ gerado por hash. |

---

## 🏗 8. CBV vs FBV — Comparação no Projeto

| Critério | CBV | FBV |
|----------|-----|-----|
| Onde é usado | `core/views.py` → `DashboardView` | `accounts`, `produtos`, `vendas`, `envia_email` |
| Controle de login | `LoginRequiredMixin` | `@login_required` |
| Controle de admin | `dispatch()` sobrescrito | decorador `@admin_required` |
| Herança | `TemplateView`, `LoginRequiredMixin` | nenhuma (funções simples) |
| Motivo no projeto | Página estática simples, onde reaproveitar mixins e centralizar a regra de admin é vantajoso | Formulários com POST/GET, `inlineformset`, validações e tratamento de exceções exigem controle explícito do fluxo |

**Resumo:** o projeto usa **FBV como padrão** e **CBV apenas no dashboard**, onde o `LoginRequiredMixin` + `dispatch()` customizado tornam o código mais limpo e reutilizável.

| **Parte 8 ✅** | Comparação justificada: CBV (`TemplateView`) no dashboard, FBV no restante por exigir controle granular de fluxo. |
---

## 💼 9. Projeto CRM — Requisitos Atendidos (Back-end Django)

### 9.1 Fluxo completo de uma venda (passo a passo)

1. **Registro de venda (`/vendas/nova/`)** → `registrar_venda` monta um `VendaForm` (cliente) + `ItemVendaFormSet` (produtos e quantidades) já filtrados pelo usuário logado.
2. **Validação do formset** → `ItemVendaForm.clean()` impede quantidade `<= 0` e quantidade maior que o estoque disponível.
3. **Transação atômica** → `transaction.atomic()` envolve o salvamento da venda e dos itens; qualquer erro de estoque (`ValidationError`) faz rollback e exibe mensagem ao usuário.
4. **`ItemVenda.save()`** → com `select_for_update()` no produto, baixa o estoque (`baixar_estoque`), calcula `subtotal = preco * quantidade` e chama `venda.atualizar_total()`.
5. **`Venda.save()`** → atribui o `numero` sequencial por usuário e inicializa `total = 0.00`.
6. **Faturamento (`/vendas/faturamento/`)** → soma os `total` das vendas do usuário em `Decimal`.
7. **Exclusão de venda (`/vendas/<pk>/excluir/`)** → `Venda.delete()` devolve o estoque de cada item antes de remover o registro.

### 9.2 Tabela de requisitos

| Requisito | Como foi atendido |
|-----------|-------------------|
| Cadastrar, editar e remover produtos | `produto_create`, `produto_update_view`, `produto_delete` (`@login_required` + `@admin_required`), usando `ProdutoForm`. O produto é sempre gravado com `usuario=request.user` |
| Definir quantidade em estoque | Campo `estoque` (`PositiveIntegerField`) no model `Produto`, validado em `Produto.clean()` e no `ProdutoSerializer.validate_estoque()` |
| Atualizar o estoque a cada venda | `ItemVenda.save()` com `transaction.atomic()` + `select_for_update()`: baixa o estoque ao criar/editar o item e devolve ao remover; `ItemVenda.delete()` e `Venda.delete()` repõem o estoque |
| Faturamento total atualizado | `Venda.atualizar_total()` recalcula via `Sum('subtotal')` a cada mudança de item; `faturamento()` (HTML) e `FaturamentoAPIView` (API) expõem o total |
| Controle de acesso | Views HTML com `@login_required` e `@admin_required`; API com JWT + `IsAuthenticated` + `IsEmpresaAdmin` |
| Isolamento de dados por usuário | Todas as queries usam `filter(usuario=request.user)`; `get_object_or_404(..., usuario=request.user)` impede acesso a registros de terceiros |
| Exclusão segura de venda | `Venda.delete()` restaura o estoque dos itens dentro de uma transação |

> ⚠️ **Ponto de atenção (faturamento):** o cálculo atual é **por usuário** (`Venda.objects.filter(usuario=request.user)`), e não consolidado por empresa. Para um faturamento "da empresa" (somando as vendas de todos os usuários da mesma empresa), basta alterar as queries de `faturamento()` e `FaturamentoAPIView.get()` para filtrar por `usuario__perfil__empresa` do usuário logado.

### 9.3 Regras de negócio centrais

| Regra | Local | Detalhe |
|-------|-------|---------|
| Estoque nunca negativo | `Produto.baixar_estoque()` / `Produto.clean()` | Lança `ValidationError` se `estoque < quantidade` ou `quantidade <= 0` |
| Numeração de venda por usuário | `Venda.save()` + `UniqueConstraint(['usuario','numero'])` | Sequencial (`#1`, `#2`, ...) reiniciando por usuário |
| Total da venda sempre coerente | `Venda.atualizar_total()` | Agrega `Sum('subtotal')` dos itens |
| Subtotal derivado do preço atual | `ItemVenda.save()` | `subtotal = Decimal(produto.preco) * quantidade` |
| Um admin por empresa | `UniqueConstraint(['empresa'], name='unique_admin_per_empresa')` | Garante o "dono" único da empresa |

| **Parte 9 ✅** | MVP do CRM completo: CRUD de produtos com estoque, vendas transacionais com devolução de estoque, faturamento e isolamento de dados por usuário. |
---

## 🌐 10. DRF — Requests e Responses

No Django REST Framework, o ciclo requisição → resposta é abstraído:

- **`rest_framework.request.Request`**: envolve o `HttpRequest` do Django.
  - `request.data` → corpo já parseado conforme o `Content-Type` (JSON, form-data, etc). Substitui `request.POST`/`request.body`.
  - `request.query_params` → parâmetros da query string (equivalente ao antigo `request.GET`).
- **`rest_framework.response.Response`**: recebe dados Python (dict/list) e delega a renderização aos *renderers* (JSON por padrão).
  - Aceita `data` e `status` (ex.: `status.HTTP_201_CREATED`).

**Uso no projeto:**

```python
# accounts/api_views.py
@api_view(['POST'])
@permission_classes([AllowAny])
def register_api(request):
    serializer = RegisterSerializer(data=request.data)     # request.data
    if serializer.is_valid():
        ...
        return Response({...}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

| Onde | Uso |
|------|-----|
| `accounts/api_views.py` | `request.data` no register/login; `Response` com `201`, `200`, `400` e `401` |
| `produtos/api_views.py` | `Response` gerado pelo `ModelViewSet` a partir do serializer |
| `vendas/api_views.py` | `Response` com `200` e os dados de vendas/faturamento |

| **Parte 10.1 ✅** | `request.data` e `Response` (com status HTTP explícitos) em todas as views de API. |

---

## 📡 11. DRF — API REST

A API segue os princípios REST: recursos identificados por URL, verbos HTTP mapeando operações CRUD, comunicação stateless via JSON e autenticação por token.

### 11.1 Base e organização

- Prefixo único: **`/api/`**, definido em `main/urls.py` com três `include()`.
- Organização por app:

```python
# main/urls.py (trecho)
path('api/', include('accounts.api_urls')),   # autenticação
path('api/', include('produtos.api_urls')),   # produtos (router)
path('api/', include('vendas.api_urls')),     # vendas + faturamento
```

### 11.2 Contrato de recursos

```text
Autenticação
  POST   /api/register/          cria usuário + perfil/empresa, devolve JWT
  POST   /api/login/             autentica e devolve JWT
  POST   /api/token/refresh/     renova o access token

Produtos (recurso "produtos")
  GET    /api/produtos/          lista produtos do usuário
  POST   /api/produtos/          cria produto
  GET    /api/produtos/{id}/     detalha produto (inclui estoque)
  PUT    /api/produtos/{id}/     atualiza produto
  PATCH  /api/produtos/{id}/     atualiza parcialmente
  DELETE /api/produtos/{id}/     remove produto

Vendas / Faturamento
  GET    /api/vendas/            lista vendas do usuário
  GET    /api/faturamento/       faturamento (dono da empresa)

Documentação
  GET    /api/schema/            schema OpenAPI 3.0 (JSON)
  GET    /api/docs/              Swagger UI interativo
```

### 11.3 Exemplos de uso (cURL)

```bash
# 1) Registrar conta e obter tokens
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"ana","email":"ana@ex.com","password":"senha12345","empresa_nome":"Loja da Ana"}'

# 2) Login
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"ana","password":"senha12345"}'

# 3) Criar produto (rota protegida por JWT)
curl -X POST http://localhost:8000/api/produtos/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -d '{"nome":"Notebook","descricao":"14 polegadas","preco":"3500.00","estoque":10}'

# 4) Listar vendas
curl http://localhost:8000/api/vendas/ -H "Authorization: Bearer <ACCESS_TOKEN>"

# 5) Faturamento (apenas dono da empresa)
curl http://localhost:8000/api/faturamento/ -H "Authorization: Bearer <ACCESS_TOKEN>"

# 6) Renovar access token
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" -d '{"refresh":"<REFRESH_TOKEN>"}'
```

| **Parte 11 ✅** | API REST versionada por prefixo (`/api/`), com recursos claros, verbos HTTP corretos e respostas JSON. |
---

## 📦 12. DRF — Model Serializers

Os *serializers* convertem instâncias de models ↔ JSON e fazem a validação dos dados de entrada (papel semelhante aos Forms, mas voltado para API).

### 12.1 `accounts/serializers.py`

| Serializer | Model | Campos | Observações |
|------------|-------|--------|-------------|
| `UserSerializer` | `User` | `id`, `username`, `email`, `first_name`, `last_name` | Usado nas respostas de register/login |
| `RegisterSerializer` | `User` | `id`, `username`, `email`, `password`, `nome`, `empresa_nome` | `password` é `write_only=True, min_length=8`; `empresa_nome` é obrigatório; `nome` é opcional |

```python
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    nome = serializers.CharField(max_length=100, required=False, allow_blank=True)
    empresa_nome = serializers.CharField(
        max_length=100, required=True, allow_blank=False,
        error_messages={'blank': 'O campo empresa é obrigatório.',
                        'required': 'O campo empresa é obrigatório.'})

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'nome', 'empresa_nome')

    def create(self, validated_data):
        nome = validated_data.pop('nome', '')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
        )
        Perfil.objects.create(user=user, nome=nome)   # empresa é vinculada na view
        return user
```

### 12.2 `produtos/serializers.py`

```python
class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ('id', 'nome', 'descricao', 'preco', 'estoque', 'imagem',
                  'data_criacao', 'data_atualizacao')
        read_only_fields = ('id', 'data_criacao', 'data_atualizacao')

    def validate_estoque(self, value):
        if value < 0:
            raise serializers.ValidationError('O estoque não pode ser negativo.')
        return value

    def validate_preco(self, value):
        if value <= 0:
            raise serializers.ValidationError('O preço deve ser maior que zero.')
        return value
```

- `read_only_fields` protege campos gerados pelo sistema (`id`, datas).
- Validações de domínio replicadas na camada de API (`estoque >= 0`, `preco > 0`).

### 12.3 `vendas/serializers.py`

```python
class ItemVendaSerializer(serializers.ModelSerializer):
    produto = ProdutoSerializer(read_only=True)                 # nested (leitura)
    produto_id = serializers.PrimaryKeyRelatedField(            # escrita por id
        queryset=Produto.objects.all(), source='produto', write_only=True)

    class Meta:
        model = ItemVenda
        fields = ('id', 'produto', 'produto_id', 'quantidade', 'subtotal')
        read_only_fields = ('id', 'subtotal')


class VendaSerializer(serializers.ModelSerializer):
    itens = ItemVendaSerializer(many=True, read_only=True)
    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True, default=None)

    class Meta:
        model = Venda
        fields = ('id', 'numero', 'usuario', 'data_venda', 'total',
                  'cliente', 'cliente_nome', 'itens')
        read_only_fields = ('id', 'numero', 'usuario', 'data_venda', 'total')
```

Conceitos aplicados:

- **Serialização aninhada (nested):** `ItemVendaSerializer` expõe o produto completo (`produto`) na leitura.
- **Separação leitura/escrita:** `produto` (read-only, objeto completo) e `produto_id` (write-only, aceita PK na escrita) via o parâmetro `source='produto'`.
- **Campos derivados somente leitura:** `subtotal`, `total`, `numero` e `usuario` são calculados pelo model/view e nunca aceitos do cliente.
- **Campo calculado:** `cliente_nome` usa `source='cliente.nome'` para entregar um dado amigável ao consumidor da API.

| **Parte 12 ✅** | Serializers de todos os recursos da API, com validações, `read_only`/`write_only` corretos e serialização aninhada. |
---

## 🖐 13. DRF — `@api_view` e `APIView`

O DRF oferece três níveis de abstração para escrever views. O projeto usa os três.

| Nível | Recurso | Onde é usado no projeto |
|-------|---------|------------------------|
| Função + decorator | `@api_view(['POST'])` | `register_api`, `login_api` |
| Classe base | `APIView` | `VendaListAPIView`, `FaturamentoAPIView` |
| ViewSet (mais abstrato) | `ModelViewSet` | `ProdutoViewSet` |

### 13.1 `@api_view` (FBV de API)

Transforma uma função em view de API: valida os métodos HTTP permitidos, injeta o `Request` do DRF (`request.data`) e permite devolver `Response`.

```python
@api_view(['POST'])
@permission_classes([AllowAny])
def login_api(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'detail': 'Informe usuário e senha.'},
                        status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)
    if user is None:
        return Response({'detail': 'Credenciais inválidas.'},
                        status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)
    return Response({
        'user': UserSerializer(user).data,
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }, status=status.HTTP_200_OK)
```

> Adequado para endpoints simples e isolados, onde não há um recurso CRUD completo por trás (ex.: login).

### 13.2 `APIView` (CBV de API)

Classe em que cada método HTTP é um método Python (`get`, `post`, `put`, `patch`, `delete`) e as permissões são declaradas via `permission_classes`.

```python
class VendaListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        vendas = Venda.objects.filter(usuario=request.user)
        serializer = VendaSerializer(vendas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FaturamentoAPIView(APIView):
    permission_classes = [IsAuthenticated, IsEmpresaAdmin]

    def get(self, request):
        vendas = Venda.objects.filter(usuario=request.user)
        total = sum((venda.total for venda in vendas), Decimal('0.00'))
        return Response({
            'usuario': request.user.username,
            'total_faturamento': str(total),
            'total_vendas': vendas.count(),
        }, status=status.HTTP_200_OK)
```

> Adequado quando a resposta não é um CRUD de recurso (ex.: um relatório consolidado como o faturamento).

| **Parte 13 ✅** | Uso combinado de `@api_view` (register/login) e `APIView` (vendas/faturamento), cada um no cenário em que é mais adequado. |

---

## 🎯 14. DRF — ViewSets e Routers

### 14.1 `ModelViewSet` — `ProdutoViewSet`

Um ViewSet agrupa as seis ações CRUD em uma única classe. O `ModelViewSet` já traz a implementação padrão de `list`, `create`, `retrieve`, `update`, `partial_update` e `destroy`.

```python
class ProdutoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para CRUD de produtos.
    Cada usuário só vê e gerencia seus próprios produtos.
    """
    serializer_class = ProdutoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Produto.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)
```

- `get_queryset()` → **escopo por usuário**: o queryset filtrado é usado por **todas** as ações, o que faz um `retrieve/update/delete` de um produto alheio responder `404`.
- `perform_create()` → injeta o dono automaticamente, sem exigir que o cliente envie o campo `usuario`.

### 14.2 `DefaultRouter` — geração automática de rotas

```python
# produtos/api_urls.py
router = DefaultRouter()
router.register(r'produtos', ProdutoViewSet, basename='produto')

urlpatterns = [path('', include(router.urls))]
```

Rotas geradas automaticamente:

| Método | URL | Ação do ViewSet | Nome da rota |
|--------|-----|-----------------|--------------|
| GET | `/api/produtos/` | `list` | `produto-list` |
| POST | `/api/produtos/` | `create` | `produto-list` |
| GET | `/api/produtos/{pk}/` | `retrieve` | `produto-detail` |
| PUT | `/api/produtos/{pk}/` | `update` | `produto-detail` |
| PATCH | `/api/produtos/{pk}/` | `partial_update` | `produto-detail` |
| DELETE | `/api/produtos/{pk}/` | `destroy` | `produto-detail` |

Benefícios: menos código repetitivo, URLs consistentes com o padrão REST e nomes de rota reaproveitáveis com `reverse('produto-detail', args=[pk])`.

| **Parte 14 ✅** | `ModelViewSet` com escopo por usuário + `DefaultRouter` gerando as seis rotas do CRUD de produtos. |
---

## ✏ 15. DRF — CRUD (POST/GET/PUT/PATCH/DELETE)

### 15.1 Como cada ação funciona no `ProdutoViewSet`

| Ação | O que o DRF faz | Comportamento no projeto |
|------|-----------------|--------------------------|
| `list` (GET) | Aplica `get_queryset()` e serializa com `many=True` | Lista apenas os produtos do usuário logado |
| `create` (POST) | Valida com o serializer e salva | `perform_create()` grava `usuario=request.user` |
| `retrieve` (GET `{pk}`) | Busca o objeto no queryset da view | Produto de outro usuário → `404` |
| `update` (PUT) | Valida o payload completo e salva | `produto.usuario` permanece o dono |
| `partial_update` (PATCH) | Valida apenas os campos enviados | Ideal para ajustar só o `estoque` ou o `preco` |
| `destroy` (DELETE) | Remove o objeto | Só é possível remover produtos do próprio usuário |

### 15.2 Matriz de verbos e permissões da API

| Recurso | Endpoint | Verbos | Permissão |
|---------|----------|--------|-----------|
| Conta | `/api/register/` | POST | `AllowAny` |
| Conta | `/api/login/` | POST | `AllowAny` |
| Token | `/api/token/refresh/` | POST | Público (exige `refresh` válido) |
| Produtos | `/api/produtos/` | GET, POST | `IsAuthenticated` |
| Produtos | `/api/produtos/{pk}/` | GET, PUT, PATCH, DELETE | `IsAuthenticated` |
| Vendas | `/api/vendas/` | GET | `IsAuthenticated` |
| Faturamento | `/api/faturamento/` | GET | `IsAuthenticated` + `IsEmpresaAdmin` |
| Docs | `/api/schema/`, `/api/docs/` | GET | Público |

### 15.3 Códigos de status retornados

| Código | Situação no projeto |
|--------|---------------------|
| `200 OK` | Login bem-sucedido; listagem/detalhe de recursos; faturamento |
| `201 Created` | Registro de conta e criação de produto |
| `400 Bad Request` | Erros de validação (serializer) ou credenciais não informadas |
| `401 Unauthorized` | Credenciais inválidas no login; token ausente/expirado |
| `404 Not Found` | Recurso inexistente ou pertencente a outro usuário |

> A autenticação JWT não é declarada view a view: ela vem do `REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES']` em `settings.py`, e as exceções (`AllowAny` no register/login) são explícitas.

### 15.4 Teste rápido com cURL

```bash
# Criar produto
curl -X POST http://localhost:8000/api/produtos/ \
  -H "Authorization: Bearer <ACCESS>" -H "Content-Type: application/json" \
  -d '{"nome":"Mouse","descricao":"Sem fio","preco":"89.90","estoque":25}'

# Atualizar apenas o estoque (PATCH)
curl -X PATCH http://localhost:8000/api/produtos/1/ \
  -H "Authorization: Bearer <ACCESS>" -H "Content-Type: application/json" \
  -d '{"estoque":40}'

# Remover produto
curl -X DELETE http://localhost:8000/api/produtos/1/ -H "Authorization: Bearer <ACCESS>"
```

| **Parte 15 ✅** | CRUD completo documentado: ações do ViewSet, matriz de verbos/permissões, códigos de status e exemplos de requisição. |
---

## 🔐 16. Autenticação

O projeto tem **dois mecanismos de autenticação independentes**, um para cada interface.

| Interface | Mecanismo | Persistência | Onde |
|-----------|-----------|--------------|------|
| HTML (templates) | Sessão do Django (`django.contrib.auth`) | Cookie de sessão | `/accounts/login/`, `@login_required` |
| API REST | **JWT** (SimpleJWT) | Token no header `Authorization: Bearer` | `/api/login/`, `/api/register/` |

### 16.1 Autenticação por sessão (HTML)

```python
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)          # cria a sessão
            return redirect('index')
        messages.error(request, 'Usuário ou senha inválidos.')
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)                        # encerra a sessão
    return redirect('index')
```

### 16.2 Autenticação JWT (API)

```python
refresh = RefreshToken.for_user(user)     # gera o refresh
return Response({
    'user': UserSerializer(user).data,
    'refresh': str(refresh),
    'access': str(refresh.access_token),  # access derivado do refresh
}, status=status.HTTP_200_OK)
```

- O **access token** é enviado em `Authorization: Bearer <token>` nas rotas protegidas.
- O **refresh token** é trocado por um novo access em `POST /api/token/refresh/` (view `TokenRefreshView` do SimpleJWT).

### 16.3 Configuração (`settings.py`)

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),   # access dura 60 min
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),      # refresh dura 1 dia
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    ...
}
```

| Configuração | Valor | Efeito |
|--------------|-------|--------|
| `ACCESS_TOKEN_LIFETIME` | 60 minutos | Validade do token usado nas requisições |
| `REFRESH_TOKEN_LIFETIME` | 1 dia | Validade do token usado para renovar o access |
| `ROTATE_REFRESH_TOKENS` | `False` | O mesmo refresh continua válido até expirar |
| `BLACKLIST_AFTER_ROTATION` | `True` | Prepara o projeto para blacklist caso a rotação seja ativada |
| `ALGORITHM` / `SIGNING_KEY` | `HS256` / `SECRET_KEY` | Assinatura dos tokens |
| `AUTH_HEADER_TYPES` / `AUTH_HEADER_NAME` | `Bearer` / `HTTP_AUTHORIZATION` | Formato do header esperado |

### 16.4 Fluxo de uso da API

```text
1. POST /api/register/  (ou /api/login/)   → { access, refresh }
2. Usar:  Authorization: Bearer <access>   → rotas protegidas
3. Quando o access expirar:
   POST /api/token/refresh/  { "refresh": "<refresh>" }  → { access }
4. Repetir o passo 2.
```

### 16.5 Redefinição de senha (HTML)

- `redefinir_senha` monta o e-mail com `default_token_generator` + `urlsafe_base64_encode(force_bytes(user.pk))` e envia por `send_mail`.
- O link aponta para `/accounts/redefinir-senha/<uidb64>/<token>/`, tratado por `nova_senha`, que valida o token e salva a nova senha.
- O envio é protegido por `try/except` e `EMAIL_TIMEOUT`, devolvendo mensagem amigável em vez de erro 500 quando o SMTP falha.

| **Parte 16 ✅** | Sessão (HTML) e JWT (API) convivendo no mesmo projeto, com tempos de vida, renovação de token e fluxo documentados. |
---

## 🔑 17. Permissões (DRF)

As permissões do DRF controlam **quem** pode acessar cada endpoint. Podem ser globais, por view ou customizadas.

### 17.1 Global (`settings.py`)

```python
REST_FRAMEWORK = {
    ...
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}
```

⇒ Toda view da API exige usuário autenticado **por padrão**. Views que precisam ser públicas precisam declarar isso explicitamente.

### 17.2 Por view

| View | `permission_classes` | Efeito |
|------|----------------------|--------|
| `register_api` | `[AllowAny]` | Registro aberto |
| `login_api` | `[AllowAny]` | Login aberto |
| `ProdutoViewSet` | `[IsAuthenticated]` | Só usuário logado (explícito, redundante com o global — documenta a intenção) |
| `VendaListAPIView` | `[IsAuthenticated]` | Só usuário logado |
| `FaturamentoAPIView` | `[IsAuthenticated, IsEmpresaAdmin]` | Logado **e** dono da empresa |

```python
@api_view(['POST'])
@permission_classes([AllowAny])
def register_api(request): ...

class FaturamentoAPIView(APIView):
    permission_classes = [IsAuthenticated, IsEmpresaAdmin]
```

### 17.3 Permissão customizada `IsEmpresaAdmin`

`accounts/permissions.py`:

```python
class IsEmpresaAdmin(BasePermission):
    """
    Permite acesso somente ao usuário que é administrador da empresa
    vinculada ao seu perfil (o dono da empresa).
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True

        perfil = getattr(request.user, 'perfil', None)
        if perfil is None or perfil.empresa_id is None:
            return False

        return Admin.objects.filter(
            user=request.user,
            empresa_id=perfil.empresa_id,
        ).exists()
```

Lógica, em ordem:

1. Usuário anônimo → `False`.
2. Superuser → `True` (acesso irrestrito para administração).
3. Sem `Perfil` ou sem empresa vinculada → `False`.
4. Existe registro em `Admin` ligando o usuário à empresa do seu próprio `Perfil` → `True`; caso contrário, `False`.

> **Conceito de "dono da empresa" no projeto:** é a combinação `Perfil.empresa` (a empresa do usuário) + `Admin` (o usuário é o administrador dela). Só esse usuário passa na verificação e vê o faturamento.

### 17.4 Permissões no lado HTML (paralelo)

| Recurso | HTML | API |
|---------|------|-----|
| Exigir login | `@login_required` | `IsAuthenticated` (global) |
| Exigir admin/dono | `@admin_required` (decorator) | `IsEmpresaAdmin` (`BasePermission`) |
| Esconder menus | context processor `is_admin` | — (o cliente decide o que exibir conforme os endpoints permitidos) |

### 17.5 Erros de permissão

| Situação | Resposta |
|----------|----------|
| Sem token / token expirado | `401 Unauthorized` |
| Token válido, mas sem permissão (não é dono) | `403 Forbidden` |
| Recurso de outro usuário | `404 Not Found` (o queryset filtrado esconde a existência do registro) |

| **Parte 17 ✅** | Permissões em três níveis: global (`IsAuthenticated`), por view (`AllowAny`, `IsAuthenticated`) e customizada (`IsEmpresaAdmin`), com paralelo entre HTML e API. |
---

## 💼 18. Projeto CRM — Requisitos da API Atendidos

| # | Requisito (trilha — Parte 5) | Implementação |
|---|------------------------------|---------------|
| 1 | Criar conta | `POST /api/register/` → `register_api` + `RegisterSerializer` (cria `User` e `Perfil`, vincula empresa via `buscar_ou_criar_empresa`) |
| 2 | Realizar login | `POST /api/login/` → `login_api` com `authenticate()` e retorno de `access` + `refresh` |
| 2b | Renovar token | `POST /api/token/refresh/` → `TokenRefreshView` (SimpleJWT) |
| 3 | CRUD de produtos restrito a usuário logado | `ProdutoViewSet` (`ModelViewSet`) + `DefaultRouter`: `GET/POST /api/produtos/` e `GET/PUT/PATCH/DELETE /api/produtos/{pk}/` com `IsAuthenticated` |
| 4 | Endpoint com detalhes do produto e estoque | Campo `estoque` exposto pelo `ProdutoSerializer` em `GET /api/produtos/{pk}/` (e na listagem) |
| 5 | Faturamento acessível apenas pelo dono da empresa | `GET /api/faturamento/` → `FaturamentoAPIView` com `IsEmpresaAdmin` |

### 18.1 Detalhamento dos endpoints de autenticação

**`POST /api/register/`** — corpo e resposta:

```json
// Request
{
  "username": "ana",
  "email": "ana@example.com",
  "password": "senha12345",
  "nome": "Ana Souza",
  "empresa_nome": "Loja da Ana"
}

// 201 Created
{
  "user": {"id": 1, "username": "ana", "email": "ana@example.com", "first_name": "", "last_name": ""},
  "refresh": "<jwt-refresh>",
  "access": "<jwt-access>"
}
```

**`POST /api/login/`** — erros previstos:

| Corpo enviado | Status | Resposta |
|---------------|--------|----------|
| `{username, password}` válidos | `200` | `user` + `access` + `refresh` |
| Falta `username` ou `password` | `400` | `{"detail": "Informe usuário e senha."}` |
| Credenciais incorretas | `401` | `{"detail": "Credenciais inválidas."}` |

### 18.2 Endpoint de faturamento

```json
// GET /api/faturamento/  (Authorization: Bearer <access>)
{
  "usuario": "ana",
  "total_faturamento": "1234.50",
  "total_vendas": 7
}
```

- `total_faturamento` é retornado como **string** para preservar a precisão do `Decimal` no JSON.
- `403 Forbidden` se o usuário autenticado não for o admin da empresa do seu perfil.

### 18.3 Verificação rápida de cada requisito

```bash
# 1 e 2 — criar conta e logar
curl -X POST http://localhost:8000/api/register/ -H "Content-Type: application/json" \
  -d '{"username":"ana","email":"a@e.com","password":"senha12345","empresa_nome":"Loja"}'
curl -X POST http://localhost:8000/api/login/ -H "Content-Type: application/json" \
  -d '{"username":"ana","password":"senha12345"}'

# 3 — CRUD de produtos (com token)
curl http://localhost:8000/api/produtos/ -H "Authorization: Bearer $TOKEN"

# 4 — detalhe com estoque
curl http://localhost:8000/api/produtos/1/ -H "Authorization: Bearer $TOKEN"

# 5 — faturamento (apenas dono)
curl http://localhost:8000/api/faturamento/ -H "Authorization: Bearer $TOKEN"
```

> ⚠️ **Ponto de atenção:** o faturamento hoje é somado **por usuário** (`filter(usuario=request.user)`). Para um valor consolidado da empresa inteira, altere a query para considerar todos os usuários da mesma empresa (`usuario__perfil__empresa=request.user.perfil.empresa`). A permissão `IsEmpresaAdmin` continua válida nos dois cenários.

| **Parte 18 ✅** | Os cinco requisitos da Parte 5 da trilha atendidos e verificáveis via cURL/Swagger, com o ponto de atenção do escopo do faturamento documentado. |
---

## 📝 19. Documentação da API — drf-spectacular (OpenAPI 3.0 + Swagger UI)

### 19.1 O que é e onde fica

A documentação **não é um arquivo estático**: ela é gerada dinamicamente pelo `drf-spectacular` a partir das views, serializers, permissões e da configuração de autenticação.

| Rota | View | Retorno |
|------|------|---------|
| `/api/schema/` | `SpectacularAPIView` | Schema OpenAPI 3.0 em JSON (contrato completo da API) |
| `/api/docs/` | `SpectacularSwaggerView` | **Swagger UI** — interface interativa que consome o schema acima |

Configuração das rotas (`main/urls.py`):

```python
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    ...
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='api-schema'), name='swagger-ui'),
]
```

> O `url_name='api-schema'` faz o Swagger UI buscar o JSON na rota `api-schema`.

### 19.2 Configuração (`settings.py`)

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'drf_spectacular',                 # (1) app registrado
    'rest_framework_simplejwt',
    ...
]

REST_FRAMEWORK = {
    ...
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',   # (2) schema do spectacular
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Vendas CRM API',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication'  # (3) Swagger sabe que usa JWT
    ],
}
```

Os três itens são **obrigatórios** para o Swagger UI funcionar com campos de teste:

1. `drf_spectacular` em `INSTALLED_APPS` → habilita o gerador (templates/tags internos).
2. `DEFAULT_SCHEMA_CLASS` apontando para o `AutoSchema` do spectacular → sem isso o DRF usa o schema padrão e o gerador falha com `AssertionError: Incompatible AutoSchema used on View ...`.
3. `SPECTACULAR_SETTINGS['DEFAULT_AUTHENTICATION_CLASSES']` → documenta o esquema de segurança *Bearer* e habilita o botão **Authorize**.

### 19.3 Como testar endpoints pelo Swagger UI

1. Acesse `http://localhost:8000/api/docs/` (em produção, a URL equivalente do Render).
2. Abra um dos endpoints — o botão **Try it out** habilita os campos de entrada (parâmetros de rota, query e corpo JSON).
3. Para rotas protegidas:
   - Faça `POST /api/login/` (ou `/api/register/`) e copie o valor de `access`.
   - Clique em **Authorize**, cole o token (o esquema é `Bearer <token>`) e confirme.
   - Execute as operações: o token será enviado automaticamente no header `Authorization`.
4. `POST /api/token/refresh/` permite renovar o `access` sem novo login.

### 19.4 Por que "não aparecem os campos de texto"?

Os campos de entrada (e o botão *Try it out*) só existem **dentro de cada operação** da página. Se a interface não renderizar os endpoints, as causas típicas são:

| Sintoma | Causa provável | Correção |
|---------|----------------|----------|
| `AssertionError: Incompatible AutoSchema used on View ...` | `DEFAULT_SCHEMA_CLASS` não aponta para `drf_spectacular.openapi.AutoSchema` | Ajustar em `REST_FRAMEWORK` |
| `TemplateDoesNotExist: drf_spectacular/...` | `drf_spectacular` ausente de `INSTALLED_APPS` | Adicionar em `INSTALLED_APPS` |
| Página sem endpoints | Erro na geração do schema (alguma view/queryset quebra a geração) | Rodar `python manage.py spectacular --file schema.yml` e ler o erro |
| Sem o botão *Authorize* | `SPECTACULAR_SETTINGS['DEFAULT_AUTHENTICATION_CLASSES']` não configurado | Incluir o `JWTAuthentication` |
| Layout antigo/em branco no navegador | Cache do navegador ou servidor não reiniciado | Reiniciar `runserver` e recarregar com `Ctrl+F5` |

Diagnóstico rápido do schema:

```bash
python manage.py spectacular --file schema.yml    # gera o schema e mostra os erros
```

### 19.5 Evoluções possíveis

- **`@extend_schema`**: anotar views para descrever respostas, exemplos e parâmetros com mais riqueza do que a inferência automática.
- **`@extend_schema_view`**: aplicar descrições a todas as ações de um ViewSet de uma vez.
- **`SPECTACULAR_SETTINGS['DESCRIPTION']`**: adicionar texto introdutório na raiz da documentação.
- **Proteger `/api/docs/`**: exigir autenticação em produção, caso a documentação não deva ser pública.

| **Parte 19 ✅** | Documentação OpenAPI automática com Swagger UI, JWT no Authorize, fluxo de teste e um guia de diagnóstico dos problemas mais comuns. |
---

## 🚀 20. Configuração de Ambiente e Deploy

### 20.1 Variáveis de ambiente (`.env`)

O `python-decouple` lê as variáveis do `.env` (nunca versionado). Use `.env.example` como modelo:

```bash
# Django core
SECRET_KEY=change-me-a-secure-random-string
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Email (SMTP) — use "senha de app" no Gmail
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu-email@example.com
EMAIL_HOST_PASSWORD=sua-senha-de-app
EMAIL_TIMEOUT=10

# Banco (vazio em dev → SQLite local)
# DATABASE_URL=postgresql://usuario:senha@host:5432/vendas_crm

# Cloudinary (vazio em dev → media/ local)
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
```

### 20.2 Como o `settings.py` alterna entre ambientes

| Variável | Ausente (desenvolvimento) | Definida (produção) |
|----------|---------------------------|---------------------|
| `DEBUG` | `False` por padrão — defina `True` no `.env` local | `False` |
| `DATABASE_URL` | SQLite (`db.sqlite3`) | PostgreSQL via `dj_database_url` |
| Credenciais Cloudinary | `FileSystemStorage` (`media/`) | `CloudinaryMediaStorage` |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | hosts informados + `RENDER_EXTERNAL_HOSTNAME` |
| `CSRF_TRUSTED_ORIGINS` | lista do `.env` | lista do `.env` + `https://<hostname do Render>` |

Trechos relevantes:

```python
if config('DATABASE_URL', default=''):
    DATABASES = {'default': dj_database_url.config(conn_max_age=600, conn_health_checks=True)}
else:
    DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}}

USE_CLOUDINARY_STORAGE = all(CLOUDINARY_STORAGE.values())

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
```

### 20.3 Arquivos estáticos e de mídia

- **Estáticos** (`STATIC_URL='/static/'`, `STATIC_ROOT=staticfiles/`): servidos pelo **WhiteNoise** (`CompressedManifestStaticFilesStorage`) — não depende do modo `DEBUG`.
- **Mídia** (`MEDIA_URL='/media/'`, `MEDIA_ROOT=media/`): em desenvolvimento o Django serve os arquivos (via `static()` no `urls.py` quando `DEBUG=True`); em produção vão para o **Cloudinary**.

### 20.4 Docker

```dockerfile
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libjpeg-dev zlib1g-dev && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### 20.5 Deploy no Render (`render.yaml` + `build.sh`)

```yaml
databases:
  - name: vendas-crm-db
    databaseName: vendas_crm
    plan: free
    region: oregon

services:
  - type: web
    name: vendas-crm
    runtime: python
    branch: main
    buildCommand: bash build.sh
    startCommand: gunicorn main.wsgi:application
    healthCheckPath: /
    envVars:
      - key: PYTHON_VERSION
        value: "3.12.10"
      - key: SECRET_KEY
        generateValue: true
      - key: DEBUG
        value: "False"
      - key: ALLOWED_HOSTS
        value: ".onrender.com"
      - key: DATABASE_URL
        fromDatabase: {name: vendas-crm-db, property: connectionString}
      - key: EMAIL_HOST_USER      # secret (sync: false)
      - key: EMAIL_HOST_PASSWORD  # secret (sync: false)
      - key: CLOUDINARY_CLOUD_NAME / API_KEY / API_SECRET  # secrets
```

```bash
#!/usr/bin/env bash
set -o errexit
pip install --upgrade pip
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput
```

Fluxo de publicação: **`develop` → `main`** (merge). O Render observa a branch `main` com `autoDeploy: true` e roda `build.sh` + `gunicorn main.wsgi:application`.

### 20.6 Comandos úteis

```bash
python manage.py makemigrations     # criar migrações
python manage.py migrate            # aplicar migrações
python manage.py createsuperuser    # criar superusuário (acesso ao /admin/)
python manage.py collectstatic      # coletar estáticos (produção)
python manage.py runserver          # servidor de desenvolvimento
python manage.py spectacular --file schema.yml   # gerar/validar o schema OpenAPI
```

| **Parte 20 ✅** | Configuração 12-factor (`.env`), alternância SQLite/PostgreSQL, storage local/Cloudinary, WhiteNoise para estáticos, Docker e pipeline de deploy no Render documentados. |
---

## 🛠 21. Solução de Problemas (Troubleshooting)

| Sintoma | Causa provável | Solução |
|---------|----------------|---------|
| `ModuleNotFoundError: drf_spectacular` | Pacote não instalado no venv ativo | `pip install -r requirements.txt` com o venv ativado |
| `AssertionError: Incompatible AutoSchema used on View ...` | `DEFAULT_SCHEMA_CLASS` não aponta para o `AutoSchema` do spectacular | Conferir `REST_FRAMEWORK` em `settings.py` |
| `TemplateDoesNotExist: drf_spectacular/...` | `drf_spectacular` fora de `INSTALLED_APPS` | Adicionar o app em `INSTALLED_APPS` |
| Swagger sem campos de teste / sem *Authorize* | Falta `SPECTACULAR_SETTINGS['DEFAULT_AUTHENTICATION_CLASSES']` | Incluir `JWTAuthentication` |
| Erro 500 ao pedir redefinição de senha | SMTP com credencial inválida ou host bloqueado | Usar **senha de app** do Gmail; `try/except` + `EMAIL_TIMEOUT` já evitam 500 genérico |
| `DisallowedHost` em produção | `RENDER_EXTERNAL_HOSTNAME` ausente ou host não listado | Conferir a variável de ambiente no Render |
| Erro de CSRF em POST no domínio público | Origem não confiável | Definir `CSRF_TRUSTED_ORIGINS=https://seu-dominio` |
| Imagens somem após deploy | Uploads gravados no disco efêmero | Configurar as três variáveis do Cloudinary |
| `403 Forbidden` em `/api/faturamento/` | Usuário não é admin da empresa do próprio perfil | Promover via `/accounts/promover-admin/` ou criar registro em `Admin` |
| `401 Unauthorized` com token "válido" | Access token expirado (60 min) | Renovar com `POST /api/token/refresh/` |
| Estático sem estilo em produção | `collectstatic` não executado | Conferir `build.sh` (arquivos servidos via WhiteNoise) |
| Erro de CORS no navegador | Chamada cross-origin sem `django-cors-headers` | Consumir a API no mesmo domínio ou adicionar CORS |

### 21.1 Diagnóstico rápido

```bash
python manage.py check                          # valida a configuração do Django
python manage.py spectacular --file schema.yml  # valida a geração do schema (mostra erros)
```

| **Parte 21 ✅** | Tabela de problemas frequentes (Swagger, SMTP, deploy, permissões) com causa e correção. |
---

## ✅ 22. Checklist Final de Entrega

### 22.1 Back-end Django (Parte 4 da trilha)

- [x] Ambiente virtual + `requirements.txt` versionado (Python 3.12.10)
- [x] Projeto `main` + apps `accounts`, `produtos`, `vendas`, `core`, `envia_email`
- [x] URLs com `include()` e rotas nomeadas
- [x] Models com relacionamentos, validações e estoque transacional
- [x] CRUD de produtos e categorias (HTML)
- [x] Vendas com `inlineformset` e rollback em estoque insuficiente
- [x] Faturamento com `Decimal` restrito ao admin
- [x] CBV (`DashboardView`) e FBV (`@login_required`, `@admin_required`)
- [x] Templates com herança (`base.html`) e context processor `is_admin`
- [x] Forms com validações customizadas
- [x] Isolamento de dados por usuário em todas as queries

### 22.2 API REST (Parte 5 da trilha)

- [x] Registro e login retornando JWT
- [x] CRUD de produtos via `ModelViewSet` + `DefaultRouter` (JWT)
- [x] Detalhe do produto com estoque
- [x] Faturamento restrito ao dono (`IsEmpresaAdmin`)
- [x] Serializers com validações, `read_only`/`write_only` e nested
- [x] JWT global (60 min / 1 dia) + refresh
- [x] Permissões em três níveis
- [x] OpenAPI + Swagger UI (`/api/schema/`, `/api/docs/`)

### 22.3 Infra

- [x] `.env.example` com todas as variáveis
- [x] `.gitignore` protegendo `venv/`, `.env`, `db.sqlite3`, `media/`, `staticfiles/`
- [x] `Dockerfile`, `build.sh` e `render.yaml`
- [x] WhiteNoise para estáticos + proxy SSL
- [x] Documentação (`docs/PROJETO.md`) e Swagger

### 22.4 Pontos de melhoria

1. **Faturamento por empresa:** hoje é somado por usuário; consolidar com `usuario__perfil__empresa`.
2. **Testes automatizados:** `tests.py` sem casos — cobrir estoque, permissões e API.
3. **Validação de CNPJ:** o `cnpj` por `md5` é artifício de unicidade; validar dígitos verificadores.
4. **`@extend_schema`:** enriquecer a documentação da API.
5. **Proteger `/api/docs/`:** restringir a documentação se necessário.

| **Parte 22 ✅** | Checklists de back-end, API e infraestrutura com pontos de melhoria mapeados. |

---

## 📚 23. Referência Rápida de Arquivos

| Área | Arquivo | Conteúdo |
|------|---------|----------|
| Config | `main/settings.py` | DB, templates, DRF, JWT, e-mail, storage |
| Config | `main/urls.py` | Rotas HTML + API + Swagger |
| Models | `accounts/models.py` | `Empresa`, `Perfil`, `Admin` |
| Models | `produtos/models.py` | `Categoria`, `Produto` |
| Models | `vendas/models.py` | `Cliente`, `Venda`, `ItemVenda` |
| Views | `accounts/views.py` | Login, registro, perfil, empresas, senha |
| Views | `produtos/views.py` | CRUD de produtos e categorias |
| Views | `vendas/views.py` | Vendas, faturamento e clientes |
| Views | `core/views.py` | `index`, `about`, `DashboardView` (CBV) |
| Forms | `accounts/forms.py` | Forms + `buscar_ou_criar_empresa` |
| Forms | `produtos/forms.py` | `ProdutoForm` |
| Forms | `vendas/forms.py` | `VendaForm`, `ItemVendaForm`, `ItemVendaFormSet`, `ClienteForm` |
| API | `accounts/api_views.py` | `register_api`, `login_api` |
| API | `produtos/api_views.py` | `ProdutoViewSet` |
| API | `vendas/api_views.py` | `VendaListAPIView`, `FaturamentoAPIView` |
| API | `accounts/serializers.py` | `UserSerializer`, `RegisterSerializer` |
| API | `produtos/serializers.py` | `ProdutoSerializer` |
| API | `vendas/serializers.py` | `VendaSerializer`, `ItemVendaSerializer` |
| API | `accounts/permissions.py` | `IsEmpresaAdmin` |
| API | `accounts/decorators.py` | `admin_required` |
| API | `accounts/context_processors.py` | `is_admin_context` |
| Front | `core/templates/core/base.html` | Layout base |
| Front | `core/static/core/app.css` | Estilos globais |
| Deploy | `Dockerfile`, `build.sh`, `render.yaml` | Container e publicação |
| Docs | `docs/PROJETO.md` | Esta documentação |

---

> **Documento do Projeto Vendas CRM — Trilha de Backend (Django + DRF + JWT + OpenAPI).**
