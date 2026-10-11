
import os

class Config:
    """Configurações base lidas de variáveis de ambiente."""
    SECRET_KEY = os.getenv("SECRET_KEY", "uma-chave-muito-segura-aqui")
    DATABASE = os.getenv("DATABASE_URL", "leaderboard.db")
