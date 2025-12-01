# Como Investigar e Resolver o Problema de Autenticação

**Problema Atual**: Apenas "marco" consegue fazer login. Outros usuários recebem "User not authorized".

**Status**: Estamos em loop porque não sabemos ONDE está o problema. Vamos investigar de verdade.

---

## Passo 1: Fazer Deploy da Nova Versão

```bash
# No seu Git local
git push

# No Coolify
# Vá para "Deploy" e redeploy a aplicação
# Isto vai usar o novo código com diagnóstico
```

---

## Passo 2: Rodar o Script de Diagnóstico

Quando a app estiver rodando no Coolify:

```bash
# Acesse o container do Coolify
cd /app && python diagnostico_completo.py
```

Este script vai:

1. **Verificar PostgreSQL**
   - Conectar ao banco
   - Listar usuários salvos
   - Verificar se senhas estão preenchidas

2. **Verificar config.yaml**
   - Procurar o arquivo
   - Verificar estrutura
   - Listar usuários nele

3. **Comparar os dois**
   - Verificar se estão sincronizados
   - Detectar diferenças
   - Comparar senhas

4. **Testar authenticator**
   - Tentar inicializar
   - Reportar erros

---

## Passo 3: Interpretar o Output

O script vai mostrar algo como:

### Cenário A: TUDO OK (esperado)

```
================================================================================
  CAMADA 1: PostgreSQL
================================================================================

[1.1] Tentando conectar ao PostgreSQL...
      Host: u48cw44ccwg4sowco4044goc
      Port: 5432
      User: postgres
      [OK] Conexao bem-sucedida

[1.2] Carregando usuarios do PostgreSQL...
      Total: 4 usuarios
      Usuarios: ['kennedy.oliveira', 'alisson.galvao', 'marcos.fernandes', 'marco']

[1.3] Verificando integridade dos dados...
      [OK] kennedy.oliveira: senha ok, email=kennedy@sensebike.com.br
      [OK] alisson.galvao: senha ok, email=alisson@sensebike.com.br
      [OK] marcos.fernandes: senha ok, email=marcos@sensebike.com.br
      [OK] marco: senha ok, email=marco@sensebike.com.br

================================================================================
  CAMADA 2: config.yaml
================================================================================

[2.1] Procurando config.yaml...
      [OK] Encontrado em: /app/config.yaml

[2.2] Carregando config.yaml...
      [OK] Arquivo carregado

[2.3] Verificando estrutura de credenciais...
      Total: 4 usuarios no config.yaml
      Usuarios: ['kennedy.oliveira', 'alisson.galvao', 'marcos.fernandes', 'marco']

[2.4] Verificando dados de cada usuario...
      [OK] kennedy.oliveira: senha ok, email=kennedy@sensebike.com.br
      [OK] alisson.galvao: senha ok, email=alisson@sensebike.com.br
      [OK] marcos.fernandes: senha ok, email=marcos@sensebike.com.br
      [OK] marco: senha ok, email=marco@sensebike.com.br

================================================================================
  CAMADA 3: Comparação PostgreSQL vs config.yaml
================================================================================

PostgreSQL: ['alisson.galvao', 'kennedy.oliveira', 'marcos.fernandes', 'marco']
config.yaml: ['alisson.galvao', 'kennedy.oliveira', 'marcos.fernandes', 'marco']

[OK] Listas estao sincronizadas!

[3.2] Verificando sincronizacao de senhas...
      [OK] kennedy.oliveira: senha sincronizada
      [OK] alisson.galvao: senha sincronizada
      [OK] marcos.fernandes: senha sincronizada
      [OK] marco: senha sincronizada

================================================================================
  RESUMO E DIAGNOSTICO
================================================================================

Situacao atual:
  - PostgreSQL: 4 usuarios
  - config.yaml: 4 usuarios
  - Sincronizado: SIM

[PROVAVEL] Tudo está configurado corretamente!

Se ainda nao consegue fazer login:
  1. Abra navegador INCOGNITO (ctrl+shift+p no Chrome)
  2. Tente login com cada usuario
  3. Se continuar não funcionando, rode este script novamente
  4. Procure por erros nos logs do Streamlit
```

**O QUE FAZER**: Se isto aparecer, tente fazer login em navegador incógnito. Se continuar não funcionando, há um problema no streamlit-authenticator que precisamos investigar diferente.

---

### Cenário B: config.yaml Vazio

```
[ERRO CRITICO] config.yaml está VAZIO!

Isto significa que a sincronização do PostgreSQL NUNCA FOI EXECUTADA

Proximas acoes:
  1. Verifique os logs do Streamlit para erros de sync
  2. Rode a app novamente
  3. Execute este script novamente para verificar se foi atualizado
```

**O QUE FAZER**:
1. Verifique os logs do Streamlit no Coolify
2. Procure por erros em `[sync_credentials_to_config]`
3. Se houver erro de permissão, corrija
4. Se houver erro de database, verifique PostgreSQL
5. Rode a app novamente e execute o diagnóstico outra vez

---

### Cenário C: PostgreSQL e config.yaml Desincronizados

```
[PROBLEMA] PostgreSQL e config.yaml nao estao sincronizados!

Usuarios no PostgreSQL mas NAO em config.yaml: {'kennedy.oliveira', 'alisson.galvao', 'marcos.fernandes'}

CAUSA: sync_credentials_to_config() nao foi executado ou falhou
```

**O QUE FAZER**:
1. Verifique os logs de `sync_credentials_to_config` no Streamlit
2. Veja se há erros de escrita em config.yaml
3. Verifique permissões do arquivo: `ls -la /app/config.yaml`
4. Se permissão for o problema, corrija com `chmod 644 /app/config.yaml`
5. Rode app novamente

---

## Passo 4: Compartilhar o Output

Quando rodar o script, compartilhe o OUTPUT COMPLETO comigo aqui. Vou analisar e dizer EXATAMENTE qual é o problema e como resolver.

---

## Resumo do Processo

```
┌─ Faz Deploy ─┐
│              │
└──────┬───────┘
       │
       ▼
┌─ Roda diagnostico_completo.py ─┐
│                                  │
└──────┬───────────────────────────┘
       │
       ▼
┌─ Interpreta Output ─┐
│                     │
└──────┬──────────────┘
       │
       ├─ Tudo OK?
       │   └─ Tenta login em navegador incógnito
       │
       ├─ config.yaml vazio?
       │   └─ Procura erro de sync nos logs
       │
       └─ Desincronizado?
           └─ Procura erro de permissão/escrita
```

---

## Perguntas Que Preciso Que Responda

Quando você rodar o script, me responda:

1. **Qual cenário ocorreu?** (A, B ou C)
2. **Se foi A**: Consegue fazer login em navegador incógnito?
3. **Se foi B**: O que os logs do Streamlit mostram?
4. **Se foi C**: Quantos usuários estão desincronizados?

Com essas informações, vou saber EXATAMENTE qual é o problema e vamos resolver definitivamente.

---

## Prazo

Isto deve levar **15-30 minutos** no máximo. Depois teremos a resposta que precisamos.

Roda aí e me traz o output do script.
