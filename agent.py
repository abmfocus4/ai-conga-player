import constants as const
import math
# col first, row second
# col [0], row [1]
# TODO: switch and check
class Agent:
    def __init__(self, player_type):
        super().__init__()

        self.player_type = player_type
        self.num_nodes_explored = 0
        self.depth = 0

    def move_directions(self):
        directions = set()
        # move coordinates with current location as origin
        for i in range(-1,2):
            for j in range(-1,2):
                directions.add((i,j))
        directions.remove((0,0))

        return directions  

    # given source and direction coordinates, return move
    # TODO swap?
    def get_move(self, src_col, src_row, dir):
        # print('get move')
        # print(src_col, src_row, dir)
        return (src_col+dir[0], src_row+dir[1])
      

    # checks if move does not take player outside the board +
    # is not occupied by opponent
    def is_valid_move(self, col, row, direction, opponent_squares):
        dest = (col+direction[0], row+direction[1])
        if (dest[1] >= 1) and (dest[1] <= const.ROWS) and (dest[0] >= 1) and (dest[0] <= const.COLS) and (dest not in opponent_squares):
            return True
        return False
    
    # moving stones on the board
    def update_board(self, board, src, dest, given_stones, player_squares):
        # print('begin')
        # print('given stones')
        # print(given_stones)
        # print(player_squares)
        total_stones = board.stones[src[0]][src[1]]
        # print('src')
        # print(src)
        # print('total_stones')
        # print(total_stones)

        stones = 0
        if given_stones > total_stones:
            stones = total_stones 
        else:
            stones = given_stones
        if stones>0:
            if not board.player[dest[0]][dest[1]] == self.player_type:
                board.player[dest[0]][dest[1]] = self.player_type

            board.stones[dest[0]][dest[1]] += stones
            board.stones[src[0]][src[1]] -= stones
            player_squares.add(dest)
            if board.stones[src[0]][src[1]] <= 0:
                board.stones[src[0]][src[1]] = 0
                board.player[src[0]][src[1]] = const.NULL
                if src in player_squares:
                    player_squares.remove(src)

            print('Move: Board updated by moving '+str(stones)+' stones from '+str(src)+' to '+str(dest))

    def static_eval(self, player_squares, opponent_squares):
        cost = 0
        # directions = self.move_directions()

        # for square in player_squares:
        #     for dir in directions:
        #         if self.is_valid_move(square[0], square[1], dir, opponent_squares):
        #             cost += 4
                
        # for square in opponent_squares:
        #     for dir in directions:
        #         if self.is_valid_move(square[0], square[1], dir, opponent_squares):
        #             cost -=2
        
        cost = len(opponent_squares) - len(player_squares)
        return cost

    def minimizing_player(self, white_locations, black_locations, max_eval):
        min_eval = math.inf
        my_squares = set(white_locations)
        opponent_squares = set(black_locations)

        # no need to collect moves here, we have random minimizing player

        # just collections new squares that will be occupied by white

        directions = self.move_directions()
        for square in my_squares:
            for dir in directions:
                print('min player')
                new_squares = set(my_squares)

                if self.is_valid_move(square[0], square[1], dir, opponent_squares):
                    first = self.get_move(square[0], square[1], dir)
                    new_squares.add(first)

                    if self.is_valid_move(first[0], first[1], dir, opponent_squares):
                        second = self.get_move(first[0], first[1], dir)
                        new_squares.add(second)

                        if self.is_valid_move(second[0], second[1], dir, opponent_squares):
                            third = self.get_move(second[0], second[1], dir)
                            new_squares.add(third)

                    eval = self.static_eval(opponent_squares, new_squares)

                    if eval < max_eval:
                        return eval

                    if eval < min_eval:
                        min_eval = eval
        return min_eval

    def maximizing_player(self, white_locations, black_locations):
        final_moves = list()

        max_eval = -math.inf
        my_squares = set(black_locations)
        opponent_squares = set(white_locations)

        directions = self.move_directions()
        for square in my_squares:
            for dir in directions:
                print('here')
                new_squares = set(my_squares)
                current_moves = list()

                if self.is_valid_move(square[0], square[1], dir, opponent_squares):
                    first = self.get_move(square[0], square[1], dir)
                    new_squares.add(first)
                    current_moves.append(square)
                    current_moves.append(first)

                    if self.is_valid_move(first[0], first[1], dir, opponent_squares):
                        second = self.get_move(first[0], first[1], dir)
                        new_squares.add(second)
                        current_moves.append(second)

                        if self.is_valid_move(second[0], second[1], dir, opponent_squares):
                            third = self.get_move(second[0], second[1], dir)
                            new_squares.add(third)
                            current_moves.append(third)
                    # max_eval = alpha
                    eval = self.minimizing_player(white_locations, new_squares, max_eval)

                    if eval >= max_eval:
                        max_eval = eval
                        final_moves = current_moves
        return final_moves

    def child_eval(self, player_stones, opponent_stones, current_best):
        best_eval = math.inf
        directions = self.move_directions()
        for col, row in opponent_stones:
            for dir in directions:
                first = self.get_move(col, row, dir)

                if self.is_valid_move(col, row, dir, player_stones):
                    potential_stones = set(opponent_stones)
                    potential_stones.add(first)

                    second = self.get_move(first[0], first[1], dir)
                    if self.is_valid_move(first[0], first[1], dir, player_stones):
                        potential_stones.add(second)
                        
                        third = self.get_move(second[0], second[1], dir)
                        if self.is_valid_move(second[0], second[1], dir, player_stones):
                            potential_stones.add(third)

                    eval = len(player_stones) - len(potential_stones)
                    if eval < current_best:
                        return eval
                    if eval < best_eval:
                        best_eval = eval
        return best_eval



    # return (board + valid)
    def make_move(self, board, white_locations, black_locations):
        # print("sent board")
        # board.display()
        # create sets of squares that are occupied by current player and opponent
        my_squares = set()
        opponent_square = set()
        if (self.player_type == const.WHITE):
            my_squares = white_locations
            opponent_squares = black_locations
        else:
            my_squares = black_locations
            opponent_squares = white_locations

        # directions player can move in
        directions = self.move_directions()

        # random agent move
        if self.player_type == const.RANDOM:
            print('Random Agent: WHITE playing')
            # selecting initial square
            for square in my_squares:
                # TODO: switch row, col
                col = square[0]
                row = square[1]
                for direction in directions:
                    if self.is_valid_move(col, row, direction, opponent_squares):
                        num_stones = board.stones[col][row]
                        first = self.get_move(col, row, direction)
                        # if second pos is invalid - move all stones to first
                        second = self.get_move(first[0], first[1], direction)
                        if not self.is_valid_move(first[0], first[1], direction, opponent_squares):
                            # print('1')
                            # print(second)
                            # print(direction)
                            self.update_board(board, square, first, num_stones, my_squares)
                            # set white_locations after update
                            black_locations = set(opponent_squares)
                            white_locations = set(my_squares)
                            board.valid_move = True
                            return board
                        else:
                            # if third pos is invalid - move 1 stone to first pos and others to second
                            third = self.get_move(second[0], second[1], direction)
                            # print(third)
                            if not self.is_valid_move(second[0], second[1], direction, opponent_squares):
                                # print('2')
                                self.update_board(board, square, first, 1, my_squares)
                                self.update_board(board, square, second, num_stones-1, my_squares)
                                # set white_locations after update
                                black_locations = set(opponent_squares)
                                white_locations = set(my_squares)
                                board.valid_move = True
                                return board
                            else:
                                # print('3')
                                self.update_board(board, square, first, 1, my_squares)
                                self.update_board(board, square, second, 2, my_squares)
                                self.update_board(board, square, third, num_stones-3, my_squares)
                                # print(board.stones)
                                # set white_locations after update
                                # print(my_squares)
                                black_locations = set(opponent_squares)
                                white_locations = set(my_squares)
                                board.valid_move = True
                                return board           
            print('Unable to move, surrounded by black squares. '+const.STR_RANDOM+' has lost to '+const.STR_COMPUTER+'.')
            board.valid_move = False
            return board
        
        # computer move
        else:
            print('Computer: BLACK playing')
            # moves = list()
            # (moves) = self.maximizing_player(white_locations, black_locations)

            ######

            best_move = list()
            best_eval = -math.inf
            directions = self.move_directions()
            for col, row in black_locations:
                for dir in directions:
                    first = self.get_move(col, row, dir)
                    complete_move = list()

                    if self.is_valid_move(col, row, dir, white_locations):
                        potential_locations = set(black_locations)
                        potential_locations.add(first)

                        complete_move.append((col, row))
                        complete_move.append(first)

                        second = self.get_move(first[0], first[1], dir)
                        if self.is_valid_move(first[0], first[1], dir, white_locations):
                            potential_locations.add(second)
                            complete_move.append(second)

                            third = self.get_move(second[0], second[1], dir)
                            if self.is_valid_move(second[0], second[1], dir, white_locations):
                                potential_locations.add(third)
                                complete_move.append(third)
                        eval = self.child_eval(potential_locations, white_locations, best_eval)
                        
                        if eval >= best_eval:
                            best_move = complete_move
                            best_eval = eval

            num_moves = len(best_move)
            moves = list(best_move)
            # my_squares = black_locations
            ######

            # num_moves = len(moves)
            # print(moves)
            if num_moves == 0:
                print('Unable to move, surrounded by white squares. '+const.STR_COMPUTER+' has lost to '+const.STR_RANDOM+'.')
                board.valid_move = False
                return board
            else:
                initial = moves[0]
                col = initial[0]
                row = initial[1]
                num_stones = board.stones[col][row]
                if num_moves == 4:
                    # print('4')
                    # print(best_move)
                    # print(num_stones)
                    # print(moves)
                    self.update_board(board, initial, moves[1], 1, black_locations)
                    self.update_board(board, initial, moves[2], 2, black_locations)
                    self.update_board(board, initial, moves[3], num_stones-3, black_locations)
                elif num_moves == 3:
                    # print('3')
                    self.update_board(board, initial, moves[1], 1, black_locations)
                    self.update_board(board, initial, moves[2], num_stones-1, black_locations)
                elif num_moves == 2:
                    # print('2')
                    self.update_board(board, initial, moves[1], num_stones, black_locations)
                # set black_locations after update
                # black_locations = set(black_locations)
                # white_locations = set(white_locations)
                board.valid_move = True
                return board
        print('Unable to move, surrounded by white squares. ' + const.STR_COMPUTER + ' has lost to ' + const.STR_RANDOM + '.')
        board.valid_move = False
        return board
