# Jogo da Velha com Flask e Machine Learning

## Sobre o Projeto

Este projeto é uma API para o jogo da velha desenvolvida em Flask, com suporte para identificação de jogadores e um modelo de Machine Learning que toma decisões baseadas em um histórico de jogadas. Ele utiliza MySQL como banco de dados e inclui funcionalidades adicionais, como estatísticas de jogadores e feedback para melhoria no desempenho.

## Estrutura do Projeto

```
Dev/
|-- app/
|   |-- routes/
|   |   |-- __init__.py
|   |   |-- game.py
|   |   |-- api_routes.py
|   |-- __init__.py
|   |-- models.py
|   |-- ml_model.py
|   |-- routes.py
|-- tests/
|   |-- test_model.py
|-- requirements.txt
|-- run.py
|-- README.md



```

## Funcionalidades

1. **Cadastro de jogadores**

   - Registro de jogadores com ID único, nome e histórico de jogos.

2. **Jogo da velha**

   - Lógica do jogo implementada com validação de jogadas, condições de vitória e empate.

3. **Inteligência Artificial**

   - Utilização de Machine Learning para sugerir as melhores jogadas com base em um histórico armazenado no banco de dados.

4. **Estatísticas de jogadores**

   - Número de vitórias, derrotas e empates por jogador.

5. **Feedback do jogo**

   - Sugestões de melhoria baseadas no desempenho do jogador.

## Pré-requisitos

- Python 3.9+
- MySQL

## Configuração do Ambiente

1. **Clonar o repositório**

   ```bash
   git clone <url-do-repositorio>
   cd project
   ```

2. **Criar o ambiente virtual**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate    # Windows
   ```

3. **Instalar as dependências**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar o banco de dados**

   - Certifique-se de que o MySQL está rodando e crie o banco de dados:

     ```sql
     CREATE DATABASE jogo_da_velha;
     ```

   - Configure as variáveis de conexão no arquivo `app/__init__.py`:

     ```python
     app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1:3306/jogo_da_velha'
     ```

5. **Executar as migrações**

   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

6. **Rodar o servidor**

   ```bash
   flask run
   ```

## Rotas da API

- Blibioteca de Requisitos:
   - [Insonia](https://insomnia.rest/)
      [Package.json]

### **Jogadores**

- `POST /api/register`
  - Cadastrar um novo jogador.
  - **Payload:** `{ "name": "Nome do Jogador" }`
  - **Resposta:** `{ "player_id": 1, "name": "Nome do Jogador" }`

- `POST /api/start`
  - Inicia um novo jogo.
  - **Payload:** `{ "player_id": 1 }`
  - **Resposta:** Estado inicial do tabuleiro.

### **Jogo da Velha**

- `POST /api/move`
  - Realiza uma jogada.
  - **Payload:** `{ "player_id": 1, "position": 4, "board_state": ["", "", "", "", "", "", "", "", ""] }`
  - **Resposta:** Estado atualizado do tabuleiro.

### **Machine Learning**

- `POST /api/ai-move`

  - Sugere a próxima jogada.
  - **Payload:** `{ "board_state": ["", "", "", "", "player", "", "", "", "ai"] }`
  - **Resposta:** `{ "board_state": [...], "next_move": 3 }`

- `POST /api/update-history`

  - Atualiza o histórico de jogos no banco de dados.
  - **Payload:** `{ "player_id": 1, "resultado": "vitoria", "estado_final": ["ai", "player", "ai", "player", "ai", "", "", "", "player"] }`

### **Estatísticas e Feedback**

- `GET /api/player-stats/<player_id>`
  - Retorna estatísticas do jogador.
  - **Resposta:** `{ "player_id": 1, "vitorias": 5, "derrotas": 3, "empates": 2 }`

## Testes

- Execute os testes unitários com o seguinte comando:
  ```bash
  python -m unittest discover tests
  ```

## Melhorias Futuras

- Implementar uma interface web para interação com o jogo.
- Melhorar o modelo de Machine Learning com mais dados e maior precisão.
- Adicionar suporte para partidas multiplayer em tempo real.

---

Projeto desenvolvido com Flask, SQLAlchemy e scikit-learn. 🚀



Gregory Brito
🎯 Desenvolvedor Fullstack | Designer Gráfico e UX/UI | Analista e Desenvolvedor de Sistemas
Sou um Desenvolvedor Fullstack com sólida experiência em Python e Django, especializado na criação de aplicações web escaláveis, design de APIs RESTful e otimização de bancos de dados relacionais. Combinando habilidades em back-end e front-end, desenvolvo interfaces funcionais e atrativas com foco em usabilidade (UX/UI) e design responsivo.

📍 Localização: Mooca - São Paulo
📫 Contato: gregory.brito@hotmail.com

