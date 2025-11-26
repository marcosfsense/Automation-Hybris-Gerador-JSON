#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar arquivo .htpasswd para autenticação Nginx
Uso: python gerar_htpasswd.py
"""

import hashlib
import base64
import os
import sys
from pathlib import Path

# Forçar UTF-8 no Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def gerar_hash_apr1(senha):
    """
    Gera hash APR1 (Apache) para a senha
    Compatível com .htpasswd
    """
    import crypt
    return crypt.crypt(senha, crypt.METHOD_SHA512)

def gerar_hash_bcrypt(senha):
    """
    Gera hash bcrypt para a senha (mais seguro)
    """
    try:
        import bcrypt
        salt = bcrypt.gensalt(rounds=12)
        hash_bytes = bcrypt.hashpw(senha.encode('utf-8'), salt)
        return hash_bytes.decode('utf-8')
    except ImportError:
        print("⚠️  bcrypt não disponível, usando SHA512")
        return gerar_hash_apr1(senha)

def gerar_hash_md5(senha):
    """
    Gera hash MD5 Apache para a senha
    Formato: $apr1$salt$hash
    """
    import crypt
    salt = os.urandom(8)
    return crypt.crypt(senha, '$apr1$' + base64.b64encode(salt).decode()[:8])

def gerar_htpasswd():
    """
    Função principal para gerar .htpasswd
    """
    print("=" * 60)
    print("🔐 GERADOR DE ARQUIVO .htpasswd")
    print("=" * 60)
    print()
    print("Este script gera senhas criptografadas para Nginx Auth")
    print()

    usuarios = []

    while True:
        print("\n" + "=" * 60)
        usuario = input("Nome do usuário (ou 'sair' para terminar): ").strip()

        if usuario.lower() == 'sair':
            break

        if not usuario:
            print("❌ Nome do usuário não pode estar vazio!")
            continue

        # Verificar se usuário já existe
        if any(u[0] == usuario for u in usuarios):
            print(f"❌ Usuário '{usuario}' já foi adicionado!")
            continue

        # Pedir senha
        while True:
            senha = input(f"Senha para '{usuario}': ").strip()

            if not senha:
                print("❌ Senha não pode estar vazia!")
                continue

            if len(senha) < 6:
                print("⚠️  Aviso: Senha muito curta (mínimo 6 caracteres)")
                confirma = input("Continuar mesmo assim? (s/n): ").lower()
                if confirma != 's':
                    continue

            # Confirmar senha
            confirmacao = input("Confirme a senha: ").strip()
            if senha != confirmacao:
                print("❌ Senhas não conferem!")
                continue

            break

        # Gerar hash
        try:
            # Tentar usar bcrypt (mais seguro)
            import bcrypt
            salt = bcrypt.gensalt(rounds=12)
            hash_bcrypt = bcrypt.hashpw(senha.encode('utf-8'), salt).decode('utf-8')
            linha = f"{usuario}:{hash_bcrypt}"
            print(f"✅ Usuário '{usuario}' adicionado (hash bcrypt)")
        except ImportError:
            # Fallback para crypt (padrão do sistema)
            try:
                import crypt
                hash_crypt = crypt.crypt(senha, crypt.METHOD_SHA512)
                linha = f"{usuario}:{hash_crypt}"
                print(f"✅ Usuário '{usuario}' adicionado (hash SHA512)")
            except:
                # Fallback para MD5 simples
                import hashlib
                hash_md5 = hashlib.md5(senha.encode()).hexdigest()
                linha = f"{usuario}:$apr1${hash_md5}"
                print(f"✅ Usuário '{usuario}' adicionado (hash MD5)")

        usuarios.append((usuario, linha))

    if not usuarios:
        print("\n❌ Nenhum usuário foi adicionado!")
        return

    # Exibir resultado
    print("\n" + "=" * 60)
    print("📄 ARQUIVO .htpasswd GERADO:")
    print("=" * 60)
    print()

    conteudo_arquivo = "\n".join(linha for _, linha in usuarios)
    print(conteudo_arquivo)

    print()
    print("=" * 60)

    # Perguntar se quer salvar
    salvar = input("\nSalvar em arquivo .htpasswd? (s/n): ").lower()

    if salvar == 's':
        # Salvar arquivo
        try:
            caminho = Path(".htpasswd")
            caminho.write_text(conteudo_arquivo + "\n")
            print(f"\n✅ Arquivo salvo em: {caminho.absolute()}")
            print("\n📋 Próximas ações:")
            print("1. Commitar para GitHub: git add .htpasswd && git commit -m 'chore: Adicionar autenticação'")
            print("2. Push: git push origin main")
            print("3. Configurar no Coolify em Configuration → Nginx")
            print("4. Fazer redeploy")
            print("5. Testar acesso com https://gerajson.sensebike.com.br")
        except Exception as e:
            print(f"\n❌ Erro ao salvar arquivo: {e}")
            print("\n📋 Copie manualmente o conteúdo acima e salve em .htpasswd")
    else:
        print("\n📋 Copie o conteúdo acima manualmente para um arquivo .htpasswd")

    print()

if __name__ == "__main__":
    try:
        gerar_htpasswd()
    except KeyboardInterrupt:
        print("\n\n❌ Operação cancelada pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
