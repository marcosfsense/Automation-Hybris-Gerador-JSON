#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerenciar usuários e senhas da aplicação Streamlit
Permite adicionar, editar, remover e listar usuários

Uso:
    python manage_users.py add <username> <password>
    python manage_users.py change <username> <new_password>
    python manage_users.py remove <username>
    python manage_users.py list
    python manage_users.py reset-all
"""

import json
import hashlib
import sys
import io
from pathlib import Path
from datetime import datetime

# Forçar UTF-8 no Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

CREDENTIALS_FILE = Path(__file__).parent / "credentials.json"

def hash_password(password: str) -> str:
    """Gera hash SHA256 da senha"""
    return f"sha256:{hashlib.sha256(password.encode()).hexdigest()}"

def verify_password(password: str, password_hash: str) -> bool:
    """Verifica se a senha corresponde ao hash"""
    return hash_password(password) == password_hash

def load_credentials() -> dict:
    """Carrega arquivo de credenciais"""
    if not CREDENTIALS_FILE.exists():
        return {"users": {}, "version": "1.0"}

    try:
        with open(CREDENTIALS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Erro ao ler credentials.json: {e}")
        sys.exit(1)

def save_credentials(data: dict) -> None:
    """Salva arquivo de credenciais"""
    try:
        with open(CREDENTIALS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ Credenciais salvas com sucesso em {CREDENTIALS_FILE}")
    except Exception as e:
        print(f"❌ Erro ao salvar credentials.json: {e}")
        sys.exit(1)

def add_user(username: str, password: str) -> None:
    """Adiciona novo usuário"""
    if not username or not password:
        print("❌ Erro: usuário e senha são obrigatórios")
        sys.exit(1)

    if len(username) < 3:
        print("❌ Erro: usuário deve ter pelo menos 3 caracteres")
        sys.exit(1)

    if len(password) < 8:
        print("❌ Erro: senha deve ter pelo menos 8 caracteres")
        sys.exit(1)

    data = load_credentials()

    if username in data["users"]:
        print(f"❌ Erro: usuário '{username}' já existe")
        sys.exit(1)

    data["users"][username] = {
        "password_hash": hash_password(password),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "last_login": None,
        "enabled": True
    }

    save_credentials(data)
    print(f"✅ Usuário '{username}' criado com sucesso!")

def change_password(username: str, new_password: str) -> None:
    """Altera senha de um usuário"""
    if not username or not new_password:
        print("❌ Erro: usuário e nova senha são obrigatórios")
        sys.exit(1)

    if len(new_password) < 8:
        print("❌ Erro: senha deve ter pelo menos 8 caracteres")
        sys.exit(1)

    data = load_credentials()

    if username not in data["users"]:
        print(f"❌ Erro: usuário '{username}' não encontrado")
        sys.exit(1)

    data["users"][username]["password_hash"] = hash_password(new_password)
    data["users"][username]["last_modified"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    save_credentials(data)
    print(f"✅ Senha do usuário '{username}' alterada com sucesso!")

def remove_user(username: str) -> None:
    """Remove um usuário"""
    if not username:
        print("❌ Erro: usuário é obrigatório")
        sys.exit(1)

    data = load_credentials()

    if username not in data["users"]:
        print(f"❌ Erro: usuário '{username}' não encontrado")
        sys.exit(1)

    del data["users"][username]
    save_credentials(data)
    print(f"✅ Usuário '{username}' removido com sucesso!")

def list_users() -> None:
    """Lista todos os usuários"""
    data = load_credentials()

    if not data["users"]:
        print("ℹ️  Nenhum usuário cadastrado")
        return

    print("\n" + "="*60)
    print("📋 USUÁRIOS CADASTRADOS")
    print("="*60)

    for username, info in data["users"].items():
        status = "✅ Ativo" if info.get("enabled", True) else "❌ Desativado"
        created = info.get("created_at", "N/A")
        last_login = info.get("last_login", "Nunca")

        print(f"\n👤 {username}")
        print(f"   Status: {status}")
        print(f"   Criado em: {created}")
        print(f"   Último acesso: {last_login}")

    print("\n" + "="*60 + "\n")

def reset_all() -> None:
    """Reseta para configuração padrão (apenas marco)"""
    confirmation = input("\n⚠️  Tem certeza? Isso removerá TODOS os usuários (exceto 'marco')! (s/n): ")

    if confirmation.lower() != 's':
        print("❌ Operação cancelada")
        return

    data = {
        "users": {
            "marco": {
                "password_hash": hash_password("SenhaForte123!Marcos"),
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "last_login": None,
                "enabled": True
            }
        },
        "version": "1.0"
    }

    save_credentials(data)
    print("✅ Credenciais resetadas para configuração padrão!")

def main():
    """Função principal"""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "add":
        if len(sys.argv) < 4:
            print("❌ Erro: use 'python manage_users.py add <username> <password>'")
            sys.exit(1)
        add_user(sys.argv[2], sys.argv[3])

    elif command == "change":
        if len(sys.argv) < 4:
            print("❌ Erro: use 'python manage_users.py change <username> <new_password>'")
            sys.exit(1)
        change_password(sys.argv[2], sys.argv[3])

    elif command == "remove":
        if len(sys.argv) < 3:
            print("❌ Erro: use 'python manage_users.py remove <username>'")
            sys.exit(1)
        remove_user(sys.argv[2])

    elif command == "list":
        list_users()

    elif command == "reset-all":
        reset_all()

    else:
        print(f"❌ Comando desconhecido: {command}")
        print(__doc__)
        sys.exit(1)

if __name__ == "__main__":
    main()
