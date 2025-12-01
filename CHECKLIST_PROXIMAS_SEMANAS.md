# 📋 Checklist: Próximas 2 Semanas

## 🎯 Semana 1: Recuperação de Usuários

### Dia 1-2: Recriar Usuários

- [ ] Acessar a aplicação em produção
- [ ] Criar usuário: `kennedy.oliveira`
  - [ ] Username: `kennedy.oliveira`
  - [ ] Email: (use email da empresa ou pessoal)
  - [ ] Senha: (anote em lugar seguro)
  - [ ] Verificar em PostgreSQL:
    ```bash
    python verificar_usuarios_postgres.py
    ```

- [ ] Criar usuário: `alisson.galvao`
  - [ ] Username: `alisson.galvao`
  - [ ] Email: (use email da empresa ou pessoal)
  - [ ] Senha: (anote em lugar seguro)
  - [ ] Verificar em PostgreSQL

- [ ] Criar usuário: `marcos.fernandes`
  - [ ] Username: `marcos.fernandes`
  - [ ] Email: (use email da empresa ou pessoal)
  - [ ] Senha: (anote em lugar seguro)
  - [ ] Verificar em PostgreSQL

- [ ] Fazer backup das senhas
  - [ ] Guardar em arquivo seguro
  - [ ] Compartilhar com o time conforme necessário

### Dia 3: Verificação

- [ ] Executar script de verificação:
  ```bash
  cd /app && python verificar_usuarios_postgres.py
  ```

- [ ] Confirmar que 4 usuários aparecem:
  - [ ] marco
  - [ ] kennedy.oliveira
  - [ ] alisson.galvao
  - [ ] marcos.fernandes

- [ ] Testar login com cada um dos 3 novos usuários

---

## 🔧 Semana 2: Implementação da Sincronização (EU FAÇO)

### Segunda-feira: Preparação

- [ ] Criar arquivo `src/postgres_manager.py`
  - [ ] Classe `PostgresManager`
  - [ ] Função `get_connection()`
  - [ ] Função `load_all_users()`
  - [ ] Função `save_user()`
  - [ ] Função `delete_user()`
  - [ ] Função `update_last_login()`

- [ ] Testes unitários:
  - [ ] Testar conexão
  - [ ] Testar load_all_users()
  - [ ] Testar save_user()

### Terça-feira: Integração

- [ ] Modificar `src/app_streamlit.py`:
  - [ ] Importar `PostgresManager`
  - [ ] Atualizar `load_credentials()` para carregar do PostgreSQL
  - [ ] Atualizar `save_credentials()` para sincronizar com PostgreSQL
  - [ ] Adicionar `update_last_login()` no callback de login

- [ ] Remover código antigo:
  - [ ] Remover sincronização credentials.json ↔ config.yaml (não mais necessária)

### Quarta-feira: Testes

- [ ] **Teste 1: Novo usuário persiste após redeploy**
  1. Criar usuário "teste_sync_001"
  2. Verificar em PostgreSQL
  3. Fazer redeploy (git push)
  4. Verificar que usuário ainda existe
  - [ ] ✅ Passar

- [ ] **Teste 2: Login atualiza last_login**
  1. Fazer login com "marco"
  2. Executar: `SELECT last_login FROM usuarios WHERE username = 'marco'`
  3. Verificar que timestamp foi atualizado
  - [ ] ✅ Passar

- [ ] **Teste 3: Sincronização bidirecional**
  1. Criar usuário via interface
  2. Modificar no PostgreSQL (SQL direto)
  3. Reiniciar aplicação
  4. Verificar mudança foi carregada
  - [ ] ✅ Passar

### Quinta-feira: Deploy

- [ ] Fazer commit:
  ```bash
  git add src/postgres_manager.py src/app_streamlit.py
  git commit -m "feat: Implementar sincronização automática com PostgreSQL"
  ```

- [ ] Fazer push para git

- [ ] Fazer deploy no Coolify (restartar container)

- [ ] Validação pós-deploy:
  - [ ] Acessar aplicação
  - [ ] Fazer login com "marco"
  - [ ] Criar novo usuário de teste
  - [ ] Verificar em PostgreSQL
  - [ ] Fazer novo redeploy
  - [ ] Verificar que usuário de teste persiste

### Sexta-feira: Documentação

- [ ] Atualizar README.md com nova arquitetura
- [ ] Documentar sincronização PostgreSQL
- [ ] Remover documentação antiga sobre arquivo local
- [ ] Criar changelog

---

## 📊 Verificações Periódicas

### Diárias
- [ ] Verificar se aplicação está rodando: `curl http://app-url`
- [ ] Verificar logs de erro

### Semanais
- [ ] Executar verificação de usuários:
  ```bash
  python verificar_usuarios_postgres.py
  ```
- [ ] Verificar que nenhum usuário foi perdido

### Mensais
- [ ] Fazer backup do PostgreSQL
- [ ] Revisar logs de auditoria
- [ ] Atualizar documentação se necessário

---

## 🚀 Após Implementação

### Permanentemente
- ✅ Credenciais no PostgreSQL (fonte de verdade)
- ✅ Arquivo local como backup automático
- ✅ Sincronização bidirecional
- ✅ Auditoria de login (last_login tracking)
- ✅ Nenhum risco de perda de dados em redeploys

### Futuro
- [ ] Implementar 2FA (autenticação de dois fatores)
- [ ] Adicionar recuperação de senha via email
- [ ] Implementar logs detalhados de acesso
- [ ] Dashboard de administração de usuários
- [ ] Integração com LDAP/Active Directory (opcional)

---

## ⚠️ Rollback Plan (Em caso de problema)

Se algo der errado durante a implementação:

1. **Revert para versão anterior:**
   ```bash
   git revert <commit-id>
   git push
   ```

2. **Restaurar do backup:**
   - Arquivo local: `credentials.json` ainda tem todos os dados
   - PostgreSQL: Executar migration script novamente

3. **Contactar:**
   - Se problema persistir, reverter e investigar

---

## ✅ Sucesso Final

Quando tudo estiver pronto:

```
✅ 4 usuários no PostgreSQL
✅ Sincronização automática funcionando
✅ Aplicação rodando sem erros
✅ Usuários persistem após redeploy
✅ Login atualiza last_login
✅ Documentação atualizada
✅ Nenhum risco de perda de dados

PROBLEMA RESOLVIDO PERMANENTEMENTE ✨
```

---

## 📞 Dúvidas / Problemas

Se surgir alguma dúvida durante o processo:

1. Consulte `PLANO_IMPLEMENTACAO_POSTGRESQL_SYNC.md` (código exato)
2. Consulte `SITUACAO_USUARIOS_E_PROXIMOS_PASSOS.md` (contexto)
3. Execute `verificar_usuarios_postgres.py` para ver estado atual
4. Verifique logs da aplicação

**Status Atual:** Aguardando recriar os 3 usuários (Semana 1)

**Próximo Evento:** Implementação de sincronização (Semana 2) - Data TBD
