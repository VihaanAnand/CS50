"""
Tic Tac Toe Player
"""

import copy
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
    x_count = 0
    o_count = 0
    for i in board:
        for j in i:
            if j == X:
                x_count += 1
            elif j == O:
                o_count += 1
    if o_count == x_count:
        return X
    return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    output = set()
    for i in range(len(board)):
        row = board[i]
        for j in range(len(row)):
            cell = row[j]
            if cell == EMPTY:
                output.add((i, j))
    return output


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board_copy = copy.deepcopy(board)
    possible_actions = actions(board_copy)
    if action not in possible_actions:
        raise ValueError("The \"action\" is not a valid action for the \"board\".")
    cur_player = player(board_copy)
    board_copy[action[0]][action[1]] = cur_player
    return board_copy


def three_in_a_row(cell1, cell2, cell3):
    if cell1 != EMPTY and cell1 == cell2 and cell1 == cell3:
        return cell1
    return EMPTY


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    cur_winner = None
    for i in range(3):
        if cur_winner == None or cur_winner == EMPTY:
            cur_winner = three_in_a_row(board[i][0], board[i][1], board[i][2])
    for i in range(3):
        if cur_winner == None or cur_winner == EMPTY:
            cur_winner = three_in_a_row(board[0][i], board[1][i], board[2][i])
    if cur_winner == None or cur_winner == EMPTY:
        cur_winner = three_in_a_row(board[0][0], board[1][1], board[2][2])
    if cur_winner == None or cur_winner == EMPTY:
        cur_winner = three_in_a_row(board[2][0], board[1][1], board[0][2])
    if cur_winner == None or cur_winner == EMPTY:
        return None
    return cur_winner


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    game_over = True
    for i in board:
        for j in i:
            if j == EMPTY:
                game_over = False
    return game_over


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    return 0


def max_value(state):
    v = float("-inf")
    if terminal(state):
        return utility(state)
    for action in actions(state):
        v = max(v, min_value(result(state, action)))
    return v


def min_value(state):
    v = float("inf")
    if terminal(state):
        return utility(state)
    for action in actions(state):
        v = min(v, max_value(result(state, action)))
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    cur_player = player(board)
    if terminal(board) == True:
        return None
    if cur_player == X:
        possible_actions = actions(board)
        highest = [float("-inf"), None]
        for action in possible_actions:
            value = min_value(result(board, action))
            if value > highest[0]:
                highest = [value, action]
        return highest[1]
    else:
        possible_actions = actions(board)
        highest = [float("inf"), None]
        for action in possible_actions:
            value = max_value(result(board, action))
            if value < highest[0]:
                highest = [value, action]
        return highest[1]
