import copy
import ConnectFourBoard

#It tries to maximise the number of points, for just that one turn


def other(token):
    if token == ConnectFourBoard.RED:
        return ConnectFourBoard.BLUE
    elif token == ConnectFourBoard.BLUE:
        return ConnectFourBoard.RED
    else:
        return None


# estimate of a field quality
def state_score(board, token):
    (red_score, blue_score) = board.score()
    if red_score > board.winscore:
        score = 999999
    elif blue_score > board.winscore:
        score = -9999999
    else:
        score = red_score - blue_score
    if token == ConnectFourBoard.RED:
        return score
    else:
        return -score

def flip_token(token):
    if token == ConnectFourBoard.RED:
        return ConnectFourBoard.BLUE
    else:
        return ConnectFourBoard.RED


def max_play(board, token, ply_remaining, alpha, beta):
    moves = []
    for n in range (0, board.width):
        #checks if it is full
        if(board.col_height(n) < board.height):
            #creates a new version of the same board
            newboard = copy.deepcopy(board)
            newboard.field[n][newboard.col_height(n)] = token
            if ply_remaining > 0:
                min_move = min_play(newboard, flip_token(token), ply_remaining - 1)
                value = min_move[1]
                alpha = min_play(beta, value)
            else:
                max_move = max_play(newboard, flip_token(token), ply_remaining - 1)
                value = min_move[1]
                beta = max_play(beta, value)
            if alpha >= beta:
                break
                #score advantage
                value = state_score(newboard, token)
            moves.append((n, value))
            #lambda only extracts the second value so it can compare them.
    best_move = max(moves, key = lambda x: x[1])
    return best_move
#looks for the least point advantage
def min_play(board, token, ply_remaining, alpha, beta):
    moves = []
    for n in range (0, board.width):
        #checks if it is full
        if(board.col_height(n) < board.height):
            #creates a new version of the same board
            newboard = copy.deepcopy(board)
            newboard.field[n][newboard.col_height(n)] = token
            if ply_remaining > 0:
                max_move = max_play(newboard, flip_token(token), ply_remaining - 1)
                value = max_move[1]
                alpha = max_play(alpha, value)
            else:
                min_move = min_play(newboard, flip_token(token), ply_remaining - 1)
                value = max_move[1]
                beta = min_play(beta, value)
            if alpha >= beta:
                break
                #score advantage
                value = state_score(newboard, flip_token(token))
            moves.append((n, value))
            #lambda only extracts the second value so it can compare them.
    best_move = min(moves, key = lambda x: x[1])
    return best_move





def AIcheck(board, token):
    # Modify to set a different search depth
    ply_remaining = 3
    (move, value) = max_play(board, token, ply_remaining)
    return move
