from app import db
from datetime import datetime

# Jogadores
class Player(db.Model):
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    wins = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)
    draws = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "wins": self.wins,
            "losses": self.losses,
            "draws": self.draws,
            "created_at": self.created_at
        }
    
# Jogo
class Game(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    board_state = db.Column(db.String(255), nullable=False)  # Exemplo: "['', '', '', '', '', '', '', '', '']"
    turn = db.Column(db.Enum('player', 'ai'), default='player', nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    winner = db.Column(db.Enum('player', 'ai', 'draw'), default=None)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "player_id": self.player_id,
            "board_state": eval(self.board_state),  # Converte string para lista
            "turn": self.turn,
            "is_active": self.is_active,
            "winner": self.winner,
            "created_at": self.created_at
        }
# Funcionalidades
def check_winner(board):
    """
    Verifica se há um vencedor no jogo.
    Retorna 'player', 'ai', ou None se não houver vencedor.
    """
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Linhas
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Colunas
        [0, 4, 8], [2, 4, 6]             # Diagonais
    ]

    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] and board[combo[0]] != '':
            return board[combo[0]]  # Retorna 'player' ou 'ai'

    return None

def is_draw(board):
    """
    Verifica se o jogo terminou em empate.
    """
    return all(cell != '' for cell in board) and not check_winner(board)

class HistoricoJogos(db.Model):
    __tablename__ = 'historico_jogos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    player_id = db.Column(db.Integer, nullable=False)
    resultado = db.Column(db.String(10), nullable=False)  # 'vitória', 'derrota', 'empate'
    estado_final = db.Column(db.Text, nullable=False)  # Tabuleiro final como string
    data_jogo = db.Column(db.DateTime, default=datetime.utcnow)