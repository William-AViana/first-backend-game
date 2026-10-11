def validate_score_data(data):
    """Valida manualmente se o JSON enviado pelo jogo é seguro e correto."""
    if not data:
        return False, "O corpo da requisição não pode estar vazio."
    
    player_name = data.get("player_name")
    score = data.get("score")
    
    if not player_name or not isinstance(player_name, str):
        return False, "O campo 'player_name' é obrigatório e deve ser um texto."
        
    if len(player_name) < 2 or len(player_name) > 15:
        return False, "O nome do jogador deve ter entre 2 e 15 caracteres."
        
    if score is None or not isinstance(score, int) or score < 0:
        return False, "O campo 'score' deve ser um número inteiro maior ou igual a zero."
        
    return True, None
