# 📝 Guia Completo: Explicação Linha-a-Linha do hybris_json_generator.py

> Documentação detalhada de cada classe, função e método do gerador de JSONs

---

## 📋 Índice Rápido

- [Imports](#imports)
- [Classe HybrisJSONGenerator](#classe-hybrisjsongenerator)
- [Métodos Estáticos](#métodos-estáticos)
- [Validação](#validação)
- [Criação de Transações](#criação-de-transações)
- [Geração do JSON](#geração-do-json)
- [Função n8n](#função-n8n)
- [Exemplos](#exemplos)

---

## IMPORTS

```python
from datetime import datetime          # Para trabalhar com datas e horas
import json                            # Para manipular e serializar JSON
from typing import Dict, List, Optional  # Type hints para melhor documentação
import random                          # Para gerar números aleatórios
import string                          # Para caracteres (a-z, A-Z, 0-9, etc)
from zoneinfo import ZoneInfo         # Timezone (Python 3.9+)
```

### Explicação:

| Módulo | Uso |
|--------|-----|
| **datetime** | Gera timestamps atuais em timezone do Brasil |
| **json** | Converte objetos Python em strings JSON formatadas |
| **typing** | Adiciona type hints para melhor documentação do código |
| **random** | Seleciona caracteres aleatórios para gerar IDs |
| **string** | Contém constantes com caracteres (letras, números) |
| **ZoneInfo** | Gerencia timezones (São Paulo automaticamente ajusta DST) |

---

## Classe HybrisJSONGenerator

```python
class HybrisJSONGenerator:
    """Classe para gerar JSONs de transações para o sistema Hybris"""
```

### Propósito:
Centraliza toda a lógica de geração de JSONs validados para o sistema Hybris.

### Inicialização:

```python
def __init__(self):
    # Usar timezone de São Paulo (Brasil) - considera horário de verão automaticamente
    self.brazil_tz = ZoneInfo("America/Sao_Paulo")
    # Pega a hora atual em São Paulo no formato ISO 8601
    self.current_timestamp = datetime.now(self.brazil_tz).isoformat()
```

**O que faz:**
- Cria um objeto com timezone de São Paulo
- Gera um timestamp atual no formato ISO 8601 (ex: "2024-11-13T15:30:45.123456-03:00")
- Este timestamp é usado como padrão se nenhum outro for fornecido

---

## Métodos Estáticos

### 1. `generate_unique_id()`

```python
@staticmethod
def generate_unique_id() -> str:
    """
    Gera um ID único de 42 caracteres alfanuméricos (sem traços)
    Formato: apenas letras minúsculas e números
    Exemplo: 4216b627fb0841ce8e5eb44eeda9b3b4aa26624a13d
    """
    # Define o conjunto de caracteres permitidos
    chars = string.ascii_lowercase + string.digits
    # a-z = letras minúsculas
    # 0-9 = números (via string.digits)

    # Gera 42 caracteres aleatórios
    # random.choice(chars) seleciona um caractere aleatório
    # Repetido 42 vezes
    unique_id = ''.join(random.choice(chars) for _ in range(42))
    return unique_id
```

**Explicação:**
```
string.ascii_lowercase = "abcdefghijklmnopqrstuvwxyz"
string.digits = "0123456789"
chars = "abcdefghijklmnopqrstuvwxyz0123456789"

Exemplo de output:
"4216b627fb0841ce8e5eb44eeda9b3b4aa26624a13d"
 ├─ Tem 42 caracteres
 ├─ Contém apenas a-z e 0-9
 └─ Cada chamada gera um novo ID único
```

**Uso:**
```python
generator = HybrisJSONGenerator()
id1 = generator.generate_unique_id()  # "abc123def456..."
id2 = generator.generate_unique_id()  # "xyz789uv0123..."
```

---

### 2. `format_money()`

```python
@staticmethod
def format_money(value: float) -> int:
    """Converte valor em reais para centavos (inteiro)"""
    return int(value * 100)
```

**Exemplos:**
```python
format_money(100.50)   # 10050 (centavos)
format_money(5990.00)  # 599000 (centavos)
format_money(1.99)     # 199 (centavos)
```

**Por que?**
O Hybris trabalha com valores em centavos (inteiros) para evitar problemas de precisão com vírgulas flutuantes.

---

### 3. `parse_money()`

```python
@staticmethod
def parse_money(cents: int) -> float:
    """Converte centavos para reais"""
    return cents / 100
```

**Exemplos:**
```python
parse_money(10050)   # 100.50
parse_money(599000)  # 5990.00
parse_money(199)     # 1.99
```

**Inverso de `format_money()`** - reconverte centavos para reais.

---

## Validação

### `validate_header_json()`

```python
def validate_header_json(self, header_json: Dict) -> tuple[bool, List[str]]:
    """
    Valida se o JSON do cabeçalho possui todos os campos obrigatórios

    Returns:
        tuple: (is_valid, list_of_errors)
    """
    errors = []  # Lista para armazenar erros encontrados

    # Lista de campos que DEVEM estar presentes na raiz
    required_fields = [
        "id",           # ID único do pedido
        "items",        # Array com itens do pedido
        "price",        # Valor total em centavos
        "number",       # Número do pedido
        "status",       # Status (deve ser "PAID")
        "reference",    # Referência do pedido
        "created_at",   # Data de criação
        "updated_at"    # Data de atualização
    ]

    # Verificar se cada campo obrigatório existe
    for field in required_fields:
        if field not in header_json:
            # Se não existe, adiciona erro à lista
            errors.append(f"Campo obrigatório ausente no cabeçalho: '{field}'")
```

**Validações de `items`:**

```python
    # Validar que items é um array e não está vazio
    if "items" in header_json:
        # Verifica se é uma lista (array)
        if not isinstance(header_json["items"], list):
            errors.append("Campo 'items' deve ser um array")

        # Verifica se a lista não está vazia
        elif len(header_json["items"]) == 0:
            errors.append("Campo 'items' não pode estar vazio")

        else:
            # Se tudo OK, valida campos do primeiro item
            item_required = [
                "id",          # ID do item
                "sku",         # Código do produto
                "name",        # Nome do item
                "uuid",        # UUID único
                "quantity",    # Quantidade
                "created_at",  # Data criação
                "unit_price",  # Preço unitário
                "updated_at"   # Data atualização
            ]

            # Pega o primeiro item
            item = header_json["items"][0]

            # Verifica cada campo obrigatório
            for field in item_required:
                if field not in item:
                    errors.append(f"Campo obrigatório ausente em items[0]: '{field}'")
```

**Validações de `price`:**

```python
    # Validar que price é numérico e positivo
    if "price" in header_json:
        # Verifica se é número (int ou float)
        if not isinstance(header_json["price"], (int, float)):
            errors.append("Campo 'price' deve ser numérico")

        # Verifica se é maior que zero
        elif header_json["price"] <= 0:
            errors.append("Campo 'price' deve ser maior que zero")
```

**Validações de `status`:**

```python
    # Validar status (deve ser sempre "PAID")
    if "status" in header_json and header_json["status"] != "PAID":
        errors.append("Campo 'status' deve ser 'PAID'")

    # Retorna tupla (boolean, lista_de_erros)
    is_valid = len(errors) == 0
    return is_valid, errors
```

---

## Criação de Transações

### 1. `create_pix_transaction()`

```python
def create_pix_transaction(
    self,
    amount: int,                              # Valor em centavos
    merchant_name: str,                       # Nome do comerciante
    merchant_code: str = "0027822336749400",  # Código do comerciante (padrão)
    terminal_number: str = "11111111",        # Número do terminal (padrão)
    authorization_code: Optional[str] = None,  # Código de autorização (opcional)
    created_at: Optional[str] = None,         # Timestamp customizado (opcional)
    preserve_payment_fields: Optional[Dict] = None  # Preservar campos originais
) -> Dict:
```

**Fluxo:**

```python
    # Gera ID único para a transação
    transaction_id = self.generate_unique_id()  # "abc123def456..."

    # Define timestamp
    timestamp = created_at or self.current_timestamp
    # Se passou timestamp, usa ele
    # Senão, usa timestamp atual

    # Define código de autorização
    auth_code = authorization_code or self.generate_unique_id()
    # Se passou authorization_code, usa ele
    # Senão, gera um novo ID

    # Campos padrão para PIX
    default_payment_fields = {
        "v40Code": 0,                    # Código interno Hybris
        "cityState": "Fake callback",    # Cidade (default)
        "clientName": "Fake callback",   # Nome cliente (default)
        "primaryProductCode": 25,        # Código do PIX = 25
        "primaryProductName": "PIX",     # Nome do produto
        "merchantCode": merchant_code,   # Código comerciante
        "merchantName": merchant_name,   # Nome comerciante
        # ... mais campos padrão ...
    }

    # Se preservar campos originais
    if preserve_payment_fields:
        # Copia os campos originais
        payment_fields = {**preserve_payment_fields}
        # Atualiza merchantName (permite que usuário customize)
        payment_fields["merchantName"] = merchant_name
        payment_fields["merchantCode"] = merchant_code
        # Preserva o paymentTransactionId original
    else:
        # Usa campos padrão
        payment_fields = default_payment_fields

    # Retorna dicionário com a transação completa
    return {
        "id": transaction_id,                # ID único
        "uuid": transaction_id,              # Mesmo que id
        "amount": amount,                    # Valor em centavos
        "number": terminal_number,           # Número terminal
        "status": "CONFIRMED",               # Status sempre confirmado
        "created_at": timestamp,             # Data criação
        "updated_at": timestamp,             # Data atualização
        "payment_fields": payment_fields,    # Campos específicos PIX
        "authorization_code": auth_code      # Código autorização
    }
```

---

### 2. `create_debit_transaction()`

Similar ao PIX, mas com campos específicos para débito:

```python
def create_debit_transaction(
    self,
    amount: int,
    merchant_name: str,
    card_mask: str = "************1234",      # Máscara do cartão
    card_brand: str = "VISA",                 # Bandeira
    # ... outros parâmetros ...
) -> Dict:
```

**Diferenças do PIX:**

```python
    # Código do débito = 2000
    "primaryProductCode": 2000,
    "primaryProductName": "DEBITO",

    # Inclui informações do cartão
    "card": {
        "mask": card_mask,      # "************1234"
        "brand": card_brand     # "VISA", "MASTERCARD", etc
    },

    # Inclui external_id para rastrear
    "external_id": ext_id,

    # Campos específicos de débito
    "terminal_hardware_model": "L3",
    "terminal_hardware_manufacturer": "Quantum",
```

---

### 3. `create_credit_transaction()`

Similar ao débito, mas com suporte a parcelas:

```python
def create_credit_transaction(
    self,
    amount: int,
    merchant_name: str,
    number_of_quotas: int = 1,    # IMPORTANTE: número de parcelas
    card_mask: str = "************1234",
    card_brand: str = "MASTERCARD",
    # ... outros parâmetros ...
) -> Dict:
```

**Lógica de parcelas:**

```python
    # Ajustar descrições baseado no número de parcelas
    if number_of_quotas > 1:
        # Se for parcelado
        description = f"PARCELADO LOJA EM {number_of_quotas:02d} PARCELAS"
        product_name = "CREDITO PARCELADO LOJA"
        secondary_code = 2

    else:
        # Se for à vista
        description = "A VISTA"
        product_name = "CREDITO A VISTA"
        secondary_code = 1

    # Campos específicos de crédito
    "primaryProductCode": 1000,        # Código crédito = 1000
    "numberOfQuotas": number_of_quotas, # Número de parcelas
    "secondaryProductCode": secondary_code,
    "secondaryProductName": secondary_name,
```

---

## Geração do JSON

### `generate_json_with_header()`

```python
def generate_json_with_header(
    self,
    header_json: Dict,                  # JSON do cabeçalho (do Hybris)
    transaction_type: str,              # "PIX", "DEBITO", "CREDITO" ou "MULTIPLAS"
    transactions_data: List[Dict]       # Lista com dados das transações
) -> str:
    """
    Gera o JSON completo baseado no cabeçalho fornecido
    """

    # PASSO 1: Validar cabeçalho
    is_valid, errors = self.validate_header_json(header_json)
    if not is_valid:
        # Retorna erro se cabeçalho inválido
        return {
            "success": False,
            "error": "Cabeçalho JSON inválido",
            "validation_errors": errors
        }

    # PASSO 2: Criar cópia do cabeçalho
    complete_order = header_json.copy()
    # .copy() cria uma cópia superficial (não altera original)

    # PASSO 3: Garantir status = "PAID"
    complete_order["status"] = "PAID"

    # PASSO 4: Inicializar array de transações
    complete_order["transactions"] = []

    # PASSO 5: Processar transações baseado no tipo
    transaction_type = transaction_type.upper()  # Normaliza para maiúsculas

    if transaction_type == "PIX":
        # Para cada transação nos dados fornecidos
        for trans_data in transactions_data:
            # Cria transação PIX
            transaction = self.create_pix_transaction(
                amount=self.format_money(trans_data.get("amount", 0)),
                # trans_data.get("amount", 0) = pega "amount" ou retorna 0 se não existir
                # self.format_money() = converte reais para centavos
                merchant_name=trans_data.get("merchant_name", ""),
                # ... outros parâmetros ...
            )
            # Adiciona à lista de transações
            complete_order["transactions"].append(transaction)

    elif transaction_type == "DEBITO":
        # Similar ao PIX, mas chama create_debit_transaction()
        # ...

    elif transaction_type == "CREDITO":
        # Similar ao PIX, mas chama create_credit_transaction()
        # Também passa number_of_quotas (parcelas)
        # ...

    elif transaction_type == "MULTIPLAS":
        # Processa múltiplas transações
        for trans_data in transactions_data:
            t_type = trans_data.get("type", "").upper()
            # Identifica o tipo de cada transação

            if t_type == "PIX":
                trans = self.create_pix_transaction(...)
            elif t_type == "DEBITO":
                trans = self.create_debit_transaction(...)
            elif t_type == "CREDITO":
                trans = self.create_credit_transaction(...)

            complete_order["transactions"].append(trans)

    # PASSO 6: Validar totais
    self.validate_transaction_totals(complete_order["price"], complete_order["transactions"])
    # Verifica se soma das transações = price do cabeçalho

    # PASSO 7: Converter para JSON string
    return json.dumps(
        complete_order,           # Objeto Python
        indent=2,                 # Indentação de 2 espaços
        ensure_ascii=False        # Permite caracteres especiais (acentos, etc)
    )
```

---

## Função n8n

```python
def n8n_generate_json(input_data: Dict) -> Dict:
    """
    Função compatível com o Code Node do n8n

    Input esperado:
    {
        "header_json": { ... },
        "transaction_type": "PIX",
        "transactions": [...]
    }

    Returns:
        Dict com sucesso/erro e metadados
    """

    try:
        # Criar instância do gerador
        generator = HybrisJSONGenerator()

        # Extrair dados do input
        header_json = input_data.get("header_json", {})
        transaction_type = input_data.get("transaction_type", "")
        transactions_data = input_data.get("transactions", [])

        # Validar que todos os campos foram fornecidos
        if not header_json:
            return {"success": False, "error": "..."}

        if not transaction_type:
            return {"success": False, "error": "..."}

        if not transactions_data or len(transactions_data) == 0:
            return {"success": False, "error": "..."}

        # Gerar JSON
        json_result = generator.generate_json_with_header(...)

        # Se houve erro na validação
        if isinstance(json_result, dict) and not json_result.get("success", True):
            return json_result

        # Parse do JSON gerado
        json_object = json.loads(json_result)

        # Retornar resultado de sucesso
        return {
            "success": True,
            "message": "JSON gerado com sucesso!",
            "order_number": json_object["number"],
            "transaction_count": len(json_object["transactions"]),
            "total_amount": json_object["price"],
            "total_amount_brl": generator.parse_money(json_object["price"]),
            "json_string": json_result,
            "json_object": json_object
        }

    # Se erro ao fazer parse do JSON
    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error": "Erro ao fazer parse do JSON",
            "details": str(e)
        }

    # Qualquer outro erro
    except Exception as e:
        return {
            "success": False,
            "error": "Erro ao gerar JSON",
            "details": str(e),
            "input_received": input_data
        }
```

---

## Exemplos

### `exemplo_pix_com_header()`

```python
def exemplo_pix_com_header():
    """Exemplo: Gerar JSON PIX com cabeçalho do Hybris"""

    # Criar gerador
    generator = HybrisJSONGenerator()

    # Cabeçalho que viria do formulário (copiado do Hybris)
    header = {
        "id": "c777434f-a679-4298-9803-12d069a4a13d",
        "items": [{
            "id": 1186914740,
            "sku": "08389316",
            "name": "Leandro teixeira Filipe",
            "uuid": "fedcb39b09d9495194158b5a88522662",
            # ... mais campos ...
        }],
        "price": 599000,  # em centavos
        "number": "08389316",
        "status": "PAID",
        # ... mais campos ...
    }

    # Dados da transação PIX do formulário
    transactions = [{
        "amount": 5990.00,  # em reais (será convertido para centavos)
        "merchant_name": "Loja Exemplo LTDA"
    }]

    # Gerar JSON
    json_output = generator.generate_json_with_header(
        header_json=header,
        transaction_type="PIX",
        transactions_data=transactions
    )

    print(json_output)
    return json_output
```

---

## Resumo de Conceitos Importantes

### Centavos vs Reais
```
Reais    → Centavos (×100) → JSON
100.50  → 10050           → sent to API

JSON    → Centavos (÷100) → Reais
10050   → 100.50          → display
```

### IDs e UUIDs
```
Gerados com: 42 caracteres alfanuméricos (a-z, 0-9)
Nunca com: hífen (-) ou underscore (_)
Exemplos: 4216b627fb0841ce8e5eb44eeda9b3b4aa26624a13d
          a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1
```

### Campos Obrigatórios por Tipo

**PIX:**
- amount (centavos)
- merchant_name
- number (terminal)
- authorization_code (opcional)

**DÉBITO:**
- amount
- merchant_name
- number
- authorization_code (obrigatório)
- card_mask
- card_brand

**CRÉDITO:**
- amount
- merchant_name
- number
- authorization_code
- card_mask
- card_brand
- number_of_quotas (obrigatório)

**MÚLTIPLAS:**
- Combinação de 2+ dos acima

### Códigos de Produto
```
PIX:    primaryProductCode = 25
DÉBITO: primaryProductCode = 2000
CRÉDITO: primaryProductCode = 1000
```

---

**Desenvolvido para facilitar o entendimento do código do gerador de JSONs** 🚀
