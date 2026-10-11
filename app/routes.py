from flask import Blueprint, request, jsonify
from app.database import get_db
from app.validators import validate_score_data

# Criamos um Blueprint (módulo de rotas) para organizar o app
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

@api_bp.route('/scores', methods=['POST'])
def submit_score():
    data = request.get_json()
    is_valid, error_message = validate_score_data(data)
    
    if not is_valid:
        return jsonify({"status": "error", "message": error_message}), 400
        
    try:
        db = get_db()
        with db.cursor() as cursor:
            # Placeholder alterado de ? para %s
            cursor.execute(
                "INSERT INTO scores (player_name, score) VALUES (%s, %s)",
                (data['player_name'], data['score'])
            )
        db.commit()
        return jsonify({"status": "success", "message": "Pontuação registrada!"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": "Erro interno ao salvar no banco."}), 500

@api_bp.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    """Busca o Top 10 mundial ordenado por maior pontuação."""
    from psycopg.rows import dict_row # Importação específica da versão 3
    
    db = get_db()
    # Usa o row_factory para garantir que a resposta seja formatada como dicionário JSON
    with db.cursor(row_factory=dict_row) as cursor:
        cursor.execute(
            "SELECT player_name, score FROM scores ORDER BY score DESC, created_at ASC LIMIT 10"
        )
        rows = cursor.fetchall()
        
    return jsonify(rows), 200