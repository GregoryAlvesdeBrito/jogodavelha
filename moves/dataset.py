import random
import pandas as pd

def generate_game_states(num_samples=1000):
    """
    Gera um dataset de estados de jogo da velha e as melhores jogadas.
    """
    data = []

    for _ in range(num_samples):
        # Cria um tabuleiro vazio
        board = [''] * 9
        # Número de jogadas aleatórias já feitas no tabuleiro
        num_moves = random.randint(0, 8)
        # Preenche o tabuleiro com jogadas aleatórias
        for move in range(num_moves):
            position = random.choice([i for i in range(9) if board[i] == ''])
            board[position] = 'player' if move % 2 == 0 else 'ai'
        # Determina a próxima jogada ideal (posição vazia aleatória neste exemplo)
        available_positions = [i for i in range(9) if board[i] == '']
        if available_positions:
            next_move = random.choice(available_positions)
        else:
            next_move = None  # Tabuleiro cheio

        if next_move is not None:
            data.append({'board_state': str(board), 'next_move': next_move})

 
    return pd.DataFrame(data)

dataset = generate_game_states(num_samples=1000)
dataset.to_csv('game_moves.csv', index=False)
print("Dataset Gerado e salvo como 'game_moves.csv'")
