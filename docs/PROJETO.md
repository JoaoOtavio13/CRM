# 📘 CRM de Vendas — Documentação do Projeto

> **Projeto:** Vendas_CRM
> **Framework:** Django 6.0.7 + Django REST Framework 3.17.1
> **Autenticação API:** JWT (djangorestframework-simplejwt 5.5.1)
> **Documentação API:** drf-spectacular 0.28.0 (OpenAPI 3.0 + Swagger UI)
> **Frontend:** Templates Django + Bootstrap (via herança de templates)
> **Projeto acadêmico** - Trilha de Backend
> **Objetivo:** Sistema CRM para empresas de varejo, com gestão de produtos, clientes, vendas, estoque e faturamento.

---

## 📋 Visão Geral do Sistema

O CRM de Vendas é um sistema completo para gestão comercial de pequenas e médias empresas de varejo. Ele permite:

- **Autenticação e perfis de usuário:** login/logout, registro de conta, perfil com dados pessoais e vinculação a uma empresa.
- **Gestão de empresas e admins:** cada empresa tem um usuário administrador (dono) que controla produtos, vendas e faturamento.
- **Catálogo de produtos:** criação, edição, exclusão de produtos com nome, descrição, preço, estoque e imagem, organizando-os em categorias.
- **Vendas:** registro de vendas com itens, atualização automática de estoque e cálculo de total faturado.
- **Clientes:** cadastro de clientes vinculados ao usuário.
- **Faturamento:** visualização do total faturado (acesso restrito ao dono da empresa).
- **API REST:** endpoints para criação de conta, login (JWT), CRUD de produtos, listagem de vendas e faturamento.
- **Documentação OpenAPI:** Swagger UI interativo para explorar e testar a API.

---

## ⚙️ 1. Criação do Ambiente Virtual

O projeto usa Python **3.12.10** (definido em __python-version e no Dockerfile baseado em python:3.12-slim).

### Passo a passo

`ash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
pip install -r requirements.txt
`

### Dependências (
equirements.txt)

| Pacote | Versão | Uso |
|--------|--------|-----|
| Django | 6.0.7 | Framework web principal |
| djangorestframework | 3.17.1 | API REST |
| djangorestframework-simplejwt | 5.5.1 | Tokens JWT para autenticação |
| drf-spectacular | 0.28.0 | Geração automática de schema OpenAPI 3.0 + Swagger UI |
| python-decouple | 3.8 | Leitura de variáveis de ambiente do arquivo .env |
| dj-database-url | 3.1.2 | Conexão com banco de dados via URL (PostgreSQL no Render) |
| cloudinary | 1.46.2 | Armazenamento de imagens em produção (uploads de produtos/perfis) |
| psycopg[binary] | 3.3.5 | Driver PostgreSQL para produção |
| gunicorn | 26.2.0 | Servidor WSGI para produção (Render) |
| whitenoise | 6.12.0 | Servir arquivos estáticos em produção |
| Pillow | 12.3.0 | Manipulação de imagens (upload de produtos/perfis) |
| PyJWT | 2.13.0 | Manipulação de tokens JWT (usado pelo simplejwt) |
| asgiref | 3.12.1 | Compatibilidade ASGI para Django |
| sqlparse | 0.5.5 | Parser SQL (depêndencia do Django) |
| tzdata | 2026.3 | Dados de fusos horários |

| **Parte 4.1 ✅** | Ambiente virtual criado com env, dependências versionadas em 
equirements.txt |

---

