"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

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
    Xcount = 0
    Ocount = 0

    for v in board:
        for h in v:
            if h == X:
                Xcount += 1
            elif h == O:
                Ocount += 1
    
    #    print("x count", Xcount) #debug
    #     print("o count", Ocount)#debug
    if Xcount <= Ocount:
        return X
    
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()

    for i, x in enumerate(board):
        for j, y in enumerate(x):
            if y == EMPTY:
                possible_actions.add((i, j))

    return possible_actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    player_ = player(board)
    new_board = deepcopy(board)

    i, j = action

    if board[i][j] != None:
        raise Exception
    else:
        new_board[i][j] = player_
    
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for player in (X, O):

        for row in board:
            if row == [player] * 3:
                return player
        
        for i in range(3):
            column = [board[x][i] for x in range(3)]
            if column == [player] * 3:
                return player
            
        if [board[i][i] for i in range(3)] == [player] * 3:
            return player

        elif [board[i][~i] for i in range(3)] == [player] * 3:
            return player

    return None 


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    
    for row in board:
        if EMPTY in row:
            return False
        
    return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_ = winner(board)

    if winner_ == X:
        return 1
    
    elif winner_ == O:
        return -1
    
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    if player(board) == X:
        #         print("X's turn")
        #         print_board(board)
        value = float('-inf')   
        best_move = None
        #        print('minimax',value,'best move:',best_move )
        for action in actions(board):
            #            print('action',action,)
            min_val = minvalue(result(board, action))

            if min_val > value:
                #                print('min val greater than previous max values ',min_val>value , 'new value :',min_val ,'previous value :
                value = min_val
                best_move = action
        
        return best_move
    
    elif player(board) == O:
        #         print("O's Turn")
        #         print_board(board)
        value = float('+inf')
        best_move = None
        for action in actions(board):
            max_val = maxvalue(result(board, action))
            #             print('max val is ',max_val)

            if max_val < value:
                value = max_val
                best_move = action
        
        return best_move
    
def minvalue(board):
    if terminal(board):
        return utility(board)
    
    max_value = math.inf
    for action in actions(board):
        max_value = min(max_value, maxvalue(result(board, action)))
    

    return max_value

def maxvalue(board):
    if terminal(board):
        return utility(board)
    
    min_value = -math.inf
    for action in actions(board):
        min_value = max(min_value, minvalue(result(board, action)))

    return min_value
