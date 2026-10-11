from flask import Blueprint, request, jsonify
from app.database import get_db
from app.validators import validate_score_data

# Criamos um Blueprint (módulo de rotas) para organizar o app
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

@api_bp.route('/scores', methods=['POST'])
def submit_score():
    """Recebe a pontuação do jogo e salva no banco de dados."""
    data = request.get_json()
    
    # Valida a entrada
    is_valid, error_message = validate_score_data(data)
    if not is_valid:
        return jsonify({"status": "error", "message": error_message}), 400
        
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO scores (player_name, score) VALUES (?, ?)",
            (data['player_name'], data['score'])
        )
        db.commit()
        return jsonify({"status": "success", "message": "Pontuação registrada!"}), 21
    except Exception:
        return jsonify({"status": "error", "message": "Erro interno ao salvar no banco."}), 500

@api_bp.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    """Busca o Top 10 mundial ordenado por maior pontuação."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT player_name, score FROM scores ORDER BY score DESC, created_at ASC LIMIT 10"
    )
    rows = cursor.fetchall()
    
    # Converte as linhas do banco em uma lista de dicionários JSON
    leaderboard = [{"player_name": row["player_name"], "score": row["score"]} for row in rows]
    return jsonify(leaderboard), 200
