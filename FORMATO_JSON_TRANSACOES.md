# 📋 Formato JSON para Colar Transações Existentes

**Data**: 19 de Novembro de 2025
**Versão**: 2.2
**Status**: Referência Técnica

---

## 🎯 O Que Colar?

Quando você responde **"Sim"** para "Já existe a transação?", você deve colar **o objeto da transação inteira** do Hybris (não o array, apenas UM objeto).

### ❌ INCORRETO (Array ou estrutura errada)
```json
[{
  "id": "...",
  "amount": 40000,
  ...
}]
```

```json
{
  "trasaction": {
    "id": "...",
    "amount": 40000,
    ...
  }
}
```

### ✅ CORRETO (Apenas o objeto da transação)
```json
{
  "id": "...",
  "amount": 40000,
  "number": "...",
  ...
}
```

---

## 📊 Formato por Tipo de Transação

### 1️⃣ PIX (Campos Mínimos)

**Campos Essenciais** (o que é EXIGIDO colar):
```json
{
  "id": "6608fbe6-0ade-4bfd-a0d7-65d4947396c3",
  "amount": 40000,
  "number": "681204",
  "status": "CONFIRMED",
  "payment_fields": {
    "merchantName": "S2BS FLORIANOPOLIS SC",
    "primaryProductCode": 25
  }
}
```

**Campos Opcionais** (recomendado incluir se disponível):
- `created_at`: Timestamp ISO 8601
- `authorization_code`: Código de autorização
- `external_id`: ID externo

**Exemplo Completo PIX**:
```json
{
  "id": "6608fbe6-0ade-4bfd-a0d7-65d4947396c3",
  "amount": 284050,
  "number": "681204",
  "status": "CONFIRMED",
  "created_at": "2025-11-19T17:08:20Z",
  "external_id": "c3166398-8bf2-43e7-ab64-0c49a38e29c2",
  "payment_fields": {
    "merchantName": "S2BS FLORIANOPOLIS SC",
    "primaryProductCode": 25
  }
}
```

---

### 2️⃣ DÉBITO (Campos Mínimos)

**Campos Essenciais** (o que é EXIGIDO colar):
```json
{
  "id": "6608fbe6-0ade-4bfd-a0d7-65d4947396c3",
  "amount": 40000,
  "number": "681204",
  "status": "CONFIRMED",
  "card": {
    "mask": "************5968",
    "brand": "VISA"
  },
  "payment_fields": {
    "merchantName": "S2BS FLORIANOPOLIS SC",
    "primaryProductCode": 2000,
    "authorization_code": "002297"
  }
}
```

**Campos Opcionais** (recomendado incluir):
- `created_at`: Timestamp ISO 8601
- `authorization_code`: Código de autorização (também pode estar em payment_fields)
- `external_id`: ID externo

**Exemplo Completo DÉBITO**:
```json
{
  "id": "6608fbe6-0ade-4bfd-a0d7-65d4947396c3",
  "amount": 100000,
  "number": "681204",
  "status": "CONFIRMED",
  "created_at": "2025-11-19T17:08:20Z",
  "external_id": "c3166398-8bf2-43e7-ab64-0c49a38e29c2",
  "card": {
    "mask": "************5968",
    "brand": "VISA"
  },
  "authorization_code": "002297",
  "payment_fields": {
    "merchantName": "S2BS FLORIANOPOLIS SC",
    "primaryProductCode": 2000
  }
}
```

---

### 3️⃣ CRÉDITO (Campos Mínimos)

**Campos Essenciais** (o que é EXIGIDO colar):
```json
{
  "id": "6608fbe6-0ade-4bfd-a0d7-65d4947396c3",
  "amount": 40000,
  "number": "681204",
  "status": "CONFIRMED",
  "card": {
    "mask": "************5968",
    "brand": "VISA"
  },
  "payment_fields": {
    "merchantName": "S2BS FLORIANOPOLIS SC",
    "primaryProductCode": 1000,
    "numberOfQuotas": 12,
    "authorization_code": "002297"
  }
}
```

**Campos Opcionais** (recomendado incluir):
- `created_at`: Timestamp ISO 8601
- `authorization_code`: Código de autorização
- `external_id`: ID externo

**Exemplo Completo CRÉDITO**:
```json
{
  "id": "6608fbe6-0ade-4bfd-a0d7-65d4947396c3",
  "amount": 240000,
  "number": "681204",
  "status": "CONFIRMED",
  "created_at": "2025-11-19T17:08:20Z",
  "external_id": "c3166398-8bf2-43e7-ab64-0c49a38e29c2",
  "card": {
    "mask": "************5968",
    "brand": "VISA"
  },
  "authorization_code": "002297",
  "payment_fields": {
    "merchantName": "S2BS FLORIANOPOLIS SC",
    "primaryProductCode": 1000,
    "numberOfQuotas": 12
  }
}
```

