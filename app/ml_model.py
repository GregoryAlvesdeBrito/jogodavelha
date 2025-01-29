import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

def train_model():
    # Carregar o dataset ampliado
    df = pd.read_csv("augmented_game_moves.csv")

    # Converte o estado do tabuleiro de string para lista
    df['board_state'] = df['board_state'].apply(eval)

    # Converte os valores do tabuleiro para numéricos
    def encode_board(board):
        return [0 if cell == '' else (1 if cell == 'player' else 2) for cell in board]

    df['board_state'] = df['board_state'].apply(encode_board)

    # Transforma o tabuleiro em um vetor de features
    X = pd.DataFrame(df['board_state'].to_list())  # Cada célula vira uma coluna
    y = df['next_move']

    # Dividir o dataset em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Treinar o modelo
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Avaliação do modelo
    accuracy = model.score(X_test, y_test)
    print(f"Acurácia do modelo com o novo dataset: {accuracy * 100:.2f}%")

    # Salvar o modelo treinado
    joblib.dump(model, "ai_model.pkl")
    print("Modelo treinado e salvo como 'ai_model.pkl'")


# Carregar o modelo treinado
def load_model():
    """
    Carrega o modelo treinado salvo como 'ai_model.pkl'.
    """
    try:
        model = joblib.load("ai_model.pkl")
        return model
    except FileNotFoundError:
        raise Exception("Modelo 'ai_model.pkl' não encontrado. Treine o modelo antes de usar.")
