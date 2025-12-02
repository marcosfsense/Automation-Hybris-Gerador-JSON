# 📚 Documentação - Índice Completo

**Bem-vindo à documentação do Gerador JSON Hybris!**

Escolha o guia que melhor se adequa ao seu caso:

---

## 🚀 Primeiros Passos

### Para Usuários Novos
1. **[ESTRUTURA_PROJETO.md](ESTRUTURA_PROJETO.md)** - Entenda a organização dos arquivos
2. **[GUIA_USO.md](GUIA_USO.md)** - Como usar a aplicação

### Para Desenvolvedores
1. **[AUTENTICACAO.md](AUTENTICACAO.md)** - Como funciona o sistema de login
2. **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Resolvendo problemas

---

## 📖 Documentação Principal

| Documento | Descrição |
|-----------|-----------|
| **[ESTRUTURA_PROJETO.md](ESTRUTURA_PROJETO.md)** | 📋 Mapa completo do projeto - **COMECE AQUI** |
| **[GUIA_USO.md](GUIA_USO.md)** | 📖 Como usar a aplicação passo-a-passo |
| **[AUTENTICACAO.md](AUTENTICACAO.md)** | 🔐 Sistema de autenticação PostgreSQL + config.yaml |
| **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** | 🆘 Resolução de problemas comuns |

---

## 📚 Documentação de Referência

| Documento | Descrição |
|-----------|-----------|
| **[GUIA_GERENCIAR_USUARIOS.md](GUIA_GERENCIAR_USUARIOS.md)** | 👥 Adicionar/remover/editar usuários |
| **[USUARIOS_E_POSTGRESQL.md](USUARIOS_E_POSTGRESQL.md)** | 🗄️ Estrutura de dados no PostgreSQL |
| **[EXEMPLOS.md](EXEMPLOS.md)** | 📄 Exemplos de JSONs gerados |
| **[CHANGELOG.md](CHANGELOG.md)** | 📅 Histórico de versões e mudanças |

---

## 🔧 Documentação Técnica Avançada

| Documento | Descrição |
|-----------|-----------|
| **[FLUXO_AUTENTICACAO_v4.md](FLUXO_AUTENTICACAO_v4.md)** | 🔐 Fluxo detalhado de autenticação |

---

## 📊 Histórico & Registros

Documentos do processo de desenvolvimento (para referência):

| Documento | Descrição |
|-----------|-----------|
| **[HISTORICO_INVESTIGACAO_DESCOBERTA.md](HISTORICO_INVESTIGACAO_DESCOBERTA.md)** | 📝 Como descobrimos a causa raiz |
| **[HISTORICO_DIAGNOSTICO.md](HISTORICO_DIAGNOSTICO.md)** | 🔍 Análise do diagnóstico completo |
| **[HISTORICO_FIX_ORDEM_FUNCOES.md](HISTORICO_FIX_ORDEM_FUNCOES.md)** | ⚡ Fix crítico da ordem de funções |
| **[HISTORICO_SUCESSO_FINAL.md](HISTORICO_SUCESSO_FINAL.md)** | 🎉 Documentação do sucesso final |
| **[PROXIMAS_ACOES.md](PROXIMAS_ACOES.md)** | 📋 Próximos passos (histórico) |
| **[PROXIMAS_ACOES_DEPLOY.md](PROXIMAS_ACOES_DEPLOY.md)** | 🚀 Instruções de deploy (histórico) |

---

## 🛠️ Ferramentas (Usar via linha de comando)

```bash
# Diagnóstico completo
python tools/diagnostico_completo.py

# Verificar usuários PostgreSQL
python tools/verificar_usuarios_postgres.py

# Testar sincronização
python tools/debug_sync.py

# Migrar usuários para PostgreSQL
python tools/migrate_users_to_postgres.py

# Debug específico
python tools/debug_marcos.py
```

---

## ⚡ Quick Links

- **[Voltar ao README principal](../README.md)** - Documentação da aplicação
- **[Ver Changelog](CHANGELOG.md)** - Histórico de atualizações
- **[Troubleshooting](TROUBLESHOOTING.md)** - Resolver problemas

---

## 🎯 Por Caso de Uso

### "Não consigo fazer login"
→ Veja **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)**

### "Quero adicionar um novo usuário"
→ Veja **[GUIA_GERENCIAR_USUARIOS.md](GUIA_GERENCIAR_USUARIOS.md)**

### "Como o sistema de autenticação funciona?"
→ Veja **[AUTENTICACAO.md](AUTENTICACAO.md)**

### "Onde estão os arquivos do projeto?"
→ Veja **[ESTRUTURA_PROJETO.md](ESTRUTURA_PROJETO.md)**

### "Como usar a aplicação?"
→ Veja **[GUIA_USO.md](GUIA_USO.md)**

---

## 📞 Precisa de Ajuda?

1. **Primeiro**: Leia [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. **Depois**: Rode `python tools/diagnostico_completo.py`
3. **Ainda tem dúvida?**: Consulte [ESTRUTURA_PROJETO.md](ESTRUTURA_PROJETO.md)

---

**Última atualização**: 2025-12-02
**Status**: ✅ Documentação Completa