---

## 🔑 Campos Críticos por Tipo

| Tipo | Campo | Valor | Obrigatório |
|------|-------|-------|-------------|
| **PIX** | `amount` | Centavos (int) | ✅ |
| **PIX** | `number` | String | ✅ |
| **PIX** | `payment_fields.merchantName` | String | ✅ |
| **PIX** | `payment_fields.primaryProductCode` | 25 | ✅ |
| **PIX** | `status` | String (PAID/CONFIRMED) | ✅ |
| | | | |
| **DÉBITO** | `amount` | Centavos (int) | ✅ |
| **DÉBITO** | `number` | String | ✅ |
| **DÉBITO** | `card.mask` | String (****XXXX) | ✅ |
| **DÉBITO** | `card.brand` | String (VISA/MASTERCARD) | ✅ |
| **DÉBITO** | `payment_fields.merchantName` | String | ✅ |
| **DÉBITO** | `payment_fields.primaryProductCode` | 2000 | ✅ |
| **DÉBITO** | `authorization_code` | String | ✅ |
| **DÉBITO** | `status` | String (CONFIRMED) | ✅ |
| | | | |
| **CRÉDITO** | `amount` | Centavos (int) | ✅ |
| **CRÉDITO** | `number` | String | ✅ |
| **CRÉDITO** | `card.mask` | String (****XXXX) | ✅ |
| **CRÉDITO** | `card.brand` | String (VISA/MASTERCARD) | ✅ |
| **CRÉDITO** | `payment_fields.merchantName` | String | ✅ |
| **CRÉDITO** | `payment_fields.primaryProductCode` | 1000 | ✅ |
| **CRÉDITO** | `payment_fields.numberOfQuotas` | 1-24 | ✅ |
| **CRÉDITO** | `authorization_code` | String | ✅ |
| **CRÉDITO** | `status` | String (CONFIRMED) | ✅ |

---

## 📝 Seu Exemplo - Como Usar

O JSON que você forneceu é uma transação **CRÉDITO**. Aqui está como colar:

### Dele (Completo):
```json
{
  "id": "6608fbe6-0ade-4bfd-a0d7-65d4947396c3",
  "card": {
    "mask": "************5968",
    "brand": "VISA"
  },
  "amount": 40000,
  "number": "681204",
  "status": "CONFIRMED",
  "description": "",
  "external_id": "c3166398-8bf2-43e7-ab64-0c49a38e29c2",
  "payment_fields": {
    "pan": "************5968",
    "v40_code": 4,
    "type_name": "VENDA A CREDITO",
    "city_state": "FLORIANOPOLIS SC",
    "client_name": "PAYWAVE/VISA",
    "service_tax": 0,
    "status_code": 1,
    "boarding_tax": 0,
    "has_password": true,
    "has_warranty": false,
    "product_name": "CREDITO A VISTA",
    "request_date": 1763572100000,
    "change_amount": 0,
    "document_type": "J",
    "entrance_mode": "692010107300",
    "has_signature": false,
    "merchant_code": "0027749350969400",
    "merchant_name": "S2BS FLORIANOPOLIS SC",
    "application_id": "cielo.launcher",
    "totalizer_code": 10,
    "interest_amount": 0,
    "up_front_amount": 0,
    "application_name": "cielo.launcher.ORDER",
    "avaiable_balance": 0,
    "credit_admin_tax": 0,
    "final_cryptogram": "5C37C6DF310F12C8",
    "first_quota_date": 0,
    "has_connectivity": true,
    "is_external_call": true,
    "merchant_address": "BENVENUTA",
    "number_of_quotas": 0,
    "card_capture_type": 3,
    "payment_type_code": 1,
    "first_quota_amount": 0,
    "has_sent_reference": false,
    "is_financial_product": true,
    "primary_product_code": 1000,
    "primary_product_name": "CREDITO",
    "card_label_application": "VISA CREDITO",
    "has_sent_merchant_code": false,
    "payment_transaction_id": "c3166398-8bf2-43e7-ab64-0c49a38e29c2",
    "secondary_product_code": 1,
    "secondary_product_name": "A VISTA",
    "original_transaction_id": "0",
    "receipt_print_permission": 1,
    "has_printed_client_receipt": false,
    "is_double_font_print_allowed": true,
    "is_only_integration_cancelable": false
  },
  "terminal_number": "00239561",
  "transaction_date": "2025-11-19T17:08:20Z",
  "transaction_type": "PAYMENT",
  "authorization_code": "002297",
  "terminal_hardware_model": "L3",
  "terminal_hardware_manufacturer": "Quantum"
}
```

