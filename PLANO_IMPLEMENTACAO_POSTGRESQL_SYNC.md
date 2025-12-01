# Plano de Implementação: Sincronização PostgreSQL

## 🎯 Objetivo

Implementar sincronização automática entre a aplicação Streamlit e PostgreSQL para que **nenhum usuário seja perdido em redeploys futuros**.

## 📊 Status Atual

| Item | Status | Detalhe |
|------|--------|---------|
| PostgreSQL | ✅ Funcionando | `u48cw44ccwg4sowco4044goc:5432` |
| Tabela `usuarios` | ✅ Criada | Schema completo pronto |
| Usuários no BD | ✅ 1 usuário | Apenas "marco" |
| Sync no app | ❌ Não existe | Precisamos implementar |

## 🔧 Implementação

### Etapa 1: Funções de Banco de Dados (Nova)

**Arquivo:** `src/postgres_manager.py` (NOVO)

```python
import psycopg2
from psycopg2 import sql
from datetime import datetime
import json

class PostgresManager:
    """Gerencia operações com PostgreSQL"""

    DB_CONFIG = {
        'host': 'u48cw44ccwg4sowco4044goc',
        'port': 5432,
        'database': 'postgres',
        'user': 'postgres',
        'password': 'poMaf572450+@'
    }

    @staticmethod
    def get_connection():
        """Obtém conexão com PostgreSQL"""
        return psycopg2.connect(**PostgresManager.DB_CONFIG)

    @staticmethod
    def load_all_users():
        """
        Carrega TODOS os usuários do PostgreSQL
        Retorna dict no formato de credentials.json
        """
        try:
            conn = PostgresManager.get_connection()
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT username, password_hash, password, email, name,
                           enabled, created_at, last_login, last_modified
                    FROM usuarios
                    ORDER BY created_at
                """)
                users = {}
                for row in cur.fetchall():
                    username, password_hash, password, email, name, enabled, \
                    created_at, last_login, last_modified = row

                    users[username] = {
                        'password_hash': password_hash or '',
                        'password': password or '',
                        'email': email or '',
                        'name': name or username,
                        'enabled': enabled,
                        'created_at': created_at.isoformat() if created_at else None,
                        'last_login': last_login.isoformat() if last_login else None,
                        'last_modified': last_modified.isoformat() if last_modified else None
                    }
                conn.close()
                return users
        except Exception as e:
            print(f"❌ Erro ao carregar usuários do PostgreSQL: {e}")
            return {}

    @staticmethod
    def save_user(username, email, name, password_hash, password, enabled=True):
        """
        Salva/atualiza um usuário no PostgreSQL
        """
        try:
            conn = PostgresManager.get_connection()
            with conn.cursor() as cur:
                sql_upsert = """
                INSERT INTO usuarios (username, email, name, password_hash, password, enabled)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (username) DO UPDATE SET
                    email = EXCLUDED.email,
                    name = EXCLUDED.name,
                    password_hash = EXCLUDED.password_hash,
                    password = EXCLUDED.password,
                    enabled = EXCLUDED.enabled,
                    updated_at = CURRENT_TIMESTAMP
                """
                cur.execute(sql_upsert, (username, email, name, password_hash, password, enabled))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ Erro ao salvar usuário no PostgreSQL: {e}")
            return False

    @staticmethod
    def delete_user(username):
        """
        Delete usuário do PostgreSQL
        """
        try:
            conn = PostgresManager.get_connection()
            with conn.cursor() as cur:
                cur.execute("DELETE FROM usuarios WHERE username = %s", (username,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ Erro ao deletar usuário do PostgreSQL: {e}")
            return False

    @staticmethod
    def update_last_login(username):
        """
        Atualiza last_login após login bem-sucedido
        """
        try:
            conn = PostgresManager.get_connection()
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE usuarios
                    SET last_login = CURRENT_TIMESTAMP,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE username = %s
                """, (username,))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"⚠️  Erro ao atualizar last_login: {e}")
```

### Etapa 2: Integração no app_streamlit.py

**Localização:** `src/app_streamlit.py` - Modificar `load_authenticator()` e `load_credentials()`

**Antes (❌ Antigo):**
```python
def load_credentials():
    """Carrega credentials.json do arquivo local"""
    global credentials_data

    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, 'r', encoding='utf-8') as f:
            credentials_data = json.load(f)
    else:
        credentials_data = {"users": {}}
```

**Depois (✅ Novo):**
```python
def load_credentials():
    """Carrega credentials do PostgreSQL (com fallback para arquivo)"""
    global credentials_data

    # 1️⃣ Tentar carregar do PostgreSQL (FONTE DE VERDADE)
    from src.postgres_manager import PostgresManager
    users_from_db = PostgresManager.load_all_users()

    if users_from_db:
        # ✅ Usuários encontrados no banco
        credentials_data = {"users": users_from_db}
        print(f"✅ Carregados {len(users_from_db)} usuários do PostgreSQL")

    # 2️⃣ Se nenhum usuário no BD, carregar do arquivo (backup)
    elif os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, 'r', encoding='utf-8') as f:
            file_data = json.load(f)
            credentials_data = file_data
            # Sincronizar arquivo para BD também
            for username, user_info in credentials_data.get("users", {}).items():
                PostgresManager.save_user(
                    username,
                    user_info.get('email', ''),
                    user_info.get('name', username),
                    user_info.get('password_hash', ''),
                    user_info.get('password', '')
                )
        print(f"✅ Carregados {len(credentials_data.get('users', {}))} usuários do arquivo (sincronizados para BD)")

    # 3️⃣ Se nada encontrado, começar vazio
    else:
        credentials_data = {"users": {}}
        print("ℹ️  Nenhum usuário encontrado - começando vazio")
```

