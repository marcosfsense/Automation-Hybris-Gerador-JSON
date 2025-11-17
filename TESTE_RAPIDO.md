# 🧪 GUIA DE TESTE RÁPIDO

Use este guia para testar rapidamente todas as funcionalidades do aplicativo.

---

## 🚀 Iniciando o Aplicativo

```bash
# Windows
executar_app.bat

# Outros SOs
python -m streamlit run src/app_streamlit.py
```

O navegador abrirá em `http://localhost:8501`

---

## 📋 JSON de Teste (Cabeçalho)

Cole este JSON na seção 1️⃣ para todos os testes:

```json
{
  "id": "c777434f-a679-4298-9803-12d069a4a13d",
  "items": [
    {
      "id": 1186914740,
      "sku": "08389316",
      "name": "Produto Teste",
      "uuid": "fedcb39b-09d9-4951-9415-8b5a88522662",
      "details": null,
      "order_id": 3741538564,
      "quantity": 1,
      "created_at": "2025-11-17T10:30:00Z",
      "unit_price": 50000,
      "updated_at": "2025-11-17T10:30:00Z"
    }
  ],
  "price": 50000,
  "number": "00000001",
  "status": "PAID",
  "reference": "Teste Rápido",
  "created_at": "2025-11-17T10:30:00Z",
  "updated_at": "2025-11-17T10:30:00Z",
}
```

---

## ✅ TESTE 1: PIX

### Passos:
1. Cole o JSON do cabeçalho acima
2. Selecione **PIX** no tipo de transação
3. **Verifique**:
   - ❌ Seção 2.1 **NÃO** deve aparecer
   - ✅ Seção 3 deve exibir formulário PIX
4. Preencha:
   - **amount**: 500.00 (será convertido para 50000 centavos)
   - **number**: 11111111
   - **merchantName**: Teste PIX
5. Clique **🚀 Gerar JSON**
6. **Verifique**:
   - ✅ Mensagem de sucesso
   - ✅ JSON com `"transactions"` contendo 1 transação
   - ✅ productCode: 25 (PIX)
   - ✅ Botão de download funciona

### Resultado Esperado:
```json
{
  "transactions": [
    {
      "id": "...",
      "amount": 50000,
      "status": "PAID",
      "payment_fields": {
        "primaryProductCode": 25,
        "merchantName": "Teste PIX",
        ...
      }
    }
  ]
}
```

---

## ✅ TESTE 2: DÉBITO

### Passos:
1. Recarregue ou limpe os campos
2. Cole o JSON do cabeçalho novamente
3. Selecione **DEBITO** no tipo de transação
4. **Verifique**:
   - ❌ Seção 2.1 **NÃO** deve aparecer
   - ✅ Seção 3 deve exibir formulário DÉBITO
5. Preencha:
   - **amount**: 500.00
   - **number**: 22222222
   - **merchantName**: Teste Débito
   - **authorization_code**: AUTH123456 (**obrigatório**)
6. Clique **🚀 Gerar JSON**
7. **Verifique**:
   - ✅ JSON com productCode: 2000 (DÉBITO)
   - ✅ Card.mask: "************XXXX"
   - ✅ authorization_code presente

### Resultado Esperado:
```json
{
  "transactions": [
    {
      "id": "...",
      "amount": 50000,
      "payment_fields": {
        "primaryProductCode": 2000,
        "merchantName": "Teste Débito",
        "authorizationCode": "AUTH123456",
        ...
      },
      "card": {
        "mask": "************XXXX",
        "brand": "XXXXXXXX"
      }
    }
  ]
}
```

---

## ✅ TESTE 3: CRÉDITO

### Passos:
1. Cole o JSON do cabeçalho novamente
2. Selecione **CREDITO**
3. **Verifique**:
   - ❌ Seção 2.1 **NÃO** deve aparecer
   - ✅ Seção 3 deve exibir formulário CRÉDITO
   - ✅ Campo "numberOfQuotas" deve aparecer
4. Preencha:
   - **amount**: 500.00
   - **number**: 33333333
   - **merchantName**: Teste Crédito
   - **numberOfQuotas**: 6 (parcelas)
   - **authorization_code**: AUTH789012 (**obrigatório**)
5. Clique **🚀 Gerar JSON**
6. **Verifique**:
   - ✅ JSON com productCode: 1000 (CRÉDITO)
   - ✅ numberOfQuotas: 6

### Resultado Esperado:
```json
{
  "transactions": [
    {
      "id": "...",
      "amount": 50000,
      "payment_fields": {
        "primaryProductCode": 1000,
        "merchantName": "Teste Crédito",
        "numberOfQuotas": 6,
        "authorizationCode": "AUTH789012",
        ...
      },
      "card": {
        "mask": "************XXXX",
        "brand": "XXXXXXXX"
      }
    }
  ]
}
```

---

## ✅ TESTE 4: MÚLTIPLAS (SEM Pré-preenchimento)

### Passos:
1. Cole o JSON do cabeçalho
2. Selecione **MULTIPLAS**
3. **Verifique**:
   - ✅ Seção 2.1 **DEVE** aparecer
   - ✅ Pergunta: "Já existe o JSON das transações?"
4. **Selecione "Não"** em 2.1
5. **Verifique**:
   - ✅ Seção 3 aparece com "Quantas transações?"
   - ✅ Slider com valor 2
