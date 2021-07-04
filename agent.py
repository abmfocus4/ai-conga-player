import constants as const
import math
import random


class Agent:
    def __init__(self, player_type):
        super().__init__()

        self.player_type = player_type
        self.num_nodes_explored = 0
        self.depth = 2

    def get_directions(self):
        directions = list()
        for i in range(-1, 2):
            for j in range(-1, 2):
                directions.append((i, j))
        directions.remove((0, 0))

        return directions

    def get_child(self, parent, direction):
        return ((parent[0] + direction[0]), (parent[1] + direction[1]))

    # WHITE IS MINIMIZING PLAYER
    def minimizing_player(self, white_squares, black_squares, alpha):
        self.nodes_explored = 0
        min_score = math.inf
        nodes = 0   
        # GET MOVES PLAYED BY WHITE
        for square in black_squares:
            for direction in self.get_directions():
                nodes += 1
                temp_squares = set(black_squares)
                first = self.get_child(square, direction)

                # GET CURRENT MOVE
                if self.is_valid_move(first, white_squares):
                    temp_squares.add(first)

                    second = self.get_child(first, direction)
                    if self.is_valid_move(second, white_squares):
                        temp_squares.add(second)

                        third = self.get_child(second, direction)
                        if self.is_valid_move(third, white_squares):
                            temp_squares.add(third)
                    # CHECK IT'S GOODNESS
                    evaluation = self.utility_function(
                        white_squares, temp_squares)

                    self.nodes_explored += nodes

                    # PRUNING
                    if evaluation < alpha:
                        return evaluation
                    
                    # UPDATING MIN SCORE
                    min_score = min(evaluation, min_score)

        self.nodes_explored += nodes
        return min_score

    # USED TO EVALUATED THE GOODNESS OF A MOVE
    def utility_function(self, max_squares, min_squares):
        squares_score = 0
        moves_score = 0

        for square in max_squares:
            squares_score += 10
            for direction in self.get_directions():
                first = self.get_child(square, direction)
                if self.is_valid_move(first, min_squares):
                    moves_score += 1

        for square in min_squares:
            squares_score -= 10
            for direction in self.get_directions():
                first = self.get_child(square, direction)
                if self.is_valid_move(first, max_squares):
                    moves_score -= 1

        return squares_score

   # UPDATE THE BOARD BASED ON THE STEPS
    def update_board(self, board, src, dest, given_stones, player_squares):
        stones = min(given_stones, board.stones[src[0]][src[1]])
        if stones > 0:
            # NEWLY OCCUPIED SQUARE - SET PLAYER TYPE
            if not board.player[dest[0]][dest[1]] == self.player_type:
                board.player[dest[0]][dest[1]] = self.player_type

            # ADD STONES TO DEST, REMOVE STONES FROM SRC
            board.stones[dest[0]][dest[1]] += stones
            board.stones[src[0]][src[1]] -= stones
            player_squares.add(dest)
            if board.stones[src[0]][src[1]] <= 0:
                board.stones[src[0]][src[1]] = 0
                board.player[src[0]][src[1]] = const.NULL
                if src in player_squares:
                    player_squares.remove(src)

            print('Move: Board updated by moving ' + str(stones) +
                  ' stones from ' + str(src) + ' to ' + str(dest))

    # CONTRAINTS FOR BOARD
    def is_inside_board(self, dest):
        if (dest[1] >= 1) and (dest[1] <= const.ROWS) and (dest[0] >= 1) and (dest[0] <= const.COLS):
            return True
        return False

    # VALID MOVE : IS INSIDE THE BOARD AND DOES NOT BELONG TO OPPONENT
    def is_valid_move(self, dest, occupied_squares):
        return self.is_inside_board(dest) and dest not in occupied_squares
    
    # USER PLAYS THE MOVE ONCE THEY DECIDE WHAT TO DO
    def play_minmax_move(self, board, move, max_player_squares):
        if len(move) != 0:
            current_square = move[0]
            col_idx = current_square[0]
            row_idx = current_square[1]

            num = board.stones[col_idx][row_idx]
            num_steps = len(move) - 1

            if num_steps == 3:
                self.update_board(
                    board, current_square, move[1], 1, max_player_squares)
                self.update_board(
                    board, current_square, move[2], 2, max_player_squares)
                self.update_board(
                    board, current_square, move[3], num - 3, max_player_squares)
                return True

            elif num_steps == 2:
                self.update_board(
                    board, current_square, move[1], 1, max_player_squares)
                self.update_board(
                    board, current_square, move[2], num - 1, max_player_squares)
                return True

            elif num_steps == 1:
                self.update_board(
                    board, current_square, move[1], num, max_player_squares)
                return True

            print("No move possible WHITE LOST")
        return False

    # BASED ON THE AGENT, IMPLEMENT THE THINKING BEHIND THE MOVE
    def find_move(self, board, white_squares, black_squares):
        directions = self.get_directions()

        if self.player_type == const.RANDOM:
            print('Random Agent: WHITE playing')
            # UNORDERED DATA STRUCTION, white_squares IS A SET
            # DIRECTIONS IS A LIST, SHUFFLED BY RANDOM AGENT BEFORE SELECTION
            random.shuffle(directions)
            for square in white_squares:
                for direction in directions:
                    col_idx = square[0]
                    row_idx = square[1]
                    num = board.stones[col_idx][row_idx]

                    first = self.get_child(square, direction)
                    if self.is_valid_move(first, black_squares):

                        second = self.get_child(first, direction)
                        if not self.is_valid_move(second, black_squares):
                            self.update_board(
                                board, square, first, num, white_squares)
                            board.move_found = True
                            return board
                        else:
                            third = self.get_child(second, direction)
                            if not self.is_valid_move(third, black_squares):
                                self.update_board(
                                    board, square, first, 1, white_squares)
                                self.update_board(
                                    board, square, second, num - 1, white_squares)
                                board.move_found = True
                                return board
                            else:
                                self.update_board(
                                    board, square, first, 1, white_squares)
                                self.update_board(
                                    board, square, second, 2, white_squares)
                                self.update_board(
                                    board, square, third, num - 3, white_squares)
                                board.move_found = True
                                return board
            print('No possible move WHITE lost')
            board.move_found = False
            return board
        else:
            print('MINMAX Agent: BLACK playing')
            # SETTING THE CURRENT DEPTH OF FIRST ITERATION AS MAX_DEPTH
            current_depth = self.depth
            alpha = -math.inf
            beta = math.inf
            while (current_depth > 0):
                current_depth -= 1
                best_move = list()
                max_score = -math.inf

                for square in black_squares:
                    for direction in directions:
                        first = self.get_child(square, direction)
                        # KEEPING TRACK OF STEPS ALONG WITH SQUARES OCCUPIED BY SELECTING STEP
                        temp_squares = set(black_squares)
                        temp_move = list()

                        if self.is_valid_move(first, white_squares):
                            temp_squares.add(first)

                            temp_move.append(square)
                            temp_move.append(first)

                            second = self.get_child(first, direction)
                            if self.is_valid_move(second, white_squares):
                                temp_squares.add(second)
                                temp_move.append(second)

                                third = self.get_child(second, direction)
                                if self.is_valid_move(third, white_squares):
                                    temp_squares.add(third)
                                    temp_move.append(third)

                            # FINDING EVALUATION OF MINIMIZING PLAYER
                            evaluation = self.minimizing_player(
                                temp_squares, white_squares, max_score)

                            if evaluation > max_score:
                                best_move = temp_move
                                max_score = evaluation

                            # ALPHA BETA PRUNING
                            # UPDATING ALPHA
                            alpha = max(alpha, max_score)

                            # BREAKING FROM LOOP IS MAX VALUE FOUND
                            if beta <= alpha:
                                break
                            
                            current_depth-=1

            success = self.play_minmax_move(board, best_move, black_squares)

            if success:
                print(str(self.nodes_explored*2) + ' node/s were explored to find the best move')
                print('The depth of the search tree traversed is ' + str(self.depth))
                board.move_found = True
                return board
            else:
                board.move_found = False
                return board
            
