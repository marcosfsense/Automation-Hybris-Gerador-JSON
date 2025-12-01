# Gestão de Usuários e PostgreSQL

## Status Atual (2025-12-01)

### ✨ SINCRONIZAÇÃO AUTOMÁTICA IMPLEMENTADA - VERSÃO 2.0

A gestão de usuários **agora é 100% integrada** com PostgreSQL. Todas as operações são feitas pela interface Streamlit e sincronizadas automaticamente com o banco de dados.

**🔧 Novo na v2.0**: Sincronização automática no startup da aplicação. Usuários do PostgreSQL são carregados automaticamente quando a aplicação inicia.

---

## Como Funciona

### 📋 Operações de Usuários (via Interface Streamlit)

Acesse: **"👥 Gerenciar Usuários"** no menu lateral

#### ➕ Criar Usuário
1. Preencha: Username, Senha, Email (opcional)
2. Clique em **"✅ Criar Usuário"**
3. Automático:
   - ✅ Salva em `credentials.json` (backup local)
   - ✅ Salva em PostgreSQL (fonte de verdade)
   - ✅ Sincroniza com `config.yaml`

#### 📋 Listar Usuários
- Mostra todos os usuários cadastrados
- Informações: Username, Status, Data de criação, Último acesso
- Sincronizado com PostgreSQL

#### 🔑 Alterar Senha
1. Selecione o usuário
2. Defina nova senha
3. Automático:
   - ✅ Atualiza em ambos: arquivo + banco
   - ✅ Hash SHA256 gerado automaticamente

#### ❌ Remover Usuário
1. Selecione o usuário
2. Confirme remoção
3. Automático:
   - ✅ Remove de `credentials.json`
   - ✅ Remove de PostgreSQL
   - ✅ Sincroniza em `config.yaml`

### 🔄 Sincronização Automática

**Ao criar/editar/remover usuário:**
```
Interface Streamlit
       ↓
credentials.json (backup)
       ↓
PostgreSQL (FONTE DE VERDADE)
       ↓
config.yaml (sync)
```

**Ao fazer login:**
```
PostgreSQL atualiza last_login
    ↓
Timestamp registrado com precisão
```

**Ao fazer redeploy:**
```
Aplicação inicia (startup)
    ↓
load_credentials() ativada
    ↓
Tenta carregar arquivo credentials.json
    ↓
✨ SINCRONIZAÇÃO CRÍTICA:
Carrega usuários do PostgreSQL (FONTE DE VERDADE)
    ↓
Mescla: PostgreSQL + arquivo local
    ↓
Atualiza credentials.json com dados do PostgreSQL
    ↓
Usuários autenticados e disponíveis ✅
```

**Importante**: Se PostgreSQL estiver indisponível, aplicação usa dados do arquivo local como fallback.

---

## Arquitetura

### PostgreSQL Manager (`src/postgres_manager.py`)

Novo módulo que gerencia:
- ✅ Conexão com PostgreSQL
- ✅ Criar/atualizar/deletar usuários
- ✅ Sincronizar credenciais
- ✅ Rastrear `last_login`
- ✅ Garantir tabela existe

### Integração na Aplicação (`src/app_streamlit.py`)

Modificações:
1. **Import**: `from postgres_manager import PostgresManager`
2. **save_credentials()**: Agora sincroniza com PostgreSQL
3. **delete_user()**: Remove de ambos banco e arquivo
4. **login()**: Atualiza `last_login` no PostgreSQL

---

## Fluxo de Dados

```
┌─────────────────────────────┐
│   Interface Streamlit       │
│  (Gerenciar Usuários)       │
└────────────┬────────────────┘
             │
             ↓
┌─────────────────────────────┐
│  PostgreSQL Manager         │
│  (sync automático)          │
└────────────┬────────────────┘
             │
    ┌────────┴────────┐
    ↓                 ↓
┌──────────┐    ┌─────────────┐
│PostgreSQL│    │credentials  │
│(Verdade) │    │.json(Backup)│
└──────────┘    └─────────────┘
```

---

## Vantagens da Solução

✅ **Nenhum usuário será mais perdido** em redeploys
✅ **Interface única** para gerenciar usuários
✅ **Sem scripts Python** necessários (tudo na UI)
✅ **Backup automático** em arquivo local
✅ **Auditoria** com `last_login` no banco
✅ **Recuperação automática** de falhas
✅ **PostgreSQL é fonte de verdade**

---

## Próximas Ações

### 1️⃣ Recriar Usuários Perdidos

Acesse a aplicação → **👥 Gerenciar Usuários** → **➕ Criar Usuário**

Recrie:
- `kennedy.oliveira`
- `alisson.galvao`
- `marcos.fernandes`

### 2️⃣ Verificar Sincronização

Após criar, execute no Coolify:
```bash
cd /app && python verificar_usuarios_postgres.py
```

Você verá todos os usuários salvos no PostgreSQL.

### 3️⃣ Pronto!

Agora a sincronização é automática. Qualquer operação de usuário:
- ✅ Salva no arquivo
- ✅ Sincroniza no banco
- ✅ Persiste em redeploys

---

## Variáveis de Ambiente (Opcional)

Se quiser customizar conexão PostgreSQL, use:

```bash
DB_HOST=seu-host
DB_PORT=5432
DB_NAME=postgres
DB_USER=seu-usuario
DB_PASSWORD=sua-senha
```

Padrão (pré-configurado):
- Host: `u48cw44ccwg4sowco4044goc`
- Port: `5432`
- User: `postgres`

---

## Resumo

| Operação | Antes | Agora (v2.0) |
|----------|-------|-------|
| Criar usuário | Arquivo apenas | Arquivo + PostgreSQL ✅ |
| Editar senha | Arquivo apenas | Arquivo + PostgreSQL ✅ |
| Remover usuário | Arquivo apenas | Arquivo + PostgreSQL ✅ |
| Rastrear login | Nenhum | PostgreSQL (last_login) ✅ |
| Redeploy | Usuários perdidos ❌ | **Sincronização automática ✅** |
| Startup | Arquivo apenas | **PostgreSQL + Arquivo ✅** |
| Fallback | N/A | **Arquivo se PostgreSQL indisponível ✅** |
| Interface | Sim | Sim (tudo aqui!) ✅ |

---

## Mudanças da v2.0

### ✅ Sincronização de Startup

A aplicação agora sincroniza automaticamente com PostgreSQL quando inicia:

1. **load_credentials()** agora carrega do PostgreSQL
2. **Prioridade**: PostgreSQL é fonte de verdade
3. **Fallback**: Se PostgreSQL indisponível, usa arquivo local
4. **Mesclagem**: Combina dados do banco com arquivo para máxima segurança

### 📋 Métodos Atualizados

- `load_all_users()` - Agora retorna formato `{"users": {...}}`
- `load_credentials()` - Agora sincroniza com PostgreSQL no startup

**Resultado: Problema permanentemente resolvido! 🎉**