### Etapa 3: Hooks de Criação/Modificação de Usuários

**Em `save_credentials()`** - Adicionar sincronização com BD:

```python
def save_credentials(log_action=None):
    """Salva credentials em arquivo E PostgreSQL"""
    global credentials_data

    # 1. Salvar no arquivo local (backup)
    with open(CREDENTIALS_FILE, 'w', encoding='utf-8') as f:
        json.dump(credentials_data, f, indent=2, ensure_ascii=False)

    # 2. Sincronizar com PostgreSQL
    from src.postgres_manager import PostgresManager
    for username, user_info in credentials_data.get("users", {}).items():
        PostgresManager.save_user(
            username,
            user_info.get('email', ''),
            user_info.get('name', username),
            user_info.get('password_hash', ''),
            user_info.get('password', '')
        )

    # 3. Log de auditoria
    if log_action:
        log_user_action(log_action)

    print(f"✅ Dados salvos em arquivo e sincronizados com PostgreSQL")
```

### Etapa 4: Atualizar Hooks de Login

**Após login bem-sucedido:**

```python
# No callback do login bem-sucedido
from src.postgres_manager import PostgresManager

if authenticator.login('login_widget', 'main'):
    # ... código existente ...

    # ✅ Atualizar last_login no PostgreSQL
    PostgresManager.update_last_login(st.session_state.username)

    print(f"✅ {st.session_state.username} logou com sucesso")
```

## 📋 Checklist de Implementação

### Fase 1: Preparação
- [ ] Criar arquivo `src/postgres_manager.py` com classe `PostgresManager`
- [ ] Testar conexão com PostgreSQL
- [ ] Testar load_all_users() retorna dados corretos

### Fase 2: Integração na Aplicação
- [ ] Modificar `load_credentials()` em app_streamlit.py
- [ ] Modificar `save_credentials()` para sincronizar com BD
- [ ] Adicionar `update_last_login()` no callback de login
- [ ] Testar carregamento de usuários

### Fase 3: Validação
- [ ] Criar novo usuário na interface
- [ ] Verificar que aparece no PostgreSQL
- [ ] Fazer redeploy
- [ ] Verificar que usuário ainda existe
- [ ] Fazer login com novo usuário
- [ ] Verificar que last_login foi atualizado

### Fase 4: Limpeza
- [ ] Remover código antigo de sincronização credentials.json ↔ config.yaml (não mais necessário)
- [ ] Atualizar documentação
- [ ] Commitar changes

## 🧪 Testes

**Teste 1: Novo usuário sobrevive a redeploy**
```
1. Criar usuário "teste123"
2. Verificar em PostgreSQL: SELECT * FROM usuarios WHERE username = 'teste123'
3. Fazer redeploy (push + Coolify)
4. Acessar aplicação
5. Verificar que "teste123" ainda está lá
✅ Sucesso: Usuário não foi perdido
```

**Teste 2: Login atualiza last_login**
```
1. Fazer login com "marco"
2. Executar: SELECT last_login FROM usuarios WHERE username = 'marco'
3. Comparar com horário do login
✅ Sucesso: last_login foi atualizado
```

**Teste 3: Sincronização bidirecional**
```
1. Criar usuário na interface
2. Verificar que aparece em PostgreSQL
3. Modificar usuário no PostgreSQL diretamente (SQL)
4. Reiniciar aplicação
5. Verificar que mudanças foram carregadas
✅ Sucesso: PostgreSQL é fonte de verdade
```

## 🚀 Timeline

| Fase | Atividade | Duração Estimada | Data |
|------|-----------|-----------------|------|
| 1 | Criar postgres_manager.py | 30 min | Hoje |
| 2 | Integrar em app_streamlit.py | 45 min | Hoje |
| 3 | Testes completos | 30 min | Hoje |
| 4 | Deploy e validação | 15 min | Hoje |
| - | **Total** | **~2 horas** | **Hoje** |

## 📝 Notas Importantes

1. **Fonte de Verdade:** PostgreSQL é a fonte de verdade, arquivo é apenas backup
2. **Fallback:** Se PostgreSQL falhar, carrega do arquivo como fallback
3. **Sincronização:** A cada operação de usuário, ambos são atualizados
4. **Auditoria:** Manter log de todas as operações
5. **Recuperação:** Se arquivo corrupto, dados estão salvos no BD

## 🔐 Segurança

- ✅ Senhas hasheadas no PostgreSQL
- ✅ Senhas plaintext mantidas apenas para compatibilidade com streamlit-authenticator
- ✅ Conexão PostgreSQL usa credenciais (melhorar: usar variáveis de ambiente)
- ⏳ TODO: Mover credenciais do BD para variáveis de ambiente

---

**Próximo passo:** Implementar Fase 1 (criar postgres_manager.py)
