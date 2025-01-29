import random
import pandas as pd
import numpy as np

def generate_game_states(num_samples=1000):
    """
    Gera um dataset de estados do jogo da velha com jogadas inteligentes.
    """
    data = []

    def check_victory(board, player):
        """
        Verifica se o jogador 'player' venceu no tabuleiro.
        """
        win_positions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Linhas
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Colunas
            [0, 4, 8], [2, 4, 6]             # Diagonais
        ]
        for positions in win_positions:
            if all(board[pos] == player for pos in positions):
                return True
        return False

    def find_best_move(board):
        """
        Retorna a melhor jogada para a IA, seguindo regras básicas.
        """
        # 1. Verificar se a IA pode vencer em uma jogada
        for i in range(9):
            if board[i] == '':
                board[i] = 'ai'
                if check_victory(board, 'ai'):
                    board[i] = ''  # Reverte a jogada
                    return i
                board[i] = ''

        # 2. Bloquear vitória do jogador
        for i in range(9):
            if board[i] == '':
                board[i] = 'player'
                if check_victory(board, 'player'):
                    board[i] = ''  # Reverte a jogada
                    return i
                board[i] = ''

        # 3. Caso contrário, escolha aleatoriamente
        available_positions = [i for i, cell in enumerate(board) if cell == '']
        return random.choice(available_positions)

    for _ in range(num_samples):
        # Cria um tabuleiro vazio
        board = [''] * 9

        # Número de jogadas aleatórias já feitas
        num_moves = random.randint(0, 8)

        # Preenche o tabuleiro com jogadas aleatórias
        for move in range(num_moves):
            position = random.choice([i for i in range(9) if board[i] == ''])
            board[position] = 'player' if move % 2 == 0 else 'ai'

        # Determina a próxima jogada ideal
        if '' in board:
            next_move = find_best_move(board)
            data.append({'board_state': str(board), 'next_move': next_move})

    # Criar um DataFrame
    return pd.DataFrame(data)

def augment_data_with_symmetry(df):
    """
    Amplia o dataset usando simetria (espelhamento e rotação).
    """
    augmented_data = []

    def rotate_board(board):
        """Roda o tabuleiro 90 graus no sentido horário."""
        return [
            board[6], board[3], board[0],
            board[7], board[4], board[1],
            board[8], board[5], board[2]
        ]

    def mirror_board(board):
        """Espelha o tabuleiro horizontalmente."""
        return [
            board[2], board[1], board[0],
            board[5], board[4], board[3],
            board[8], board[7], board[6]
        ]

    for _, row in df.iterrows():
        board = eval(row['board_state'])
        next_move = row['next_move']

        # Adiciona o estado original
        augmented_data.append({'board_state': str(board), 'next_move': next_move})

        # Adiciona estados rotacionados e espelhados
        rotated_board = board
        for _ in range(3):
            rotated_board = rotate_board(rotated_board)
            augmented_data.append({'board_state': str(rotated_board), 'next_move': next_move})

        mirrored_board = mirror_board(board)
        augmented_data.append({'board_state': str(mirrored_board), 'next_move': next_move})

    return pd.DataFrame(augmented_data)

# Gerar dataset inicial
dataset = generate_game_states(num_samples=1000)

# Ampliar com simetria
augmented_dataset = augment_data_with_symmetry(dataset)

# Salvar o dataset
augmented_dataset.to_csv('augmented_game_moves.csv', index=False)
print("Dataset ampliado e salvo como 'augmented_game_moves.csv'")
