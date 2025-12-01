# Gestão de Usuários e PostgreSQL

## Status Atual (2025-12-01)

### ✨ SINCRONIZAÇÃO AUTOMÁTICA IMPLEMENTADA - VERSÃO 3.0

A gestão de usuários **agora é 100% integrada** com PostgreSQL. Todas as operações são feitas pela interface Streamlit e sincronizadas automaticamente com o banco de dados.

**🔧 Novo na v3.0**:
- PostgreSQL é a **ÚNICA e exclusiva fonte de verdade**
- Sem mescla desnecessária com arquivo local
- Tratamento melhorado de erros de autenticação com botões de "Tentar Novamente"
- Ordem de inicialização corrigida para sincronização perfeita

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
✨ PASSO 1: load_credentials() carrega DO PostgreSQL
    ↓
✨ PASSO 2: sync_credentials_to_config() converte para config.yaml
    ↓
✨ PASSO 3: load_authenticator() inicializado com dados sincronizados
    ↓
Usuários carregados do PostgreSQL (ÚNICA fonte) ✅
    ↓
authenticator pronto para receber login ✅
```

**Fallback Inteligente:**
- PostgreSQL indisponível? Usa arquivo local como backup
- Erro de autenticação? Botão "Tentar Novamente" ou "Limpar Dados"

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

| Operação | Antes | v2.0 | v3.0 (Atual) |
|----------|-------|------|------|
| Criar usuário | Arquivo apenas | Arquivo + PostgreSQL ✅ | PostgreSQL ✅ |
| Editar senha | Arquivo apenas | Arquivo + PostgreSQL ✅ | PostgreSQL ✅ |
| Remover usuário | Arquivo apenas | Arquivo + PostgreSQL ✅ | PostgreSQL ✅ |
| Rastrear login | Nenhum | PostgreSQL (last_login) ✅ | PostgreSQL (last_login) ✅ |
| Redeploy | Usuários perdidos ❌ | Mescla (PostgreSQL + arquivo) | **Apenas PostgreSQL ✅** |
| Startup | Arquivo apenas | PostgreSQL + mescla | **PostgreSQL direto ✅** |
| Fallback | N/A | Arquivo se DB indisponível | **Arquivo se DB indisponível ✅** |
| Erro Autenticação | Nenhuma opção ❌ | Nenhuma opção ❌ | **Botões "Tentar" e "Limpar" ✅** |
| Interface | Sim | Sim ✅ | Sim ✅ |

---

## Mudanças da v3.0

### ✅ PostgreSQL como ÚNICA Fonte de Verdade

**Antes (v2.0)**: Mescla de PostgreSQL + arquivo local (complexo, inconsistências)

**Agora (v3.0)**:
- PostgreSQL = ÚNICA e exclusiva fonte de dados
- Arquivo JSON = APENAS fallback se PostgreSQL indisponível
- Sem mesclas desnecessárias
- Dados sempre consistentes

### ✅ Ordem de Inicialização Corrigida

```
v2.0: credentials ← arquivo → authenticator (dados desatualizados)
v3.0: PostgreSQL → credentials → config.yaml → authenticator ✅
```

### ✅ Tratamento de Erros de Autenticação

- Erro ao fazer login? Botão **"🔄 Tentar Novamente"**
- Session state corrompido? Botão **"🔓 Limpar Dados"**
- Interface amigável para resolver problemas

### 📋 Métodos Atualizados

- `load_credentials()` - Agora carrega APENAS de PostgreSQL
- `authenticator.login()` - Com tratamento melhorado de exceções

**Resultado: Solução robusta e consistente! 🎉**
