import sys, pickle
import constants as const

# 4x4 board
# player1 has 10b (1,4) , player2 has 10w (4,1)
class CongaBoard():
    def __init__(self):
        super().__init__()
        # who occupies the square
        self.player = dict()
        # how many stones in the square
        self.stones = dict()
        # flag to determine if board is returned after playing valid move
        self.valid_move = False

        # initialize board - no player, no stones
        for row in range (1,const.ROWS+1):
            self.player[row] = dict()
            self.stones[row] = dict()
            for col in range(1,const.COLS+1):
                self.player[row][col] = const.NULL
                self.stones[row][col] = 0


        # first positions
        # Player1 at (1,4) has 10 black stones
        self.player[1][4] = const.BLACK
        self.stones[1][4] = 10

        # Player2 at (4,1) has 10 white stones
        self.player[4][1] = const.WHITE
        self.stones[4][1] = 10

    def display(self):
        keys = self.stones.keys()
        reversed = pickle.loads(pickle.dumps(list(keys)))
        reversed.reverse()

        # print row column numbers
        sys.stdout.write('\n     1     2     3      4')
        sys.stdout.write('\n     _____ _____ _____ _____\n')

        # print number of stones in square
        for col in reversed:
            sys.stdout.write('    |     |     |     |     |\n    |')
            for row in keys:
                # set color
                player_type = self.player[row][col]
                if player_type == const.BLACK:
                    color = const.PURPLE
                elif player_type == const.WHITE:   
                    color = const.RED
                else:
                    color = const.GREEN
                
                # print row
                num_stones = str(self.stones[row][col])
                if len(num_stones) == 1:
                    num_stones = ' ' + num_stones
                sys.stdout.write(' ' + color + num_stones + '\033[0m' + '  |')

            # print bottom of row with row number
            sys.stdout.write('\n ' + str(col) + '  |_____|_____|_____|_____|\n')

        print("")