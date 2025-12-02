# Estrutura do Projeto - Gerador JSON Hybris

**Última atualização**: 2025-12-01 (Organização profissional e consolidação)

---

## 📂 Estrutura de Diretórios

```
AUTOMAÇÃO HYBRIS - GERADOR DE JSONs/
│
├── 📄 README.md                          # 📌 COMECE AQUI - Documentação principal
├── 📄 CLAUDE.md                          # Instruções para Claude Code
├── 📄 requirements.txt                   # Dependências Python
│
├── 📁 src/                               # 🔧 Código-fonte principal
│   ├── app_streamlit.py                  # Aplicação web principal
│   ├── hybris_json_generator.py          # Gerador de JSONs
│   ├── postgres_manager.py               # Gerenciador PostgreSQL
│
├── 📁 tools/                             # 🛠️ Ferramentas de diagnóstico e manutenção
│   ├── diagnostico_completo.py           # Diagnóstico completo das 3 camadas
│   ├── debug_sync.py                     # Teste manual de sincronização
│   ├── debug_marcos.py                   # Debug específico para marcos
│   ├── verificar_usuarios_postgres.py    # Verificação de usuários no BD
│   ├── migrate_users_to_postgres.py      # Migração de usuários para PostgreSQL
│
├── 📁 docs/                              # 📚 Documentação completa
│   ├── ESTRUTURA_PROJETO.md              # Este arquivo
│   ├── GUIA_INSTALACAO.md                # Como instalar e configurar
│   ├── GUIA_USO.md                       # Como usar a aplicação
│   ├── AUTENTICACAO.md                   # Sistema de autenticação (PostgreSQL + config.yaml)
│   ├── TROUBLESHOOTING.md                # Resolução de problemas
│   ├── CHANGELOG.md                      # Histórico de versões
│
├── 📁 examples/                          # 📋 Exemplos de saída
│   ├── exemplo_pix.txt
│   ├── exemplo_debito.txt
│   ├── exemplo_credito.txt
│   ├── exemplo_multiplas.txt
│
├── 📁 venv/                              # 🐍 Ambiente virtual Python (ignorado)
│
└── 📄 config.yaml                        # ⚙️ Autenticação (gerado automaticamente)
    credentials.json                      # 🔐 Credenciais backup (gerado automaticamente)
    usuarios_log.txt                      # 📋 Log de ações de usuários (gerado)
```

---

## 📌 Arquivos Principais

### Código-fonte (`src/`)

| Arquivo | Responsabilidade |
|---------|------------------|
| `app_streamlit.py` | Aplicação web completa com autenticação e interface |
| `hybris_json_generator.py` | Gerador de JSONs para todos os tipos de transação |
| `postgres_manager.py` | Gerenciam conexão e operações no PostgreSQL |

### Ferramentas (`tools/`)

| Script | Uso |
|--------|-----|
| `diagnostico_completo.py` | Diagnosticar problema de autenticação (3 camadas) |
| `debug_sync.py` | Testar sincronização manual PostgreSQL → config.yaml |
| `debug_marcos.py` | Debug específico |
| `verificar_usuarios_postgres.py` | Verificar usuários no PostgreSQL |
| `migrate_users_to_postgres.py` | Migrar usuários do arquivo para PostgreSQL |

### Documentação (`docs/`)

| Documento | Conteúdo |
|-----------|----------|
| `ESTRUTURA_PROJETO.md` | Este arquivo - mapa do projeto |
| `GUIA_INSTALACAO.md` | Setup inicial e configuração |
| `GUIA_USO.md` | Como usar a aplicação |
| `AUTENTICACAO.md` | Detalhes do sistema de autenticação |
| `TROUBLESHOOTING.md` | Resolução de problemas comuns |
| `CHANGELOG.md` | Histórico de versões |

---

## 🚀 Quick Start

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Configurar PostgreSQL
```bash
python tools/migrate_users_to_postgres.py
```

### 3. Rodar a aplicação
```bash
streamlit run src/app_streamlit.py
```

### 4. Acessar no navegador
```
http://localhost:8501
```

---

## 🔐 Sistema de Autenticação

**Componentes:**

```
PostgreSQL (Fonte de Verdade)
    ↓
    └─→ app_streamlit.py (carrega no startup)
            ↓
            └─→ config.yaml (sincroniza automaticamente)
                    ↓
                    └─→ streamlit-authenticator (autentica usuários)
```

**Fluxo de Login:**

1. App inicia e carrega usuários do PostgreSQL
2. Sincroniza para config.yaml
3. Autenticador lê config.yaml
4. Usuário faz login no Streamlit
5. Credenciais validadas contra config.yaml

**Veja**: `docs/AUTENTICACAO.md` para mais detalhes.

---

## 🛠️ Troubleshooting Rápido

### "User not authorized"
```bash
# Verificar se usuário existe no PostgreSQL
python tools/verificar_usuarios_postgres.py

# Testar sincronização manualmente
python tools/debug_sync.py

# Diagnóstico completo
python tools/diagnostico_completo.py
```

### Problema de sincronização
```bash
# Verificar se PostgreSQL está acessível
python tools/diagnostico_completo.py
```

**Veja**: `docs/TROUBLESHOOTING.md` para mais cenários.

---

## 📦 Dependências Principais

```
streamlit              # Framework web
streamlit-authenticator # Autenticação
psycopg2              # Driver PostgreSQL
pyyaml                # Parsing YAML
```

**Arquivo**: `requirements.txt`

---

## 🔄 Arquitetura

### Camada de Dados
- PostgreSQL: Fonte de verdade para credenciais
- config.yaml: Cache/sincronização para authenticator
- credentials.json: Backup local

### Camada de Aplicação
- app_streamlit.py: Aplicação principal (interface + autenticação)
- hybris_json_generator.py: Gerador de JSONs
- postgres_manager.py: Acesso ao banco

### Camada de Ferramentas
- Scripts de diagnóstico para troubleshooting
- Scripts de migração para setup inicial

---

## 📋 Commits Importantes

| Commit | Descrição |
|--------|-----------|
| 982173e | Fix crítico - Reorganizar estrutura de startup |
| 3a201b8 | Documentar sucesso final - Autenticação 100% funcional |
| e8abd12 | Melhorias em Dockerfile |

---

## ✅ Checklist de Setup

- [ ] Python 3.7+ instalado
- [ ] PostgreSQL acessível
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Usuários migrados para PostgreSQL
- [ ] `streamlit run src/app_streamlit.py` rodando
- [ ] Login funcional para todos os usuários
- [ ] Logs mostram sincronização bem-sucedida

---

## 🤝 Contribuindo

Ao fazer mudanças:

1. Comente o código se lógica for complexa
2. Atualize documentação se funcionalidade mudar
3. Execute `tools/diagnostico_completo.py` antes de commitar
4. Use mensagens de commit claras

---

## 📞 Suporte

**Problema?** Veja `docs/TROUBLESHOOTING.md` primeiro.

**Entender autenticação?** Leia `docs/AUTENTICACAO.md`.

**Setup inicial?** Siga `docs/GUIA_INSTALACAO.md`.

---

**Última organização**: 2025-12-01
**Status**: ✅ Produção-ready
