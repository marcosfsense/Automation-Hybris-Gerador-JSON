# Fluxo Completo de Autenticação - v4.0

**Data**: 2025-12-01
**Versão**: 4.0
**Status**: ✅ Com logs detalhados implementados

---

## O Problema que Estava Acontecendo

Usuários existiam no PostgreSQL mas não conseguiam fazer login:

```
Kennedy Oliveira no PostgreSQL: ✅
Kennedy Oliveira no config.yaml: ❌
Tentativa de login: "User not authorized" ❌
```

**Causa Raiz**: A sincronização entre PostgreSQL → config.yaml falhava silenciosamente.

---

## Novo Fluxo de Autenticação (v4.0)

### Passo 1: Inicialização da Aplicação

Quando a app inicia (ao fazer deploy no Coolify), acontece:

```
┌─ APP INICIA ─────────────────────────────────────┐
│                                                   │
│ 1. Import de bibliotecas                         │
│    - streamlit, yaml, psycopg2, etc              │
│                                                   │
│ 2. Definição de funções                          │
│    - load_authenticator()                        │
│    - load_credentials()                          │
│    - sync_credentials_to_config()                │
│                                                   │
│ 3. EXECUÇÃO COMEÇA AQUI ↓↓↓                      │
└───────────────────────────────────────────────────┘
```

### Passo 2: Carregar Credenciais do PostgreSQL

**Função**: `load_credentials()`
**Arquivo**: `src/app_streamlit.py` linhas 89-152

```
[load_credentials] Iniciando carregamento...
[load_credentials] Conectando a PostgreSQL...

TRY:
  Conectar a PostgreSQL (host: u48cw44ccwg4sowco4044goc, port: 5432)
  Garantir que tabela "usuarios" existe

  SELECT * FROM usuarios

  ✅ Se sucesso:
     [load_credentials] OK: Carregados 4 usuarios do PostgreSQL:
     - kennedy.oliveira: senha=[preenchida], email=kennedy@sensebike.com.br
     - alisson.galvao: senha=[preenchida], email=alisson@sensebike.com.br
     - marcos.fernandes: senha=[preenchida], email=marcos@sensebike.com.br
     - marco: senha=[preenchida], email=marco@sensebike.com.br

     RETURN: {
       "users": {
         "kennedy.oliveira": {"password": "senha123", "email": "...", ...},
         "alisson.galvao": {...},
         ...
       },
       "version": "1.0"
     }

EXCEPT: PostgreSQL indisponível ou erro
  [load_credentials] AVISO: PostgreSQL indisponivel
  → Tenta fallback com credentials.json
  → Se vazio, usa credencial padrão (marco)
```

**⚠️ IMPORTANTE**: PostgreSQL é a ÚNICA fonte de verdade. Se estiver indisponível:
1. Tenta credentials.json
2. Se vazio, usa apenas "marco"

---

### Passo 3: Sincronizar para config.yaml

**Função**: `sync_credentials_to_config(credentials_data)`
**Arquivo**: `src/app_streamlit.py` linhas 327-407

Este é o passo crítico que estava falhando silenciosamente!

```
📊 INICIANDO SINCRONIZAÇÃO DE CREDENCIAIS
Credenciais carregadas: ['kennedy.oliveira', 'alisson.galvao', 'marcos.fernandes', 'marco']

  [sync] Encontrado config.yaml em: /app/config.yaml
  [sync] Sincronizando 4 usuarios...

  Para CADA usuário:
    [sync] OK: kennedy.oliveira
    [sync] OK: alisson.galvao
    [sync] OK: marcos.fernandes
    [sync] OK: marco

  [sync] SUCESSO: config.yaml salvo em /app/config.yaml

  VERIFICACAO:
  [sync] VERIFICACAO: 4 usuarios confirmados no arquivo:
         ['kennedy.oliveira', 'alisson.galvao', 'marcos.fernandes', 'marco']
```

**O que acontece internamente**:

```python
config['credentials']['usernames'] = {
    'kennedy.oliveira': {
        'email': 'kennedy@sensebike.com.br',
        'name': 'Kennedy Oliveira',
        'password': 'senha123'  # ← Texto plano do PostgreSQL
    },
    'alisson.galvao': {
        'email': 'alisson@sensebike.com.br',
        'name': 'Alisson Galvao',
        'password': 'senha456'
    },
    # ... mais usuários
}
```

Salva em: `config.yaml`

**⚠️ MUDANÇA CRÍTICA da v3.0**: Agora com verificação de salvamento!
Se salvamento falhar, a função **não falha silenciosamente** - ela faz `raise` da exceção.

