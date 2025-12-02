# Conectar ao PostgreSQL via DBeaver

**Status**: Guia completo passo-a-passo
**Data**: 2025-12-02

---

## 📊 Informações de Conexão

Extraídas do arquivo `src/postgres_manager.py`:

```
Host:     u48cw44ccwg4sowco4044goc
Port:     5432
Database: postgres
User:     postgres
Password: poMaf572450+@
```

---

## 🚀 Passo-a-Passo no DBeaver

### 1️⃣ Abrir DBeaver

- Clique em **File** → **New Database Connection**
- Ou pressione **Ctrl+N**
- Ou clique no ícone **+** na aba "Database"

---

### 2️⃣ Selecionar PostgreSQL

Na janela "New Database Connection":

- Procure por **PostgreSQL**
- Clique em **PostgreSQL** (não PostgreSQL JDBC)
- Clique **Next >**

---

### 3️⃣ Configurar Conexão

Preencha com as informações abaixo:

```
Server Host:    u48cw44ccwg4sowco4044goc
Port:           5432
Database:       postgres
Username:       postgres
Password:       poMaf572450+@
```

**Campos específicos no DBeaver:**

| Campo | Valor |
|-------|-------|
| **Server Host** | `u48cw44ccwg4sowco4044goc` |
| **Port** | `5432` |
| **Database** | `postgres` |
| **Username** | `postgres` |
| **Password** | `poMaf572450+@` |

---

### 4️⃣ Verificar Conexão

Clique no botão **"Test Connection"**

**Esperado ver:**
```
✅ Connected
Successfully connected to PostgreSQL database
```

Se der erro, verifique:
- ✅ Host correto? `u48cw44ccwg4sowco4044goc`
- ✅ Porta aberta? `5432`
- ✅ Usuário e senha corretos?
- ✅ VPS/Firewall permite conexão de fora?

---

### 5️⃣ Finalizando

- Clique **Finish**
- A conexão aparecerá na aba "Databases"

---

## 📋 Estrutura do Banco

Após conectar, você verá:

```
u48cw44ccwg4sowco4044goc (banco)
└── postgres (database)
    └── Schemas
        └── public
            └── Tables
                ├── usuarios          ← TABELA PRINCIPAL
                └── (índices)
```

---

## 👥 Tabela de Usuários

### Campos da Tabela `usuarios`

```sql
SELECT * FROM usuarios;
```

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | SERIAL | ID único (chave primária) |
| `username` | VARCHAR | Nome de login (ÚNICO) |
| `email` | VARCHAR | Email do usuário |
| `name` | VARCHAR | Nome completo |
| `password_hash` | VARCHAR | Hash SHA256 da senha |
| `password` | VARCHAR | Senha em plaintext |
| `enabled` | BOOLEAN | Usuário ativo? |
| `created_at` | TIMESTAMP | Data de criação |
| `last_login` | TIMESTAMP | Último acesso |
| `last_modified` | TIMESTAMP | Última modificação |
| `updated_at` | TIMESTAMP | Última atualização |

### Usuários Cadastrados

```sql
SELECT username, email, enabled, created_at FROM usuarios;
```

**Esperado encontrar:**

| username | email | enabled | created_at |
|----------|-------|---------|------------|
| marco | marco@example.com | true | 2025-... |
| marcos.fernandes | marcos.fernandes@example.com | true | 2025-... |
| kennedy.oliveira | kennedy.oliveira@example.com | true | 2025-... |
| alisson.galvao | alisson.galvao@example.com | true | 2025-... |

---

## 🔍 Consultas Úteis

### Ver todos os usuários

```sql
SELECT username, email, name, enabled
FROM usuarios
ORDER BY created_at DESC;
```

### Ver último acesso de cada usuário

```sql
SELECT username, last_login
FROM usuarios
ORDER BY last_login DESC;
```

### Contar usuários ativos

```sql
SELECT COUNT(*) as total_usuarios
FROM usuarios
WHERE enabled = true;
```

### Ver usuário específico

```sql
SELECT * FROM usuarios
WHERE username = 'marcos.fernandes';
```

### Atualizar senha de um usuário

```sql
UPDATE usuarios
SET password = 'nova_senha_aqui'
WHERE username = 'marcos.fernandes';
```

### Ver estrutura da tabela

```sql
\d usuarios
```

---

## 🔒 Segurança - IMPORTANTE!

⚠️ **Nunca compartilhe**:
- Host: `u48cw44ccwg4sowco4044goc`
- User: `postgres`
- Password: `poMaf572450+@`

Estas informações estão em:
- `src/postgres_manager.py` (hardcoded)
- `src/app_streamlit.py` (carregado ao iniciar)

**Recomendação**: Usar variáveis de ambiente (`.env`) em produção.

---

## 🆘 Troubleshooting

### ❌ "Connection refused"

**Causa**: Porta 5432 fechada ou VPS não permite acesso

**Solução**:
1. Verificar se PostgreSQL está rodando na VPS
2. Verificar firewall: porta 5432 aberta?
3. Verificar se host está correto: `u48cw44ccwg4sowco4044goc`

### ❌ "FATAL: password authentication failed"

**Causa**: Senha incorreta

**Solução**: Usar exatamente: `poMaf572450+@` (com o `@` e `+`)

### ❌ "Unknown host"

**Causa**: Host não resolve

**Solução**: Verificar se é domínio ou IP
- Se for domínio: precisa de DNS funcional
- Se for IP: usar o IP direto

### ❌ "Connection timeout"

**Causa**: Network/firewall bloqueando

**Solução**:
1. Testar ping: `ping u48cw44ccwg4sowco4044goc`
2. Testar porta: `telnet u48cw44ccwg4sowco4044goc 5432`
3. Verificar VPS firewall rules

---

## 📖 Recursos Adicionais

- [DBeaver Official Docs](https://dbeaver.io/docs/)
- [PostgreSQL Connection Guide](https://www.postgresql.org/docs/current/libpq-connect.html)
- [DBeaver PostgreSQL Setup](https://github.com/dbeaver/dbeaver/wiki/PostgreSQL)

---

## 💡 Dicas Úteis

### Salvar Connection

DBeaver salva automaticamente. Para acessar depois:
- Aba "Databases" na esquerda
- Expansão `u48cw44ccwg4sowco4044goc`
- Clique duas vezes para conectar

### Executar Query

1. Clique com direito na conexão
2. **SQL Editor** → **New SQL Script**
3. Cole a query
4. Pressione **Ctrl+Enter** para executar

### Adicionar Favorito

- Clique com direito na tabela
- **Add to Favorites**
- Aparecerá em "Favorites" no topo

### Exportar Dados

- Clique com direito na tabela
- **Export Data** → JSON/CSV/Excel
- Escolha formato e destino

---

**Status**: ✅ Pronto para usar
**Última atualização**: 2025-12-02
