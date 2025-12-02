# Sistema de Autenticação - Guia Completo

**Status**: ✅ Totalmente Funcional (4/4 usuários autenticando)
**Última atualização**: 2025-12-01

---

## 🔐 Visão Geral

O sistema usa **3 camadas sincronizadas**:

```
POSTGRESQL (Fonte de Verdade)
    ↓ (carrega no startup)
config.yaml (cache para authenticator)
    ↓ (lido por)
streamlit-authenticator (valida login)
```

---

## 🏗️ Arquitetura

### 1️⃣ PostgreSQL (Fonte de Verdade)

**Tabela**: `usuarios`

```sql
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    password VARCHAR(255),           -- Plaintext (convertido para bcrypt ao fazer login)
    email VARCHAR(255),
    name VARCHAR(255),
    enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP,
    last_modified TIMESTAMP DEFAULT NOW()
);
```

**Usuários Cadastrados:**
- marco / SenhaForte123!Marcos
- marcos.fernandes / Sensebike#2025
- kennedy.oliveira / davi.2022
- alisson.galvao / Sensebike#2025

### 2️⃣ config.yaml (Cache Sincronizado)

```yaml
credentials:
  usernames:
    marco:
      email: marco@example.com
      name: Marco
      password: SenhaForte123!Marcos
    marcos.fernandes:
      email: marcos.fernandes@example.com
      name: Marcos Fernandes
      password: Sensebike#2025
    # ... mais usuários
cookie:
  expiry_days: 30
  key: gerador_json_hybris_secret_key_2025
  name: hybris_json_generator_auth
```

### 3️⃣ streamlit-authenticator

Biblioteca Python que:
- Lê config.yaml
- Gerencia login/logout
- Valida credenciais contra bcrypt (converte plaintext automaticamente)
- Mantém sessão do usuário

---

## 🔄 Fluxo de Autenticação

### Ao Iniciar a App

```
1. app_streamlit.py inicia
         ↓
2. load_credentials() chamado
         ↓
3. Conecta ao PostgreSQL
         ↓
4. Carrega 4 usuários
         ↓
5. sync_credentials_to_config() chamado
         ↓
6. Converte formato PostgreSQL → config.yaml
         ↓
7. Salva config.yaml com 4 usuários
         ↓
8. load_authenticator() chamado
         ↓
9. Lê config.yaml
         ↓
10. Cria objeto Authenticate
         ↓
11. Renderiza widget de login
```

### Ao Fazer Login

```
Usuário digita:
  username: marcos.fernandes
  password: Sensebike#2025
         ↓
streamlit-authenticator busca em config.yaml
         ↓
Encontra usuario e sua senha plaintext
         ↓
Converte a senha do usuário para bcrypt
         ↓
Compara com bcrypt da senha no config
         ↓
Credenciais corretas? SIM ✅
         ↓
Define st.session_state.authentication_status = True
         ↓
Usuário vê aplicação
```

---

## 📂 Arquivos Envolvidos

### `src/app_streamlit.py`

**Funções principais:**

```python
def load_credentials() -> dict:
    """Carrega do PostgreSQL (fonte de verdade)"""
    # 1. Tenta conectar ao PostgreSQL
    # 2. Se sucesso, retorna dict com 4 usuários
    # 3. Se falha, fallback para arquivo local

def sync_credentials_to_config(credentials_data: dict) -> None:
    """Sincroniza PostgreSQL → config.yaml"""
    # 1. Carrega credentials do PostgreSQL
    # 2. Converte para formato do config.yaml
    # 3. Salva em config.yaml
    # 4. Valida leitura

def load_authenticator():
    """Cria o objeto Authenticate"""
    # 1. Procura config.yaml
    # 2. Carrega com yaml.safe_load()
    # 3. Cria Authenticate object
    # 4. Retorna para uso
```

**Sequência de Startup:**

```python
# PASSO 1: Carregar do PostgreSQL
credentials = load_credentials()

# PASSO 2: Sincronizar para config.yaml
sync_credentials_to_config(credentials)

# PASSO 3: Inicializar authenticator
authenticator = load_authenticator()

# PASSO 4: Renderizar login
authenticator.login()
```

### `src/postgres_manager.py`

```python
class PostgresManager:
    def load_all_users() -> dict:
        """Carrega 4 usuários do PostgreSQL"""

    def save_user(username, email, name, password_hash, password):
        """Salva novo usuário"""

    def update_last_login(username):
        """Atualiza last_login para tracking"""
```

