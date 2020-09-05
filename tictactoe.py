"""
Tic Tac Toe Player
"""

import math
import pdb
import copy

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
    empties = 0
    for i in board:
        for j in i:
            if j == EMPTY:
                empties = empties + 1
    if empties % 2 == 1:
        return X
    return O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    actions = []
    
    for i in range(3):
        for j in range(3):
            if board[i][j] is EMPTY:
                actions.append((i, j))

    return actions


def result(board, action):

    currentplayer = player(board)

    board2 = copy.deepcopy(board)

    if currentplayer == X:

        if board2[action[0]][action[1]] == X or board2[action[0]][action[1]] == O:

            raise RuntimeError('Move not possible')

        board2[action[0]][action[1]] = currentplayer

    else:

        if board2[action[0]][action[1]] == X or board2[action[0]][action[1]] == O:

            raise ValueError('Move not possible')

        board2[action[0]][action[1]] = currentplayer

    return board2




def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    potential_wins = []

    # 3 in a row
    for row in board:
        potential_wins.append(set(row))

    # 3 in a column
    for i in range(3):
        potential_wins.append(set([board[k][i] for k in range(3)]))

    # 3 in a diagonal
    potential_wins.append(set([board[i][i] for i in range(3)]))
    potential_wins.append(set([board[i][2 - i] for i in range(3)]))

    # Checking if any three are the same
    for i in potential_wins:
        if i == {X}:
            return X
        elif i == {O}:
            return O
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    
    if winner(board) == X:
        return True
    elif winner(board) == O:
        return True
    
    for i in board:
        for j in i:
            if j == EMPTY:
                return False
    return True
        


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0
    
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    set_possible_actions = actions(board)
    possible_actions = []
    currentplayer = player(board)
    for current_action in set_possible_actions:
        if currentplayer == X:
            action_result = min_minimax(result(board, current_action))
        else:
            action_result = max_minimax(result(board, current_action))
        possible_actions.append([current_action, action_result])
    best_action = possible_actions[0]
    for current_action in possible_actions:
        if currentplayer == X:
            if current_action[1] > best_action[1]:
                best_action = current_action
        else:
            if current_action[1] < best_action[1]:
                best_action = current_action
    if terminal(board):
        return None
    return best_action[0]


def max_minimax(board):
    if terminal(board):
        return utility(board)
    else:
        score = -math.inf
        for action in actions(board):
            score = max(score, min_minimax(result(board, action)))

        return score

def min_minimax(board):
    if terminal(board):
        return utility(board)
    else:
        score = math.inf
        for action in actions(board):
            score = min(score, max_minimax(result(board, action)))

        return score