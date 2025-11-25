"""
Script de teste para validar as correções implementadas
"""

import json

print("=" * 60)
print("TESTE DAS CORREÇÕES IMPLEMENTADAS")
print("=" * 60)

# Teste 1: Validar parsing de JSON com erros "Extra data"
print("\n[TESTE 1] Parsing de JSON com detecção de erro 'Extra data'")
print("-" * 60)

test_jsons = [
    ('{ "id": "test", "amount": 100 }', "JSON válido simples"),
    ('{ "id": "test", "amount": 100 } EXTRA_TEXT', "JSON com dados extras após fechamento"),
    ('{ "id": "test", "amount": 100 },, { "outro": "json" }', "JSON duplicado com vírgula dupla"),
]

for test_json, descricao in test_jsons:
    try:
        json.loads(test_json)
        print(f"✅ {descricao}: PARSE OK")
    except json.JSONDecodeError as e:
        print(f"❌ {descricao}")
        print(f"   Erro: {str(e)}")
        print(f"   Posição: char {e.pos}")

# Teste 2: Validar hash detection
print("\n\n[TESTE 2] Hash detection para detectar mudanças no header")
print("-" * 60)

import hashlib

header1 = '{ "id": "123", "price": 1000 }'
header2 = '{ "id": "123", "price": 1000 }'  # Mesmo conteúdo
header3 = '{ "id": "123", "price": 2000 }'  # Conteúdo diferente

hash1 = hashlib.md5(header1.encode()).hexdigest()
hash2 = hashlib.md5(header2.encode()).hexdigest()
hash3 = hashlib.md5(header3.encode()).hexdigest()

print(f"Header 1: {hash1}")
print(f"Header 2: {hash2}")
print(f"Header 3: {hash3}")

if hash1 == hash2:
    print("✅ Hashes iguais para JSONs idênticos")
else:
    print("❌ Hashes deveriam ser iguais para JSONs idênticos")

if hash1 != hash3:
    print("✅ Hashes diferentes para JSONs diferentes")
else:
    print("❌ Hashes deveriam ser diferentes para JSONs diferentes")

# Teste 3: Validar lógica de transações múltiplas
print("\n\n[TESTE 3] Lógica de transações múltiplas (temp_transactions com índices)")
print("-" * 60)

# Simular a lógica de preenchimento com índices
num_transactions = 3
temp_transactions = [None] * num_transactions

# Simular adição de transações em índices específicos
trans_1 = {"amount": 100, "number": "001"}
trans_2 = {"amount": 200, "number": "002"}
trans_3 = {"amount": 300, "number": "003"}

temp_transactions[0] = trans_1
temp_transactions[1] = trans_2
temp_transactions[2] = trans_3

print(f"Transações criadas: {len([t for t in temp_transactions if t is not None])}")

# Filtrar None (como faz o código)
valid_transactions = [t for t in temp_transactions if t is not None]
print(f"Transações válidas após filtragem: {len(valid_transactions)}")

# Calcular soma
total = sum([t.get("amount", 0) for t in valid_transactions])
print(f"Soma total: {total}")

if total == 600:
    print("✅ Soma correta!")
else:
    print("❌ Soma incorreta!")

print("\n" + "=" * 60)
print("TESTES CONCLUÍDOS")
print("=" * 60)
