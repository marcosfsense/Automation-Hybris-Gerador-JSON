# 👥 Guia Completo - Gerenciar Usuários e Senhas

Você agora pode criar, editar e remover usuários de forma segura e fácil!

---

## 📋 Sumário Rápido

| Tarefa | Comando |
|--------|---------|
| **Adicionar usuário** | `python manage_users.py add <username> <password>` |
| **Alterar senha** | `python manage_users.py change <username> <new_password>` |
| **Remover usuário** | `python manage_users.py remove <username>` |
| **Listar usuários** | `python manage_users.py list` |
| **Reset padrão** | `python manage_users.py reset-all` |

---

## 🚀 Exemplos Práticos

### 1️⃣ Adicionar Novo Usuário

**Comando:**
```bash
python manage_users.py add joao Senha123!Joao
```

**Resultado esperado:**
```
✅ Usuário 'joao' criado com sucesso!
```

**O que foi feito:**
- Usuário `joao` criado
- Senha `Senha123!Joao` armazenada com segurança (hash SHA256)
- Usuário habilitado automaticamente

### 2️⃣ Alterar Senha de um Usuário

**Comando:**
```bash
python manage_users.py change marco SenhaNovaForte123!
```

**Resultado esperado:**
```
✅ Senha do usuário 'marco' alterada com sucesso!
```

**O que foi feito:**
- Senha antiga removida
- Nova senha `SenhaNovaForte123!` armazenada com segurança
- Usuário pode logar com a nova senha imediatamente

### 3️⃣ Remover um Usuário

**Comando:**
```bash
python manage_users.py remove joao
```

**Resultado esperado:**
```
✅ Usuário 'joao' removido com sucesso!
```

**O que foi feito:**
- Usuário `joao` completamente removido
- Já não pode mais logar na aplicação

### 4️⃣ Listar Todos os Usuários

**Comando:**
```bash
python manage_users.py list
```

**Resultado esperado:**
```
============================================================
📋 USUÁRIOS CADASTRADOS
============================================================

👤 marco
   Status: ✅ Ativo
   Criado em: 2024-11-26 10:30:45
   Último acesso: 2024-11-26 11:15:22

👤 joao
   Status: ✅ Ativo
   Criado em: 2024-11-26 10:35:10
   Último acesso: Nunca

============================================================
```

---

## ⚙️ Requisitos de Senha

As senhas devem atender aos seguintes critérios:

