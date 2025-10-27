# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**AUTOMAÇÃO HYBRIS - GERADOR DE JSONs** is an automation system that generates JSON files for payment binding in the Hybris e-commerce platform. It eliminates manual JSON creation, reducing processing time from 5-10 minutes to <30 seconds and errors from ~10% to <1%.

**Technology Stack:**
- Python 3.7+ (no external dependencies)
- n8n for deployment and automation
- Postman for API testing
- Standard library only: `datetime`, `json`, `typing`, `uuid`

## Project Structure

```
├── hybris_json_generator.py      # Main generator class with all transaction types
├── test_validator.py              # Automated test suite (6 test scenarios)
├── n8n_workflow_hybris.json       # n8n workflow (importable)
├── Postman_Collection_Hybris.json # API testing collection
├── exemplo_gerado_pix.json        # Sample JSON output
├── Documentation/
│   ├── README.md                  # Complete technical documentation
│   ├── RESUMO_EXECUTIVO.md        # Executive summary
│   ├── GUIA_RAPIDO.md             # 5-minute quick start
│   └── [4 more docs for different audiences]
└── CLAUDE.md                       # This file
```

## Common Commands

```bash
# Generate example JSONs and test locally
python hybris_json_generator.py

# Run comprehensive test suite (6 scenarios, all transaction types)
python test_validator.py

# These output examples and validation results to console
# No build step or external dependencies needed
```

## Architecture Overview

### Core Components

**HybrisJSONGenerator** (hybris_json_generator.py)
- Single-responsibility class handling JSON generation
- Key methods:
  - `create_base_order()` - Builds order structure
  - `create_pix_transaction()` - PIX payment (product code 25)
  - `create_debit_transaction()` - Debit card (product code 2000)
  - `create_credit_transaction()` - Credit card with installments (product code 1000)
  - `create_multiplas_transaction()` - Combines 2+ payment types
  - `validate_transaction_totals()` - Ensures transaction sum equals order total
  - `generate_json()` - Main entry point

**HybrisJSONValidator** (test_validator.py)
- Validates generated JSONs against Hybris requirements
- 7 validation rules: structure, transactions, amounts, dates, product codes, required fields, JSON format
- Used in automated tests

### Key Architectural Patterns

1. **Amount Handling:** All monetary values stored as centavos (integers). Convert Reals to centavos with `× 100` (e.g., R$ 150.50 = 15050)

2. **Timestamp Format:** ISO 8601 UTC (e.g., "2024-10-24T15:30:00Z")

3. **Transaction Types:**
   - **PIX (25):** Instant payment, no card required
   - **DEBITO (2000):** Debit card with brand and authorization
   - **CREDITO (1000):** Credit card with 1-24 installment support
   - **MULTIPLAS:** 2+ payment types combined in single order

4. **JSON Structure:** Root object contains `id`, `items`, `price` (centavos), `number`, `status` ("PAID"), `created_at`, `updated_at`, and `transactions` array

5. **Default Merchant Config:**
   - Merchant Code: "0011112591759400"
   - Terminal Number: "11111111"
   - Application ID: "cielo.launcher"
   - Status: Always "PAID"

### Separation of Concerns

- **Generation Logic:** HybrisJSONGenerator builds JSON structures
- **Validation Logic:** HybrisJSONValidator ensures correctness
- **Testing:** test_validator.py covers all transaction types
- **Deployment:** n8n_workflow_hybris.json ready for production

## Validation Rules

The system enforces 7 validation rules:
1. Transaction sum equals order total
2. UUID format correctness
3. Currency values in centavos (integers)
4. ISO 8601 UTC timestamp format
5. Correct product codes per transaction type
6. All required fields present
7. Valid JSON structure

## n8n Integration

**Webhook Endpoint:** POST `/webhook/hybris-json-generator`

**Form Fields (Streamlit Interface):**
- **amount**: Valor em Reais (convertido para centavos automaticamente)
- **number**: Número da transação/terminal
- **merchantName**: Pré-preenchido com "Fake callback Bruno - " (personalizável pelo usuário)
- **authorization_code**: Código de autorização (opcional para PIX, obrigatório para DÉBITO/CRÉDITO)
- **numberOfQuotas**: Número de parcelas (somente CRÉDITO, entre 1-24)

**Campos Fixos (hardcoded no código):**
- **card.mask**: Sempre "************XXXX" (não aparece no formulário)
- **card.brand**: Sempre "XXXXXXXX" (não aparece no formulário)

**Deployment:** Execute `streamlit run src/app_streamlit.py` or use `executar_app.bat` on Windows

## Testing

The test suite validates all 4 transaction types:

```bash
python test_validator.py
# Runs 6 test scenarios covering:
# - Single transactions (PIX, Debit, Credit at-sight)
# - Credit installments (6x)
# - Multiple payment combinations (2-way and 3-way splits)
# - All validations pass (100% success rate)
```

## Adding New Transaction Types

1. Create `create_[type]_transaction()` method in HybrisJSONGenerator
2. Define product code and payment_fields structure
3. Add case in `generate_json()` method's transaction type switch
4. Add test scenario in test_validator.py
5. Update documentation
6. Run tests to verify

## Key Files to Know

| File | Purpose |
|------|---------|
| hybris_json_generator.py | Main generator - all logic here |
| test_validator.py | Testing & validation rules |
| README.md | Complete technical reference |
| analise_jsons.md | Deep dive into JSON structure |
| guia_implementacao_n8n.md | Step-by-step n8n setup |
| n8n_workflow_hybris.json | Ready-to-import workflow |

## Important Notes

- **No external dependencies:** Uses only Python standard library for maximum portability
- **Python 3.7+:** Compatible with all modern Python versions
- **Type hints:** Already used throughout for code clarity
- **Hardcoded defaults:** Merchant codes and terminal numbers are hardcoded but can be overridden via parameters
- **Order number generation:** Based on timestamp (last 8 digits)
- **UTC timestamps:** All dates in UTC with 'Z' suffix (ISO 8601)

## Common Development Tasks

**Running generator locally:**
```bash
python hybris_json_generator.py
# Outputs 4 formatted JSON examples to console
```

**Testing before deployment:**
```bash
python test_validator.py
# Validates all 6 scenarios, shows pass/fail for each
```

**Deploying to n8n:**
1. Create or edit Code Node in n8n workflow
2. Copy-paste entire HybrisJSONGenerator class
3. Map webhook inputs to function parameters
4. Test with Postman collection (included)
5. Activate workflow

**Modifying defaults:**
- Edit constants in HybrisJSONGenerator methods
- Update corresponding test cases
- Run tests to verify changes
- Update documentation

## Documentation Map

- **README.md** - Complete API reference and examples (start here for details)
- **RESUMO_EXECUTIVO.md** - Executive summary with metrics and benefits
- **GUIA_RAPIDO.md** - 5-minute quick start guide
- **analise_jsons.md** - Detailed JSON structure analysis
- **guia_implementacao_n8n.md** - Full n8n integration guide
- **CHECKLIST_IMPLEMENTACAO.md** - Implementation phases and tasks
- **LEIA_PRIMEIRO.txt** - Entry point for first-time users
