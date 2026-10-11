import psycopg
from flask import g, current_app

def init_db():
    """Cria a tabela no PostgreSQL se não existir."""
    db_url = current_app.config['DATABASE']
    with psycopg.connect(db_url) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS scores (
                    id SERIAL PRIMARY KEY,
                    player_name VARCHAR(15) NOT NULL,
                    score INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        conn.commit()

def get_db():
    """Abre uma conexão com o PostgreSQL e armazena no contexto 'g'."""
    if 'db' not in g:
        g.db = psycopg.connect(current_app.config['DATABASE'])
    return g.db

def close_db(e=None):
    """Fecha a conexão do banco."""
    db = g.pop('db', None)
    if db is not None:
        db.close()