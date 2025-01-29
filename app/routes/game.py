from flask import Blueprint, request, jsonify
from app.ml_model import load_model
from app.models import HistoricoJogos , Player
from app import db

game = Blueprint('game', __name__) # Modelo BluePrint
model = load_model() # Modelo Treinado


#Registrar novo Jogador
@game.route('/api/register-player', methods=['POST'])
def register_player():
    data = request.get_json()

    # Verifica se o nome foi fornecido
    if not data or not data.get('name'):
        return jsonify({"error": "O nome do jogador é obrigatório."}), 400

    # Cria um novo jogador
    new_player = Player(name=data['name'])
    db.session.add(new_player)
    db.session.commit()

    return jsonify({"message": "Jogador registrado com sucesso!", "player_id": new_player.id}), 201

#Iniciar o Jogo
def start_game():
    """
    Rota para iniciar um novo jogo.
    """
    try:
        data = request.get_json()

        if 'player_id' not in data:
            return jsonify({'error': "O campo 'player_id' é obrigatório."}), 400

        player_id = data['player_id']

        # Validar se o jogador existe
        player = Player.query.get(player_id)
        if not player:
           return jsonify({'error': 'Jogador não encontrado.'}), 404

        # Estado inicial do tabuleiro
        initial_board = [""] * 9

        return jsonify({
            'player_id': player_id,
            'board_state': initial_board,
            'message': 'Jogo iniciado com sucesso!'
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

#Movimento Jogador
@game.route('/api/move', methods=['POST'])
def make_move():
    """
    Rota para realizar uma jogada.
    """
    try:
        data = request.get_json()

        if not all(key in data for key in ('player_id', 'position')):
            return jsonify({'error': "Os campos 'player_id' e 'position' são obrigatórios."}), 400

        player_id = data['player_id']
        position = data['position']
        board_state = data.get('board_state', [""] * 9)

        # Validar se a posição é válida
        if position < 0 or position > 8 or board_state[position] != "":
            return jsonify({'error': 'Posição inválida ou já ocupada.'}), 400

        # Atualizar o tabuleiro com a jogada do jogador
        board_state[position] = 'player'

        # Retornar o estado atualizado do tabuleiro
        return jsonify({'player_id': player_id, 'board_state': board_state}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

#Movimento Jogador / IA 
@game.route('/api/ai-move', methods=['POST'])
def ai_move():
    try:
        data = request.get_json()

        if 'board_state' not in data:
            return jsonify({'error': "O campo 'board_state' é obrigatório."}), 400

        board_state = data['board_state']
        if len(board_state) != 9:
            return jsonify({'error': "O estado do tabuleiro deve conter exatamente 9 posições."}), 400

        def encode_board(board):
            return [0 if cell == '' else (1 if cell == 'player' else 2) for cell in board]

        encoded_board = encode_board(board_state)
        next_move = model.predict([encoded_board])[0]

        while board_state[next_move] != "":
            encoded_board[next_move] = -1
            next_move = model.predict([encoded_board])[0]

        return jsonify({'board_state': board_state, 'next_move': int(next_move)})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


#Atualizar histórico
@game.route('/api/update-history', methods=['POST'])
def update_history():
    """
    Rota para atualizar o histórico de jogos no banco de dados.
    """
    try:
        data = request.get_json()

        # Validação do JSON recebido
        if not all(key in data for key in ('player_id', 'resultado', 'estado_final')):
            return jsonify({'error': 'Campos player_id, resultado e estado_final são obrigatórios.'}), 400

        # Criando um novo registro no histórico
        novo_historico = HistoricoJogos(
            player_id=data['player_id'],
            resultado=data['resultado'],
            estado_final=str(data['estado_final'])  # Converte o estado para string
        )
        db.session.add(novo_historico)
        db.session.commit()

        return jsonify({'message': 'Histórico atualizado com sucesso.'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

#Verificar Estatísticas Jogador
@game.route('/api/player-stats/<int:player_id>', methods=['GET'])
def player_stats(player_id):
    """
    Rota para obter estatísticas de jogo de um jogador.
    """
    try:
        # Query para contar vitórias, derrotas e empates
        vitorias = HistoricoJogos.query.filter_by(player_id=player_id, resultado='vitória').count()
        derrotas = HistoricoJogos.query.filter_by(player_id=player_id, resultado='derrota').count()
        empates = HistoricoJogos.query.filter_by(player_id=player_id, resultado='empate').count()

        # Retornar as estatísticas
        return jsonify({
            'player_id': player_id,
            'vitorias': vitorias,
            'derrotas': derrotas,
            'empates': empates
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
#Sugerir Melhorias   
@game.route('/api/feedback', methods=['POST'])
def game_feedback():
    """
    Rota para sugerir melhorias com base no resultado do jogo.
    """
    try:
        data = request.get_json()

        # Validação dos dados
        if not all(key in data for key in ('player_id', 'resultado', 'estado_final')):
            return jsonify({'error': 'Campos player_id, resultado e estado_final são obrigatórios.'}), 400

        player_id = data['player_id']
        resultado = data['resultado']
        estado_final = data['estado_final']

        # Atualizar o histórico do jogador
        novo_historico = HistoricoJogos(
            player_id=player_id,
            resultado=resultado,
            estado_final=str(estado_final)
        )
        db.session.add(novo_historico)
        db.session.commit()

        # Feedback básico
        if resultado == 'derrota':
            feedback = "Tente focar nas posições centrais ou bloquear as jogadas do adversário."
        elif resultado == 'empate':
            feedback = "Você está quase lá! Procure prever os movimentos da IA com base no tabuleiro."
        else:
            feedback = "Ótimo trabalho! Continue melhorando suas estratégias."

        # Retornar o feedback
        return jsonify({
            'player_id': player_id,
            'feedback': feedback,
            'estado_final': estado_final
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
