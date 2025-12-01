"""
Gerenciador PostgreSQL - Sincronização de Usuários
Mantém sincronização automática entre aplicação e banco de dados
"""

import psycopg2
from psycopg2 import sql
from datetime import datetime
import os

class PostgresManager:
    """Gerencia operações com PostgreSQL para usuários"""

    def __init__(self):
        """Inicializa configuração do banco de dados"""
        self.db_config = {
            'host': os.getenv('DB_HOST', 'u48cw44ccwg4sowco4044goc'),
            'port': int(os.getenv('DB_PORT', 5432)),
            'database': os.getenv('DB_NAME', 'postgres'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', 'poMaf572450+@')
        }

    def get_connection(self):
        """Obtém conexão com PostgreSQL"""
        try:
            conn = psycopg2.connect(**self.db_config)
            return conn
        except psycopg2.Error as e:
            print(f"❌ Erro ao conectar ao PostgreSQL: {e}")
            return None

    def ensure_table_exists(self):
        """Cria tabela usuarios se não existir"""
        try:
            conn = self.get_connection()
            if not conn:
                return False

            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS usuarios (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(100) UNIQUE NOT NULL,
                        email VARCHAR(255) NOT NULL,
                        name VARCHAR(255),
                        password_hash VARCHAR(255) NOT NULL,
                        password VARCHAR(255),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_login TIMESTAMP,
                        last_modified TIMESTAMP,
                        enabled BOOLEAN DEFAULT TRUE,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );

                    CREATE INDEX IF NOT EXISTS idx_usuarios_username ON usuarios(username);
                    CREATE INDEX IF NOT EXISTS idx_usuarios_email ON usuarios(email);
                """)
            conn.commit()
            conn.close()
            return True
        except psycopg2.Error as e:
            print(f"❌ Erro ao criar tabela: {e}")
            return False

    def load_all_users(self) -> dict:
        """
        Carrega TODOS os usuários do PostgreSQL
        Retorna dict no formato de credentials.json
        """
        try:
            conn = self.get_connection()
            if not conn:
                return {}

            with conn.cursor() as cur:
                cur.execute("""
                    SELECT username, password_hash, password, email, name,
                           enabled, created_at, last_login, last_modified
                    FROM usuarios
                    ORDER BY created_at
                """)
                users = {}
                for row in cur.fetchall():
                    username, password_hash, password, email, name, enabled, \
                    created_at, last_login, last_modified = row

                    users[username] = {
                        'password_hash': password_hash or '',
                        'password': password or '',
                        'email': email or '',
                        'name': name or username,
                        'enabled': enabled,
                        'created_at': created_at.strftime('%Y-%m-%d %H:%M:%S') if created_at else None,
                        'last_login': last_login.strftime('%Y-%m-%d %H:%M:%S') if last_login else None,
                        'last_modified': last_modified.strftime('%Y-%m-%d %H:%M:%S') if last_modified else None
                    }
            conn.close()
            return users
        except psycopg2.Error as e:
            print(f"❌ Erro ao carregar usuários do PostgreSQL: {e}")
            return {}

    def save_user(self, username: str, email: str, name: str,
                  password_hash: str, password: str, enabled: bool = True) -> bool:
        """
        Salva/atualiza um usuário no PostgreSQL
        """
        try:
            conn = self.get_connection()
            if not conn:
                return False

            with conn.cursor() as cur:
                sql_upsert = """
                INSERT INTO usuarios (username, email, name, password_hash, password, enabled)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (username) DO UPDATE SET
                    email = EXCLUDED.email,
                    name = EXCLUDED.name,
                    password_hash = EXCLUDED.password_hash,
                    password = EXCLUDED.password,
                    enabled = EXCLUDED.enabled,
                    updated_at = CURRENT_TIMESTAMP
                """
                cur.execute(sql_upsert, (username, email, name, password_hash, password, enabled))
            conn.commit()
            conn.close()
            return True
        except psycopg2.Error as e:
            print(f"❌ Erro ao salvar usuário no PostgreSQL: {e}")
            return False

    def delete_user(self, username: str) -> bool:
        """
        Delete usuário do PostgreSQL
        """
        try:
            conn = self.get_connection()
            if not conn:
                return False

            with conn.cursor() as cur:
                cur.execute("DELETE FROM usuarios WHERE username = %s", (username,))
            conn.commit()
            conn.close()
            return True
        except psycopg2.Error as e:
            print(f"❌ Erro ao deletar usuário do PostgreSQL: {e}")
            return False

    def update_last_login(self, username: str) -> bool:
        """
        Atualiza last_login após login bem-sucedido
        """
        try:
            conn = self.get_connection()
            if not conn:
                return False

            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE usuarios
                    SET last_login = CURRENT_TIMESTAMP,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE username = %s
                """, (username,))
            conn.commit()
            conn.close()
            return True
        except psycopg2.Error as e:
            print(f"⚠️ Erro ao atualizar last_login: {e}")
            return False

    def user_exists(self, username: str) -> bool:
        """Verifica se usuário existe no PostgreSQL"""
        try:
            conn = self.get_connection()
            if not conn:
                return False

            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM usuarios WHERE username = %s", (username,))
                result = cur.fetchone()
            conn.close()
            return result[0] > 0 if result else False
        except psycopg2.Error:
            return False

    def get_user_count(self) -> int:
        """Retorna total de usuários no banco"""
        try:
            conn = self.get_connection()
            if not conn:
                return 0

            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM usuarios")
                result = cur.fetchone()
            conn.close()
            return result[0] if result else 0
        except psycopg2.Error:
            return 0