✅ **Mínimo de 8 caracteres**
✅ **Pode incluir:** letras, números, símbolos (!@#$%^&*)
✅ **Recomendado:** Misturar maiúsculas e minúsculas

**Exemplos de senhas válidas:**
- `SenhaForte123!Marcos` ✅
- `Projeto2024@Hybris` ✅
- `Marco#Sense123` ✅
- `123456` ❌ (muito curto)

---

## 🔐 Como Funciona a Segurança

### Armazenamento de Senhas

As senhas **NÃO** são armazenadas em texto plano!

```
📁 credentials.json
│
└─ marco:
   └─ password_hash: "sha256:a43f1d0aafd193734f329da5c1f88df67aac503afea0320db3825f2396e3e9a8"
```

### Verificação de Acesso

1. **Usuário digita:** `marco` / `SenhaForte123!Marcos`
2. **App gera hash:** `sha256:a43f1d0aafd193734f329da5c...`
3. **App compara** com hash armazenado
4. **Se forem iguais:** ✅ Acesso concedido
5. **Se forem diferentes:** ❌ Acesso negado

---

## 📁 Onde as Credenciais São Armazenadas

**Arquivo:** `credentials.json` (raiz do projeto)

**Exemplo de conteúdo:**
```json
{
  "users": {
    "marco": {
      "password_hash": "sha256:a43f1d0aafd193734f329da5c1f88df67aac503afea0320db3825f2396e3e9a8",
      "created_at": "2024-11-26 10:30:45",
      "last_login": "2024-11-26 11:15:22",
      "enabled": true
    },
    "joao": {
      "password_hash": "sha256:xyz...",
      "created_at": "2024-11-26 10:35:10",
      "last_login": null,
      "enabled": true
    }
  },
  "version": "1.0"
}
```

⚠️ **IMPORTANTE:** Nunca edite este arquivo manualmente! Use sempre o script `manage_users.py`.

---

## 🐛 Resolução de Problemas

### Problema 1: "Usuário já existe"

**Erro:**
```
❌ Erro: usuário 'marco' já existe
```

**Solução:**
- Use `python manage_users.py change marco <nova_senha>` para alterar a senha
- Ou remova primeiro: `python manage_users.py remove marco`

### Problema 2: "Usuário não encontrado"

**Erro:**
```
❌ Erro: usuário 'xyz' não encontrado
```

**Solução:**
- Verifique o nome do usuário: `python manage_users.py list`
- Certifique-se de que digitou o nome correto (sensível a maiúsculas/minúsculas)

### Problema 3: "Senha muito curta"

**Erro:**
```
❌ Erro: senha deve ter pelo menos 8 caracteres
```

**Solução:**
- Use uma senha com **mínimo 8 caracteres**
- Exemplo: `SenhaForte123!` (14 caracteres)

### Problema 4: Credenciais.json não encontrado

**O que fazer:**
- Não se preocupe! O arquivo é criado automaticamente
- Execute qualquer comando: `python manage_users.py list`
- Arquivo será criado com o usuário padrão `marco`

---

## 💡 Boas Práticas

### ✅ Faça

1. **Altere a senha padrão** assim que tiver acesso
   ```bash
   python manage_users.py change marco SuaSenhaForte123!
   ```

2. **Use senhas fortes** com caracteres variados
   ```bash
   python manage_users.py add maria Projeto@Sense2024
   ```

3. **Revise permissões** periodicamente
   ```bash
   python manage_users.py list
   ```

4. **Remova usuários inativos**
   ```bash
   python manage_users.py remove usuario_antigo
   ```

### ❌ Não Faça

1. ❌ Não use senhas simples (`senha123`, `12345678`)
2. ❌ Não compartilhe senhas por email ou Slack público
3. ❌ Não edite `credentials.json` manualmente
4. ❌ Não commit `credentials.json` com dados reais no GitHub
5. ❌ Não reutilize a mesma senha para múltiplas contas

---

## 📱 Fluxo Completo de Uso

### Cenário: Novo Colaborador Precisa de Acesso

**Passo 1:** Criar usuário
```bash
python manage_users.py add carlos Senha@Carlos2024
```
Resultado: ✅ Usuário 'carlos' criado com sucesso!

**Passo 2:** Informar credenciais ao colaborador (via WhatsApp/Slack privado)
```
Acesso à aplicação Hybris:
URL: https://gerajson.sensebike.com.br
Usuário: carlos
Senha: Senha@Carlos2024
```

**Passo 3:** Colaborador faz login e pode usar a aplicação

**Passo 4:** Se esquecer a senha, você pode resetar
```bash
python manage_users.py change carlos SenhaTemporaria2024!
```

---

## 🔄 Sincronizando com Coolify (Deploy)

### Após fazer mudanças nos usuários:

1. **Fazer commit das mudanças:**
   ```bash
   git add credentials.json
   git commit -m "chore: Adicionar usuario carlos"
   git push origin main
   ```

2. **No Coolify (opcional):**
   - Se tiver auto-deploy ativado, as mudanças são aplicadas automaticamente
   - Se não tiver, faça manualmente:
     - Vá para: Gerador-JSON-Hybris → Deployments
     - Clique em "Redeploy"
     - Aguarde ~1-2 minutos (rápido, sem rebuild do Docker)

3. **Novo usuário pode logar:**
   ```
   Acesse: https://gerajson.sensebike.com.br
   Usuário: carlos
   Senha: SenhaTemporaria2024!
   ```

---

## 📊 Exemplo: Administrando Múltiplos Usuários

### Cenário Completo

**Começar com padrão:**
```bash
python manage_users.py list
# Resultado: Apenas 'marco'
```

**Adicionar 3 novos usuários:**
```bash
python manage_users.py add joao Senha@Joao2024
python manage_users.py add maria Senha@Maria2024
python manage_users.py add carlos Senha@Carlos2024
```

**Verificar todos os usuários:**
```bash
python manage_users.py list
# Resultado: 4 usuários (marco, joao, maria, carlos)
```

**Alterar senha do 'marco' para algo mais seguro:**
```bash
python manage_users.py change marco SenhaNovaForte2024!
```

**Remover usuário inativo:**
```bash
python manage_users.py remove carlos
```

**Estado final:**
```bash
python manage_users.py list
# Resultado: 3 usuários (marco, joao, maria)
```

---

## 🚀 Próximos Passos

1. ✅ Criar seus usuários necessários
2. ✅ Compartilhar credenciais com a equipe (seguramente!)
3. ✅ Fazer commit em `credentials.json` no GitHub
4. ✅ Fazer redeploy no Coolify (se necessário)
5. ✅ Testar login com os novos usuários

---

## 📞 Dúvidas Frequentes

**P: Posso editar credentials.json manualmente?**
R: ❌ Não! O arquivo precisa estar em formato JSON válido. Use sempre o script `manage_users.py`.

**P: E se eu perder a senha do 'marco'?**
R: Você pode resetar para o padrão com `python manage_users.py reset-all`, que volta apenas com o usuário 'marco' e senha 'SenhaForte123!Marcos'.

**P: Os usuários precisam fazer logout da aplicação?**
R: A aplicação usa sessões do Streamlit. Fechar o navegador já faz logout, ou clicar no botão X na URL do navegador.

**P: Quantos usuários posso ter?**
R: Ilimitado! O arquivo JSON pode armazenar quantos usuários forem necessários.

**P: Preciso fazer redeploy depois de alterar usuários?**
R: ✅ Sim! Faça:
```bash
git add credentials.json
git commit -m "chore: Alterar usuarios"
git push origin main
```

---

## ✨ Conclusão

Você agora tem **controle total** sobre quem acessa a aplicação! 🔐

- ✅ Criar novos usuários facilmente
- ✅ Alterar senhas quando necessário
- ✅ Remover acessos de forma segura
- ✅ Listar quem tem acesso

**Próximo comando:**
```bash
python manage_users.py list
```

Veja quem está usando sua aplicação agora! 👥