---

### Passo 4: Inicializar o Authenticator

**Função**: `load_authenticator()`
**Arquivo**: `src/app_streamlit.py` linhas 27-87

```
[load_authenticator] Iniciando...
[load_authenticator] Encontrado config.yaml em: /app/config.yaml

[load_authenticator] Config carregado:
  - Path: /app/config.yaml
  - Usuarios: ['kennedy.oliveira', 'alisson.galvao', 'marcos.fernandes', 'marco']
    - kennedy.oliveira: email=kennedy@sensebike.com.br, senha=[preenchida]
    - alisson.galvao: email=alisson@sensebike.com.br, senha=[preenchida]
    - marcos.fernandes: email=marcos@sensebike.com.br, senha=[preenchida]
    - marco: email=marco@sensebike.com.br, senha=[preenchida]

[load_authenticator] OK: Authenticator inicializado com 4 usuarios
```

O authenticator agora conhece todos os 4 usuários e está pronto para receber logins.

---

## Fluxo de Login do Usuário

Uma vez que a app iniciou com sucesso:

### Cenário A: Login Bem-Sucedido

```
Usuário digita: kennedy.oliveira / senha123
Clica "Entrar"
    ↓
authenticator.login() é chamado
    ↓
streamlit-authenticator procura "kennedy.oliveira" em config['credentials']['usernames']
    ↓
Encontra ✅
    ↓
Compara senha: "senha123" vs "senha123" (salva)
    ↓
Match ✅
    ↓
st.session_state.authentication_status = True
st.session_state.username = "kennedy.oliveira"
    ↓
db.update_last_login("kennedy.oliveira")  # Registra no PostgreSQL
    ↓
Aplicação libera acesso ✅
```

### Cenário B: Login Falha (Problema Anterior)

```
Usuário digita: kennedy.oliveira / senha123
Clica "Entrar"
    ↓
authenticator.login() é chamado
    ↓
streamlit-authenticator procura "kennedy.oliveira" em config['credentials']['usernames']
    ↓
Não encontra ❌
    ↓
st.session_state.authentication_status = False
    ↓
Exibe: "User not authorized"
    ↓
Usuário frustrado ❌

CAUSA: config.yaml ainda tinha apenas "marco"
PORQUE: sync_credentials_to_config() falhou silenciosamente
```

---

## Logs de Debug para Diagnosticar Problemas

Se algo der errado, o Coolify mostrará logs como:

### ✅ Caso 1: Tudo OK

```
[load_credentials] Iniciando carregamento...
[load_credentials] Conectando a PostgreSQL...
[load_credentials] OK: Carregados 4 usuarios do PostgreSQL:
  - kennedy.oliveira: senha=[preenchida], email=...
  - alisson.galvao: senha=[preenchida], email=...
  - marcos.fernandes: senha=[preenchida], email=...
  - marco: senha=[preenchida], email=...

[sync] Encontrado config.yaml em: /app/config.yaml
[sync] Sincronizando 4 usuarios...
[sync] OK: kennedy.oliveira
[sync] OK: alisson.galvao
[sync] OK: marcos.fernandes
[sync] OK: marco
[sync] SUCESSO: config.yaml salvo em /app/config.yaml
[sync] VERIFICACAO: 4 usuarios confirmados no arquivo: [...]

[load_authenticator] Iniciando...
[load_authenticator] Encontrado config.yaml em: /app/config.yaml
[load_authenticator] Config carregado:
  - Usuarios: ['kennedy.oliveira', 'alisson.galvao', 'marcos.fernandes', 'marco']
[load_authenticator] OK: Authenticator inicializado com 4 usuarios

📊 INICIALIZANDO AUTHENTICATOR (sync_status=True)
```

### ❌ Caso 2: PostgreSQL Indisponível

```
[load_credentials] Iniciando carregamento...
[load_credentials] Conectando a PostgreSQL...
[load_credentials] AVISO: PostgreSQL indisponivel: could not translate host name...
[load_credentials] Tentando fallback com credentials.json...
[load_credentials] Encontrado credentials.json em: /app/credentials.json
[load_credentials] OK: Carregados 3 usuarios do arquivo
  - kennedy.oliveira: senha=[preenchida], email=...
  - alisson.galvao: senha=[preenchida], email=...
  - marco: senha=[preenchida], email=...

[sync] Encontrado config.yaml em: /app/config.yaml
[sync] Sincronizando 3 usuarios...
[sync] OK: kennedy.oliveira
[sync] OK: alisson.galvao
[sync] OK: marco
[sync] SUCESSO: config.yaml salvo em /app/config.yaml

[load_authenticator] OK: Authenticator inicializado com 3 usuarios
```

