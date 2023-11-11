"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None
size_row = 3
size_col = 3


def initial_state():
    """
    Returns starting state of the  .
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    player_x_count = 0
    player_o_count = 0

    for row in board:
        for col in row:
            if col == X:
                player_x_count += 1
            elif col == O:
                player_o_count += 1

    if player_x_count <= player_o_count:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for row in range(size_row):
        for col in range(size_col):
            if board[row][col] == EMPTY:
                possible_actions.add((row, col))
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # not a valid action
    if action[0] not in [0, 1, 2] or action[1] not in [0, 1, 2]:
        raise NotImplementedError

    board_copy = deepcopy(board)
    board_copy[action[0]][action[1]] = player(board)
    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # row win:
    for row in board:
        if row.count(X) == 3:
            return X
        elif row.count(O) == 3:
            return O

    # col win:
    for col in range(size_col):
        res = ""
        for row in range(size_row):
            res += str(board[row][col])
        if res == "XXX":
            return X
        if res == "OOO":
            return O

    # Diagonals
    if board[0][0] == board[1][1] == board[2][2] == X:
        return X
    elif board[0][0] == board[1][1] == board[2][2] == O:
        return O
    elif board[0][2] == board[1][1] == board[2][0] == X:
        return X
    elif board[0][2] == board[1][1] == board[2][0] == O:
        return O

    # Otherwise no current winner, return None
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) or not actions(board):
        return True
    else:
        return False


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

    global actions_explored
    actions_explored = 0

    def max_value(board):
        global actions_explored

        value = -10
        best_move = None

        if terminal(board):
            return utility(board), None

        for action in actions(board):
            actions_explored += 1
            temp = min_value(result(board, action))[0]
            value = max(value, temp)
            if temp == value:
                best_move = action

        return value, best_move

    def min_value(board):
        global actions_explored

        value = 10
        best_move = None

        if terminal(board):
            return utility(board), None

        for action in actions(board):
            actions_explored += 1
            temp = max_value(result(board, action))[0]
            value = min(value, temp)
            if temp == value:
                best_move = action

        return value, best_move

    # The maximizing player picks action a in Actions(s) that produces the highest value of Min-Value(Result(s, a)).
    if player(board) == X:
        print('AI is exploring possible actions for X...')
        move = max_value(board)[1]
        print('Actions explored by AI: ', actions_explored)
        print('AI moves: ', move)
        return move
        # The minimizing player picks action a in Actions(s) that produces the lowest value of Max-Value(Result(s, a)).
    elif player(board) == O:
        print('AI is exploring possible actions for O......')
        move = min_value(board)[1]
        print('Actions explored by AI: ', actions_explored)
        print('AI moves: ', move)
        return move
