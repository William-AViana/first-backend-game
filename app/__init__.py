from flask import Flask
from app.config import Config
from app.database import close_db, init_db
from app.routes import api_bp

def create_app():
    """Fábrica do Aplicativo (Application Factory Pattern)."""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Registra a função para fechar o banco automaticamente ao fim de cada requisição
    app.teardown_appcontext(close_db)
    
    # Registra as rotas da API
    app.register_blueprint(api_bp)
    
    # Inicializa o banco de dados dentro do contexto do app Flask
    with app.app_context():
        init_db()
        
    return app