### ❌ Caso 3: Erro de Sincronização

```
[load_credentials] OK: Carregados 4 usuarios do PostgreSQL...

[sync] Encontrado config.yaml em: /app/config.yaml
[sync] Sincronizando 4 usuarios...
[sync] ERRO ao salvar config.yaml: Permission denied
Traceback:
  File "app_streamlit.py", line 388, in sync_credentials_to_config
    with open(config_path, 'w', encoding='utf-8') as f:
OSError: [Errno 13] Permission denied: '/app/config.yaml'

❌ Erro crítico ao sincronizar credentials para config.yaml
```

Neste caso, você saberia que:
- PostgreSQL tem os dados ✅
- Problema é escrever em config.yaml ❌ (permissões?)

---

## Checklist para Resolver Problemas

Quando um usuário não conseguir fazer login:

1. **Verifique os logs do Coolify**
   - Procure por `[load_credentials]`
   - Procure por `[sync]`
   - Procure por erros no PostgreSQL

2. **Se PostgreSQL está indisponível**
   - Verifique credenciais do Coolify (variáveis de ambiente)
   - Verifique se PostgreSQL está rodando
   - Verifique se credentials.json existe como fallback

3. **Se config.yaml não foi atualizado**
   - Verifique permissões do arquivo
   - Verifique se disco tem espaço
   - Procure por erros de escrita nos logs

4. **Se authenticator não reconhece usuários**
   - Verifique se config.yaml tem os usuários (comando: `cat config.yaml`)
   - Verifique se senhas estão preenchidas (não vazias)
   - Verifique se formato YAML está correto

---

## Próximos Passos para Você

1. **Deploy a nova versão no Coolify**
   ```bash
   # Fazer push
   git push
   # Redeploy no Coolify (vai usar novo código)
   ```

2. **Monitorar os logs**
   ```bash
   # No Coolify, veja "Logs" da aplicação
   # Procure pelos logs [load_credentials], [sync], [load_authenticator]
   ```

3. **Testar login com cada usuário**
   - Abra navegador incógnito
   - Tente: kennedy.oliveira / [sua_senha]
   - Tente: alisson.galvao / [sua_senha]
   - Tente: marcos.fernandes / [sua_senha]

4. **Se ainda não funcionar**
   - Compartilhe os logs do Coolify
   - Vamos diagnosticar exatamente onde está o problema

---

## Diagrama Completo do Fluxo

```
┌─────────────────────────────────────────────────────┐
│         APLICAÇÃO INICIA (Coolify)                  │
└────────────────────┬────────────────────────────────┘
                     │
        ┌────────────▼──────────────┐
        │ load_credentials()        │
        │ (linha 89)                │
        │                           │
        │ PostgreSQL → Usuários ✅  │
        │ ou Arquivo (fallback)     │
        └────────────┬──────────────┘
                     │
                     ↓
        ┌─────────────────────────────────┐
        │ sync_credentials_to_config()    │
        │ (linha 327)                     │
        │                                 │
        │ Usuarios → config.yaml ✅       │
        │ + Verificacao de salvamento     │
        └────────────┬────────────────────┘
                     │
                     ↓
        ┌─────────────────────────────────┐
        │ load_authenticator()            │
        │ (linha 27)                      │
        │                                 │
        │ Lê config.yaml                  │
        │ Cria Authenticate() ✅          │
        └────────────┬────────────────────┘
                     │
        ┌────────────▼───────────────────┐
        │  APLICAÇÃO PRONTA PARA LOGIN   │
        │                                │
        │ Usuário pode fazer login ✅    │
        └────────────────────────────────┘
```

---

## Resumo das Mudanças v4.0

| Aspecto | v3.0 | v4.0 |
|---------|------|------|
| **sync_credentials_to_config()** | Falha silenciosa | Falha com exceção ✅ |
| **Verificação de salvamento** | Não | Sim ✅ |
| **Logs de debug** | Mínimos | Detalhados ✅ |
| **load_credentials logs** | Básicos | Rastreamento total ✅ |
| **load_authenticator logs** | Básicos | Rastreamento total ✅ |
| **Visibilidade** | Opaca | Transparente ✅ |

**Resultado**: Quando algo dá errado, você sabe EXATAMENTE o quê e onde.
