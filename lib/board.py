import sys
from lib import constants as const

# 4x4 board
# player1 has 10b (1,4) , player2 has 10w (4,1)
class CongaBoard():
    def __init__(self):
        super().__init__()
        # who occupies the square
        self.player = dict()
        # how many pieces in the square
        self.pieces = dict()

        # initialize board - no player, no pieces
        for row in range (1,const.ROWS+1):
            self.player[row] = dict()
            self.pieces[row] = dict()
            for col in range(1,const.COLS+1):
                self.player[row][col] = const.NULL
                self.pieces[row][col] = 0


        # first positions
        # Player1 at (1,4) has 10 black pieces
        self.player[1][4] = const.BLACK
        self.pieces[1][4] = 10

        # Player2 at (4,1) has 10 white pieces
        self.player[4][1] = const.WHITE
        self.pieces[4][1] = 10

    def display(self):
        pass   




        