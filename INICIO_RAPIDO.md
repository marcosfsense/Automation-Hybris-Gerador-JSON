# Início Rápido

## 3 Passos para Começar

### 1️⃣ Instalar Dependências

```bash
pip install -r requirements.txt
```

Ou manualmente:
```bash
pip install streamlit>=1.28.0
```

### 2️⃣ Executar Aplicação

**Windows:**
```bash
executar_app.bat
```

**Linux/Mac ou Terminal:**
```bash
streamlit run src/app_streamlit.py
```

### 3️⃣ Usar o Sistema

1. Abra o navegador em `http://localhost:8501`
2. Cole o JSON do cabeçalho obtido no Hybris
3. Selecione o tipo de transação (PIX, DÉBITO, CRÉDITO ou MÚLTIPLAS)
4. Preencha os campos específicos
5. Clique em "Gerar JSON"
6. Copie o resultado e use no Postman/API

---

## Exemplo Rápido - PIX

### Entrada:

**JSON do Cabeçalho (do Hybris) - Copie ATÉ ANTES de "transactions":**
```json
{
  "id": "c777434f-a679-4298-9803-12d069a4a13d",
  "items": [{
    "id": 1186914740,
    "sku": "08389316",
    "name": "Leandro teixeira Filipe",
    "uuid": "fedcb39b-09d9-4951-9415-8b5a88522662",
    "details": null,
    "order_id": 3741538564,
    "quantity": 1,
    "sku_type": null,
    "reference": null,
    "created_at": "2022-09-09T14:58:12Z",
    "unit_price": 599000,
    "updated_at": "2022-09-09T14:58:12Z",
    "description": null,
    "unit_of_measure": "EACH"
  }],
  "price": 599000,
  "number": "08389316",
  "status": "PAID",
  "reference": "Leandro teixeira Filipe",
  "created_at": "2022-09-09T14:58:12Z",
  "updated_at": "2022-09-09T14:58:12Z",
}
```

**⚠️ IMPORTANTE:** NÃO copie o campo `"transactions"` - ele será gerado automaticamente!

**Dados da Transação:**
- Tipo: PIX
- Valor: R$ 5.990,00
- Number: 1111111
- Estabelecimento: Fake callback Bruno

### Saída:

O sistema adiciona o array `transactions` ao JSON do cabeçalho:

```json
{
  "id": "c777434f-a679-4298-9803-12d069a4a13d",
  "items": [...],
  "price": 599000,
  "transactions": [{
    "id": "a0jgooopiimskgfjl94jh2id31q6q60ymfhxruzpfn",
    "uuid": "a0jgooopiimskgfjl94jh2id31q6q60ymfhxruzpfn",
    "amount": 599000,
    "number": "1111111",
    "status": "CONFIRMED",
    "payment_fields": {
      "primaryProductCode": 25,
      "primaryProductName": "PIX",
      "merchantName": "Fake callback Bruno"
    }
  }]
}
```

---

## Tipos de Transação

**Nota:** Nomes dos campos em inglês (nomenclatura do JSON).

| Tipo | Campos Obrigatórios |
|------|---------------------|
| **PIX** | amount, number, merchantName |
| **DÉBITO** | amount, number, merchantName, authorization_code |
| **CRÉDITO** | amount, number, merchantName, numberOfQuotas, authorization_code |
| **MÚLTIPLAS** | 2 a 5 transações (cada uma com seus campos) |

**Campos Automáticos (não requerem preenchimento):**
- card.mask: Sempre "************XXXX"
- card.brand: Sempre "XXXXXXXX"
- merchantName: Pré-preenchido com "Fake callback Bruno - " (personalizável)

---

## Próximos Passos

- **Guia Completo:** [docs/GUIA_USO.md](docs/GUIA_USO.md)
- **Exemplos:** [docs/EXEMPLOS.md](docs/EXEMPLOS.md)
- **Estrutura do Projeto:** [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

---

## Dicas Importantes

### Valores Monetários
- **No cabeçalho:** Centavos (599000 = R$ 5.990,00)
- **No formulário:** Reais (5990.00)
- Sistema converte automaticamente

### IDs Únicos
- Gerados automaticamente
- 42 caracteres alfanuméricos
- Sem traços
- id = uuid (sempre iguais)

### Card Mask
- Formato: `************XXXX`
- 12 asteriscos + 4 últimos dígitos
- Exemplo: `************1234`

### Múltiplas Transações
- Soma dos valores deve ser igual ao `price` do cabeçalho
- Mínimo: 2 transações
- Máximo: 5 transações

---

## Suporte

**Erro ao executar?**
1. Verifique se Python 3.9+ está instalado: `python --version`
2. Verifique se Streamlit está instalado: `streamlit --version`
3. Reinstale dependências: `pip install -r requirements.txt`

**Erro de validação?**
1. Verifique se o JSON do cabeçalho está completo
2. Certifique-se de preencher todos os campos obrigatórios
3. Veja exemplos em [examples/](examples/)

**Outras dúvidas?**
- Consulte [README.md](README.md)
- Veja [docs/GUIA_USO.md](docs/GUIA_USO.md)

---

**Desenvolvido para otimizar o workflow Hybris** 🚀
**Versão:** 2.0 | **Tempo de geração:** < 30 segundos
