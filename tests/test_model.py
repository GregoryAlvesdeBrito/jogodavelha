import joblib
import numpy as np

def test_ai_move(board_state):
    """
    Testa a IA para decidir a melhor jogada com base no estado atual do tabuleiro.
    """
    # Carregar o modelo treinado
    model = joblib.load("ai_model.pkl")

    # Converte o estado do tabuleiro para valores numéricos
    def encode_board(board):
        return [0 if cell == '' else (1 if cell == 'player' else 2) for cell in board]

    encoded_board = encode_board(board_state)

    # Predizer a melhor jogada
    next_move = model.predict([encoded_board])[0]
    return next_move

# Cenários para teste
if __name__ == "__main__":
    test_boards = [
        # Cenário 1: IA deve vencer
        ['ai', 'ai', '', 
         '', 'player', '', 
         '', '', ''],

        # Cenário 2: IA deve bloquear
        ['player', 'player', '', 
         '', 'ai', '', 
         '', '', ''],

        # Cenário 3: Jogada aleatória
        ['player', '', '', 
         '', 'ai', '', 
         '', '', 'ai']
    ]

    for i, board in enumerate(test_boards):
        print(f"Cenário {i + 1} - Tabuleiro:")
        print(np.array(board).reshape(3, 3))
        move = test_ai_move(board)
        print(f"IA sugere a próxima jogada na posição: {move}\n")
