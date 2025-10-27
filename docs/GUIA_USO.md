# Gu

ia de Uso - Gerador JSON Hybris

## 🚀 Início Rápido (3 passos)

### 1. Instalar
```bash
pip install -r requirements.txt
```

### 2. Executar
```bash
streamlit run src/app_streamlit.py
```
**Ou no Windows:** Duplo clique em `executar_app.bat`

### 3. Acessar
Abre automaticamente em: **http://localhost:8501**

---

## 📖 Como Usar o Sistema

### PASSO 1: Obter JSON do Cabeçalho no Hybris

No sistema Hybris, copie **TODO o JSON do pedido ATÉ ANTES do campo "transactions"**.

**Importante:** O cabeçalho termina antes de `"transactions"`. Exemplo:

```json
{
  "id" : "c777434f-a679-4298-9803-12d069a4a13d",
  "items" : [ {
    "id" : 1186914740,
    "sku" : "08389316",
    "name" : "Leandro teixeira Filipe",
    "uuid" : "fedcb39b-09d9-4951-9415-8b5a88522662",
    "details" : null,
    "order_id" : 3741538564,
    "quantity" : 1,
    "sku_type" : null,
    "reference" : null,
    "created_at" : "2022-09-09T14:58:12Z",
    "unit_price" : 599000,
    "updated_at" : "2022-09-09T14:58:12Z",
    "description" : null,
    "unit_of_measure" : "EACH"
  } ],
  "price" : 599000,
  "number" : "08389316",
  "status" : "PAID",
  "reference" : "Leandro teixeira Filipe",
  "created_at" : "2022-09-09T14:58:12Z",
  "updated_at" : "2022-09-09T14:58:12Z",
  ← COPIE ATÉ AQUI (antes de "transactions")
}
```

**Não copie:** O campo `"transactions"` será gerado automaticamente pelo sistema.

### PASSO 2: Preencher Formulário Web

1. **Cole o JSON** no campo de texto grande
2. **Selecione o tipo** de transação
3. **Preencha os campos** (aparecem automaticamente)
4. **Clique em "Gerar JSON"**

### PASSO 3: Usar o JSON Gerado

- **Copiar**: Ctrl+A → Ctrl+C no preview
- **Baixar**: Botão "Baixar JSON"
- **Usar**: Cole no Postman e envie para API

---

## 🔧 Campos por Tipo de Transação

**Nota:** Os nomes dos campos seguem exatamente a nomenclatura do JSON (sem tradução).

### PIX
- ✅ **amount** - Valor em Reais
- ✅ **number** - Número da transação/terminal
- ✅ **merchantName** - Nome do estabelecimento (pré-preenchido com "Fake callback Bruno - ")
- ○ **authorization_code** - Código de autorização (opcional)

### DÉBITO
- ✅ **amount** - Valor em Reais
- ✅ **number** - Número da transação/terminal
- ✅ **merchantName** - Nome do estabelecimento (pré-preenchido com "Fake callback Bruno - ")
- ✅ **authorization_code** - Código de autorização
- 🔒 **card.mask** - Fixo: "************XXXX" (não requer preenchimento)
- 🔒 **card.brand** - Fixo: "XXXXXXXX" (não requer preenchimento)

### CRÉDITO
- ✅ **amount** - Valor em Reais
- ✅ **number** - Número da transação/terminal
- ✅ **merchantName** - Nome do estabelecimento (pré-preenchido com "Fake callback Bruno - ")
- ✅ **numberOfQuotas** - Número de parcelas (1-24)
- ✅ **authorization_code** - Código de autorização
- 🔒 **card.mask** - Fixo: "************XXXX" (não requer preenchimento)
- 🔒 **card.brand** - Fixo: "XXXXXXXX" (não requer preenchimento)

### MÚLTIPLAS TRANSAÇÕES

Para cada transação:
1. Escolha o tipo (PIX/DÉBITO/CRÉDITO)
2. Preencha campos específicos (conforme acima)
3. **Importante:** Soma das transações = price do cabeçalho
4. Os campos card.mask e card.brand são fixos para DÉBITO/CRÉDITO

---

## ✅ Validações Automáticas

