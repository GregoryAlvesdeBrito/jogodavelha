from flask import Blueprint, request, jsonify
from app.ml_model import load_model

api = Blueprint('api', __name__)

# Carregar o modelo treinado
model = load_model()

@api.route('/api/ai-move', methods=['POST'])
def ai_move():
    """
    Rota para IA sugerir a próxima jogada.
    """
    try:
        data = request.get_json()

        # Validação do JSON recebido
        if 'board_state' not in data:
            return jsonify({'error': "O campo 'board_state' é obrigatório."}), 400

        # Extrair o estado do tabuleiro
        board_state = data['board_state']

        # Validar se o tabuleiro tem 9 posições
        if len(board_state) != 9:
            return jsonify({'error': "O estado do tabuleiro deve conter exatamente 9 posições."}), 400

        # Converter o tabuleiro em formato numérico
        def encode_board(board):
            return [0 if cell == '' else (1 if cell == 'player' else 2) for cell in board]

        encoded_board = encode_board(board_state)

        # Usar o modelo para prever a próxima jogada
        next_move = model.predict([encoded_board])[0]

        # Retornar a posição sugerida pela IA
        return jsonify({
            'board_state': board_state,
            'next_move': next_move
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
