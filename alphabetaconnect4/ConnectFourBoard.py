import copy

# Board tokens
RED = 1
BLUE = 2

# A few helper functions to manage board initialisation
def new_empty_board(height, width):
    return [([0] * height) for k in range(width)]

class InvalidBoard(Exception):
    pass

def valid_board(board):
    # Checks that the board is a rectangle. If it isn't, this function raises
    # an exception which interupts the program.
    if len(board) == 0:
        raise InvalidBoard('The board has no space')
    else:
        l = len(board[0])
        if any(len(col) != l for col in board):
            raise InvalidBoard('Not all columns have the same heights')
        elif l == 0:
            raise InvalidBoard('The board has no space')




class Board():

    def __init__(self, board=None, rewards=None, winscore=100):
        if board == None:
            # If no board is passed explicitely, just create one
            board = new_empty_board(8, 9)
        self.field = board
        # This next line will crash the program if the provided board is wrong
        valid_board(self.field)
        self.width = len(self.field)
        self.height = len(self.field[0])
        if rewards == None:
            # The default rewards: [0, 1, 2, 4, 8, 16, 32, etc. ]
            rewards = [0] + [ 2 ** (n - 1) for n in range(1, max(self.width, self.height)) ]
        self.rewards = rewards
        self.winscore = winscore


    def copy(self):
        # Creates a new board using the same underlying field of play
        return Board(
             board=copy.deepcopy(self.field),
             rewards=self.rewards,
             winscore=self.winscore
        )

    def col_height(self, col):
        # Finds out the height of a given column
        # This is useful for inserting tokens and for detecting if the board
        # is full.
        l = 0
        for space in self.field[col]:
            if space != 0:
                l += 1
        return l

    def not_full_columns(self):
        # This method collects all the columns that are not full. This gives a
        # list of playable columns. It is useful for AIs.
        cs = []
        for col in range(self.width):
            if self.col_height(col) < self.height:
                cs.append(col)
        return cs

    def attempt_insert(self, col, token):
        # is it possible to insert into this column?
        if self.col_height(col) < self.height:

            # add a token in the selected column
            self.field[col][self.col_height(col)] = token
            # return True for success
            return True

        else:
            # return False for Failure
            return False

    def score(self):
        return self.score_field(self.field)
    def score_field(self, field):

        #vertical scores field (column, not row)
        v_scores = self.score_vertical(field)
        #horizontal scores field (row, not colums)
        h_scores = self.score_horizontal(field)
        #upleft scores (left diagonal)
        ul_scores = self.score_upleft(field)
        #ur_scores (right diagonal)
        ur_scores = self.score_upright(field)
        #adds the total red scores
        red = v_scores['red'] + h_scores['red'] + ul_scores['red'] + ur_scores['red']
        #adds the total red scores
        blue = v_scores['blue'] + h_scores['blue'] + ul_scores['blue'] + ur_scores['blue']
        return(red, blue)

    def update_sequence(self, token, sequence, scores):
        #update sequence and scores based on where the new token is placed.
        #Checks if it is part of a row of tokens. If so, it adds to the score.
        #If not, it just dumps sequence and scores the sequence and records the new token in hopes that it is part of a sequence.
        if token == sequence['colour']:
            sequence['length'] += 1
        else:
            #update score points, breaks sequence
            if sequence['length'] > 0:
                points = self.rewards[sequence['length']-1]
            else:
                points = 0
            if sequence['colour'] == 1:
                scores['red'] += points
            elif sequence['colour'] == 2:
                scores['blue'] += points

            if token == 0:
                sequence['colour'] = 0
                sequence['length'] = 0
            else:
                sequence['colour'] = token
                sequence['length'] = 1
    def score_vertical(self, field):
        #this method checks for the sequences and passes info to update_sequence for it to be recorded.
        scores = { 'red': 0, 'blue': 0, }
        #looks through column and accumulates scores
        for column in range (0, self.width):
            #make a sequence value to keep info on the column
            sequence = {'length':0,'colour':0,}
            #the actual loop through column
            for row in range(0, self.height):
                #update score and sequence based on the colour of the token
                token = field[column][row]
                self.update_sequence(token, sequence, scores)
            #check the sequence at the end of the line
            self.update_sequence(0, sequence, scores)
        return scores

    def score_horizontal(self, field):
        #this method checks for the sequences and passes info to update_sequence for it to be recorded.
        scores = { 'red': 0, 'blue': 0, }
        #looks through column and accumulates scores
        for row in range (0, self.height):
            #make a sequence value to keep info on the column
            sequence = {'length':0,'colour':0,}
            #the actual loop through column
            for col in range(0, self.width):
                #update score and sequence based on the colour of the token
                token = field[col][row]
                self.update_sequence(token, sequence, scores)
            #check the sequence at the end of the line
            self.update_sequence(0, sequence, scores)
        return scores

    def score_upright (self, field):
        #in theory, this should check through the rows and cols and return the score
        scores = { 'red': 0, 'blue': 0, }
        for col in range(0, self.width):
            sequence = {'length':0,'colour':0,}
            for row in range (0, self.height):
                if col + row < self.width:
                    token = field [col + row][row]
                else:
                    token = 0
                self.update_sequence(token, sequence, scores)

            self.update_sequence(0, sequence, scores)
        # bigger outer loop, deals with moving across
        for row in range (1, self.height):
            #resets for each sequence
            sequence = {'length':0,'colour':0,}
            for col in range (0, self.width):
                if col + row < self.height:
                    token = field [col][row + col]
                else:
                    token = 0
                self.update_sequence(token, sequence, scores)

            self.update_sequence(0, sequence, scores)
        return scores

    def score_upleft(self, field):
        return self.score_upright(list(reversed(field)))













    def is_full(self):
        # TODO: You need to implement this method
        return False




# This additional class simply creates an empty board of a given size.
# Note the `Board` between brackets (`(` and `)`). This means that the methods
# from the class `Board` are available in the class `EmptyBoard`. In other
# words, `EmptyBoard` is just a special case of the general case `Board`.
class EmptyBoard(Board):

    # Function to set up the objects of this class
    def __init__(self, height=8, width=9, rewards=None, winscore=100):
        # Create a simple empty board with the right height and width
        fresh_board = new_empty_board(height, width)
        # Then, proceed to set-up as in `Board`. The `super()` part refers to
        # the class `Board`.
        Board.__init__(self, fresh_board, rewards, winscore)
