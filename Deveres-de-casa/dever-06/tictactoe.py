"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count_x = sum(row.count(X) for row in board)
    count_o = sum(row.count(O) for row in board)

    if count_x == count_o:
        return X
    elif count_x > count_o:
        return O
    else:
        # Isso não deveria ocorrer em um estado de jogo válido
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # 1. Validação da ação
    if not isinstance(action, tuple) or len(action) != 2:
        raise TypeError("Ação deve ser uma tupla (linha, coluna).")
    
    i, j = action
    
    if not (0 <= i < 3 and 0 <= j < 3):
        raise ValueError("Coordenadas de ação fora dos limites do tabuleiro (0-2).")
    
    if board[i][j] != EMPTY:
        raise ValueError("A célula já está ocupada. Ação inválida.")

    # 2. Criação de uma cópia profunda do tabuleiro
    new_board = [row[:] for row in board]

    # 3. Realiza o movimento no novo tabuleiro
    player_to_move = player(board) 
    new_board[i][j] = player_to_move
    
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Verifica linhas e colunas
    for i in range(3):
        # Linha
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != EMPTY:
            return board[i][0]
        # Coluna
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != EMPTY:
            return board[0][i]
            
    # Verifica diagonais
    # Diagonal principal (0,0) -> (2,2)
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return board[0][0]
    # Diagonal secundária (0,2) -> (2,0)
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != EMPTY:
        return board[0][2]
            
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # O jogo termina se houver um vencedor OU se não houver mais ações possíveis (empate)
    return winner(board) is not None or not actions(board)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_symbol = winner(board)
    
    if winner_symbol == X:
        return 1
    elif winner_symbol == O:
        return -1
    else:
        # Se não há vencedor, e é terminal, deve ser um empate
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # Se o jogo acabou, não há jogadas possíveis
    if terminal(board):
        return None

    current_player = player(board)

    # Função para o jogador MAX (X)
    def max_value(state):

        if terminal(state):
            return utility(state)

        v = -math.inf

        for action in actions(state):
            v = max(v, min_value(result(state, action)))

        return v

    # Função para o jogador MIN (O)
    def min_value(state):

        if terminal(state):
            return utility(state)

        v = math.inf

        for action in actions(state):
            v = min(v, max_value(result(state, action)))

        return v

    # Escolha da melhor ação
    best_action = None

    if current_player == X:

        best_score = -math.inf

        for action in actions(board):

            score = min_value(result(board, action))

            if score > best_score:
                best_score = score
                best_action = action

    else:  # jogador O

        best_score = math.inf

        for action in actions(board):

            score = max_value(result(board, action))

            if score < best_score:
                best_score = score
                best_action = action

    return best_action