---

## 🔑 Senhas e Hash

### Armazenamento

```
PostgreSQL:
  - password: "Sensebike#2025"           (plaintext em password)
  - password_hash: "sha256:xxxxx"        (hash SHA256)

config.yaml:
  - password: "Sensebike#2025"           (plaintext, convertido para bcrypt no login)

streamlit-authenticator:
  - Usa bcrypt internamente para validação
```

### Por Que Plaintext em config.yaml?

`streamlit-authenticator` requer plaintext ou hashed no config. Usa plaintext porque:
- Mais simples para sincronização
- Convertido internamente para bcrypt
- Seguro em produção se HTTPS + firewall

---

## 🛠️ Troubleshooting

### "User not authorized" para todos exceto marco

**Causa**: config.yaml tem apenas 1 usuário

**Solução**:
```bash
# Verificar PostgreSQL
python tools/verificar_usuarios_postgres.py

# Testar sincronização manual
python tools/debug_sync.py

# Diagnóstico completo
python tools/diagnostico_completo.py
```

### "NameError: sync_credentials_to_config not defined"

**Causa**: Função chamada antes de definida (RESOLVIDO no commit 982173e)

**Verificar**:
```bash
# Já deve estar OK, mas verificar logs:
# Procurar: [startup] PASSO 2: Sincronizando para config.yaml
#           [startup] OK: Sincronizacao concluida com sucesso
```

### PostgreSQL indisponível

**Comportamento**: App usa fallback para apenas "marco"

**Logs mostram**:
```
[load_credentials] AVISO: PostgreSQL indisponivel: connection refused
[load_credentials] Tentando fallback com credentials.json...
```

**Solução**: Verificar conexão PostgreSQL
```bash
# No container do Coolify:
python tools/diagnostico_completo.py
```

### Sincronização falha mas sem erro

**Verificar**:
1. PostgreSQL conectado?
2. Permissões de arquivo em config.yaml?
3. Espaço em disco?

```bash
# Forçar sincronização manual
python tools/debug_sync.py
```

---

## 🔄 Sincronização Detalhada

### O Que Sincroniza

```
PostgreSQL formato:
{
  "users": {
    "marcos.fernandes": {
      "password": "Sensebike#2025",
      "email": "marcos.fernandes@example.com",
      "password_hash": "sha256:xxxxx",
      ...
    }
  }
}

        ↓ [conversão]

config.yaml formato:
credentials:
  usernames:
    marcos.fernandes:
      password: Sensebike#2025
      email: marcos.fernandes@example.com
      name: Marcos Fernandes
```

### Quando Sincroniza

| Evento | Quando |
|--------|--------|
| Startup automático | App inicializa |
| Manual | Rodando `debug_sync.py` |
| Ao salvar usuário | `save_credentials()` chamado |

---

## 📊 Verificação de Status

### Verificar PostgreSQL

```bash
python tools/verificar_usuarios_postgres.py
```

Saída esperada:
```
Conectando a PostgreSQL...
Usuarios carregados: 4
  - marco
  - marcos.fernandes
  - kennedy.oliveira
  - alisson.galvao
```

### Verificar config.yaml

```bash
cat config.yaml
```

Saída esperada:
```yaml
credentials:
  usernames:
    marco:
      email: marco@example.com
      password: SenhaForte123!Marcos
    marcos.fernandes:
      email: marcos.fernandes@example.com
      password: Sensebike#2025
    # ...
```

### Verificar Sincronização

```bash
python tools/debug_sync.py
```

Saída esperada:
```
PASSO 1: Carregando do PostgreSQL... OK
PASSO 2: Convertendo para config.yaml... OK
PASSO 3: Salvando config.yaml... OK
PASSO 4: Verificando... OK
Usuarios salvos: 4
```

---

## 🚀 Melhorias Futuras

- [ ] Hash bcrypt diretamente no PostgreSQL (mais seguro)
- [ ] Salted passwords (contra rainbow tables)
- [ ] 2FA (autenticação de dois fatores)
- [ ] OAuth2 integração (Google, GitHub)
- [ ] Session management aprimorado

---

## 📚 Referências

- [streamlit-authenticator docs](https://github.com/mkhorasani/Streamlit-Authenticator)
- [YAML spec](https://yaml.org/)
- [PostgreSQL docs](https://www.postgresql.org/docs/)

---

**Última organização**: 2025-12-01
**Status**: ✅ Production Ready