6. Ajuste para **3 transações**
7. **Verifique**:
   - ✅ Aparecem 3 abas: Transação 1, Transação 2, Transação 3
   - ✅ Cada aba tem pergunta: "Já existe a transação?"
8. Em cada aba, preencha manualmente:

   **Aba 1 (PIX)**:
   - Já existe: Não
   - Tipo: PIX
   - amount: 200.00
   - number: 11111111
   - merchantName: Aba 1

   **Aba 2 (DÉBITO)**:
   - Já existe: Não
   - Tipo: DEBITO
   - amount: 200.00
   - number: 22222222
   - merchantName: Aba 2
   - authorization_code: AUTH111

   **Aba 3 (CRÉDITO)**:
   - Já existe: Não
   - Tipo: CREDITO
   - amount: 100.00
   - number: 33333333
   - merchantName: Aba 3
   - numberOfQuotas: 3
   - authorization_code: AUTH222

9. Clique **🚀 Gerar JSON**
10. **Verifique**:
    - ✅ JSON consolidado com 3 transações
    - ✅ Soma: 200 + 200 + 100 = 500.00
    - ✅ Transação 1: productCode 25 (PIX)
    - ✅ Transação 2: productCode 2000 (DÉBITO)
    - ✅ Transação 3: productCode 1000 (CRÉDITO)

### Resultado Esperado:
```json
{
  "price": 50000,
  "transactions": [
    { "amount": 20000, "payment_fields": { "primaryProductCode": 25 } },
    { "amount": 20000, "payment_fields": { "primaryProductCode": 2000 } },
    { "amount": 10000, "payment_fields": { "primaryProductCode": 1000 } }
  ]
}
```

---

## ✅ TESTE 5: MÚLTIPLAS (COM Pré-preenchimento)

### Passos:
1. Cole o JSON do cabeçalho
2. Selecione **MULTIPLAS**
3. Selecione **"Sim"** em "Já existe o JSON das transações?"
4. Cole este JSON no campo:

```json
[
  {
    "amount": 20000,
    "number": "44444444",
    "status": "PAID",
    "payment_fields": {
      "merchantName": "Transação Pré-preenchida 1",
      "primaryProductCode": 25
    }
  },
  {
    "amount": 30000,
    "number": "55555555",
    "status": "PAID",
    "payment_fields": {
      "merchantName": "Transação Pré-preenchida 2",
      "primaryProductCode": 2000,
      "authorizationCode": "PREPRE001"
    },
    "card": {
      "mask": "****1234",
      "brand": "VISA"
    }
  }
]
```

5. **Verifique**:
   - ✅ Mensagem de sucesso: "2 transação(ões) detectada(s)"
   - ✅ Seção 3 aparece com 2 abas (não 2, e sim as detectadas)

6. **Em cada aba, você pode**:
   - Ver os dados pré-preenchidos
   - Editar se necessário
   - Colar JSON específico da transação

7. Clique **🚀 Gerar JSON**
8. **Verifique**:
   - ✅ JSON consolidado com 2 transações
   - ✅ Dados pré-preenchidos mantidos

---

## 🔍 Checklist de Validação Completa

Marque cada item após testar:

### Estrutura da Interface
- [ ] Seção 1️⃣ - Campo de JSON presente
- [ ] Seção 2️⃣ - Selectbox com 5 opções presente
- [ ] Seção 2.1 aparece APENAS para MÚLTIPLAS
- [ ] Seção 3 aparece quando tipo selecionado

### Tipos Individuais
- [ ] PIX - Formulário correto
- [ ] DÉBITO - Formulário correto + authorization_code obrigatório
- [ ] CRÉDITO - Formulário correto + numberOfQuotas

### MÚLTIPLAS
- [ ] Seção 2.1 aparece
- [ ] Pergunta "Já existe o JSON das transações?"
- [ ] Abas criadas dinamicamente
- [ ] Cada aba tem sua pergunta individual
- [ ] Pré-preenchimento funciona
- [ ] Validação de cada aba

### JSON Final
- [ ] Cabeçalho preservado
- [ ] Status = "PAID"
- [ ] Transações no array
- [ ] Soma de valores = price
- [ ] Download funciona
- [ ] Formatação válida (indent=2)

---

## 🐛 Se Algo Não Funcionar

1. **Verifique a sintaxe Python**:
   ```bash
   python -m py_compile src/app_streamlit.py
   ```

2. **Reinicie o Streamlit**:
   - Feche a janela do navegador
   - Pressione `Ctrl+C` no terminal
   - Execute novamente: `python -m streamlit run src/app_streamlit.py`

3. **Limpe o cache do Streamlit**:
   ```bash
   streamlit cache clear
   ```

4. **Verifique os logs**:
   - Procure por erros no terminal
   - Verifique a aba "Console" do navegador (F12)

---

## ✨ Próximos Passos

Após confirmar que todos os testes passam:

1. **Documentar seus casos de uso específicos**
2. **Testar com dados reais do Hybris**
3. **Integrar com n8n** se necessário
4. **Fazer backup do JSON gerado**
5. **Usar no Postman** para enviar à API

---

## 💡 Dicas

- **Sempre cole o JSON completo do cabeçalho** (até antes de "transactions")
- **Para MÚLTIPLAS, a soma deve ser exata** (validação automática)
- **Os IDs são gerados automaticamente** (não precisa se preocupar)
- **Timestamps já são de São Paulo** (ajuste automático de fuso)
- **O JSON é formatado com indent=2** (fácil de ler)

---

**Divirta-se testando! 🎉**