✅ **PODE COLAR ASSIM** - O sistema vai:
- Detectar que é CRÉDITO (primaryProductCode = 1000)
- Extrair campos essenciais: amount, number, card, merchantName, numberOfQuotas, authorization_code
- Preservar os dados originais (payment_fields completo, card, external_id)
- Gerar JSON consolidado mantendo a estrutura

### Ou Minimalista (Mais Rápido):
Se você só quer colar o mínimo:
```json
{
  "id": "6608fbe6-0ade-4bfd-a0d7-65d4947396c3",
  "amount": 40000,
  "number": "681204",
  "status": "CONFIRMED",
  "card": {
    "mask": "************5968",
    "brand": "VISA"
  },
  "authorization_code": "002297",
  "payment_fields": {
    "merchantName": "S2BS FLORIANOPOLIS SC",
    "primaryProductCode": 1000,
    "numberOfQuotas": 0
  }
}
```

✅ **TAMBÉM FUNCIONA** - Menos campos, mesma funcionalidade

---

## 🚀 Passo-a-Passo para Colar

### 1. No Hybris, Copie a Transação

No seu sistema Hybris, localize a transação e copie o **objeto completo** (não o array):

```
transaction: { ... } ← Copie ISTO
```

NÃO copie:
```
transactions: [ { ... } ] ← Não isto
"transaction": { "trasaction": { ... } } ← Nem isto
```

### 2. No Aplicativo, Clique no Tipo (PIX/DÉBITO/CRÉDITO)

Selecione o tipo correspondente à transação que você tem

### 3. Responda "Sim" para "Já existe a transação?"

A pergunta aparecerá em Item 3

### 4. Cole o JSON na text_area

Cole o objeto inteiro no campo:
```
Cole aqui o JSON da transação [TIPO]:
[Cole o JSON aqui]
```

### 5. Clique "Gerar JSON"

O sistema vai:
- ✅ Validar o JSON
- ✅ Detectar o tipo automaticamente
- ✅ Extrair campos essenciais
- ✅ Preservar campos originais
- ✅ Gerar JSON consolidado

---

## ⚠️ Erros Comuns

### ❌ Erro 1: Colar o Array Inteiro
```json
[{
  "id": "...",
  "amount": 40000,
  ...
}]
```
**Solução**: Remove os `[` e `]` - Cole apenas `{ ... }`

### ❌ Erro 2: Colar com "transaction" ou "trasaction"
```json
{
  "transaction": {
    "id": "...",
    "amount": 40000,
    ...
  }
}
```
**Solução**: Cole apenas o conteúdo interno `{ "id": ..., "amount": ... }`

### ❌ Erro 3: JSON com Sintaxe Inválida
```json
{
  "amount": 40000,
  "number": "681204"
  // Falta uma vírgula aqui
  "merchant": "..."
}
```
**Solução**: Verifique a sintaxe - use um validador JSON online

### ❌ Erro 4: Campos Renomeados
```json
{
  "valor": 40000,  ← Deveria ser "amount"
  "numero": "681204"  ← Deveria ser "number"
}
```
**Solução**: Use os nomes de campo exatos do Hybris

### ❌ Erro 5: Falta Campo Crítico
```json
{
  "amount": 40000,
  "number": "681204"
  // Falta "payment_fields" com "primaryProductCode"
}
```
**Solução**: Copie o JSON completo do Hybris

---

## ✅ Validação Inteligente

O aplicativo agora faz detecção automática:

```python
# Se colar um JSON com primaryProductCode
if payment_fields.primaryProductCode == 25:
    Tipo detectado: PIX ✅
elif payment_fields.primaryProductCode == 2000:
    Tipo detectado: DÉBITO ✅
elif payment_fields.primaryProductCode == 1000:
    Tipo detectado: CRÉDITO ✅
else:
    Tipo desconhecido ⚠️
```

Então **não precisa se preocupar** em colar no tipo correto - o sistema detecta automaticamente!

---

## 📊 Resumo: O Que Colar

| Tipo | Copie do Hybris | Cole No App | Status |
|------|---|---|---|
| **PIX** | `transaction` (objeto) | `{ id, amount, number, payment_fields }` | ✅ |
| **DÉBITO** | `transaction` (objeto) | `{ id, amount, number, card, payment_fields }` | ✅ |
| **CRÉDITO** | `transaction` (objeto) | `{ id, amount, number, card, payment_fields }` | ✅ |
| **MÚLTIPLAS** | `transaction` (objeto) | 1 JSON por aba | ✅ |

---

## 💡 Pro Tip

Para facilitar, você pode:

1. **Copiar do Hybris** (completo com todos os campos)
2. **Colar direto no App** - O sistema extrai o que precisa
3. **Preserva** todos os campos originais no JSON final

Não precisa remover campos desnecessários - o sistema é inteligente o suficiente para aproveitar o máximo!

---

**Desenvolvido com ❤️ por Claude Code**