O sistema valida:
- ✅ JSON do cabeçalho válido
- ✅ Campos obrigatórios preenchidos
- ✅ Soma das transações = valor total
- ✅ Parcelas entre 1-24 (crédito)
- ✅ Valores numéricos

Erros aparecem em vermelho na tela.

---

## 🎯 Exemplo Completo

### 1. JSON do Cabeçalho (do Hybris)
```json
{
  "id": "abc123",
  "items": [{...}],
  "price": 599000,
  "number": "08389316",
  ...
}
```

### 2. Dados do Formulário (Crédito 6x)
- Tipo: CRÉDITO
- Valor: R$ 5990,00
- Number: 11111111
- Estabelecimento: Loja Exemplo
- Parcelas: 6
- Card Mask: ************9012
- Card Brand: MASTERCARD
- Código Auth: XYZ789

### 3. JSON Gerado (copiar e usar)
```json
{
  "id": "abc123",
  "items": [{...}],
  "price": 599000,
  "transactions": [
    {
      "id": "d7v16559h6o6q327nscuawhbr43i9ichng9u2lsx8g",
      "uuid": "d7v16559h6o6q327nscuawhbr43i9ichng9u2lsx8g",
      "amount": 599000,
      "card": {
        "mask": "************9012",
        "brand": "MASTERCARD"
      },
      "payment_fields": {
        "numberOfQuotas": 6,
        ...
      },
      ...
    }
  ]
}
```

---

## 🐛 Problemas Comuns

### "streamlit: command not found"
```bash
pip install --upgrade streamlit
```

### "ModuleNotFoundError: zoneinfo"
**Para Python 3.7-3.8:**
```bash
pip install backports.zoneinfo
```

### Porta 8501 já em uso
```bash
streamlit run src/app_streamlit.py --server.port 8502
```

### Erro ao fazer parse do JSON
- Verifique se colou o JSON completo
- Teste em: https://jsonlint.com/

### "Soma das transações difere"
- Verifique o campo `price` no cabeçalho
- Soma dos `amount` deve ser igual ao `price`

---

## 🌐 Acessar de Outros Computadores

### Descobrir IP do servidor:
```bash
# Windows
ipconfig

# Linux/Mac
ifconfig
```

### Executar com acesso de rede:
```bash
streamlit run src/app_streamlit.py --server.address 0.0.0.0
```

### Acessar de outro PC:
```
http://[IP_DO_SERVIDOR]:8501
```
Exemplo: `http://192.168.1.100:8501`

---

## ⚙️ Configurações Avançadas

### Mudar porta padrão:
```bash
streamlit run src/app_streamlit.py --server.port 8502
```

### Ver logs detalhados:
```bash
streamlit run src/app_streamlit.py --logger.level=debug
```

### Desabilitar modo headless:
```bash
streamlit run src/app_streamlit.py --server.headless false
```

---

## 📊 Recursos da Interface

### Sidebar (Barra Lateral)
- Instruções de uso
- Tipos de transação
- Status do sistema

### Preview do JSON
- Visualização formatada
- Syntax highlighting
- Numeração de linhas

### Métricas
- Número do pedido
- Total de transações
- Valor total (R$)

### Download
- Baixa como arquivo `.json`
- Nome: `hybris_[numero].json`

---

## 🎓 Dicas de Uso

1. **Sempre copie o JSON completo** do Hybris
2. **Verifique os valores** antes de gerar
3. **Use o preview** para conferir antes de copiar
4. **Salve o JSON** para histórico (botão download)
5. **Em MÚLTIPLAS**, confira a soma** dos valores

---

## 🔄 Fluxo Completo

```
Hybris → Copiar JSON
  ↓
Streamlit App → Colar + Preencher
  ↓
Gerar JSON → Preview
  ↓
Copiar ou Baixar
  ↓
Postman → Enviar para API
  ↓
Vinculação Concluída ✅
```

---

## 📞 Suporte

**Problemas técnicos:** Ver seção "Problemas Comuns" acima

**Dúvidas sobre campos:** Consultar [EXEMPLOS.md](EXEMPLOS.md)

**Histórico de mudanças:** Ver [CHANGELOG.md](CHANGELOG.md)

---

**Tempo estimado de uso:** < 1 minuto por JSON
**Dificuldade:** Fácil 🟢
**Requer conhecimento técnico:** Não ❌
