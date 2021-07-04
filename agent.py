import constants as const
import math
import random


class Agent:
    def __init__(self, player_type):
        super().__init__()

        self.player_type = player_type
        self.nodes_explored = 0
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

    # WHITE is minimizing player
    def minimizing_player(self, white_squares, black_squares, alpha):
        self.nodes_explored = 0
        min_score = math.inf
        nodes = 0

        for square in black_squares:
            for direction in self.get_directions():
                nodes += 1
                temp_squares = set(black_squares)
                first = self.get_child(square, direction)

                if self.is_valid_move(first, white_squares):
                    temp_squares.add(first)

                    second = self.get_child(first, direction)
                    if self.is_valid_move(second, white_squares):
                        temp_squares.add(second)

                        third = self.get_child(second, direction)
                        if self.is_valid_move(third, white_squares):
                            temp_squares.add(third)

                    evaluation = self.utility_function(
                        white_squares, temp_squares)

                    if evaluation <= alpha:
                        self.nodes_explored = nodes
                        return evaluation

                    min_score = min(min_score, evaluation)
        self.nodes_explored += nodes
        return min_score

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

    # moving stones on the board
    def update_board(self, board, src, dest, given_stones, player_squares):
        stones = min(given_stones, board.stones[src[0]][src[1]])
        if stones > 0:
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

            print('Move: Board updated by moving ' + str(stones) +
                  ' stones from ' + str(src) + ' to ' + str(dest))

    def is_inside_board(self, dest):
        if (dest[1] >= 1) and (dest[1] <= const.ROWS) and (dest[0] >= 1) and (dest[0] <= const.COLS):
            return True
        return False

    def is_valid_move(self, dest, occupied_squares):
        return self.is_inside_board(dest) and dest not in occupied_squares

    def play_move(self, board, move, player_squares):
        if len(move) != 0:
            current_square = move[0]
            col_idx = current_square[0]
            row_idx = current_square[1]
            num = board.stones[col_idx][row_idx]

            if len(move) == 4:
                self.update_board(
                    board, current_square, move[1], 1, player_squares)
                self.update_board(
                    board, current_square, move[2], 2, player_squares)
                self.update_board(
                    board, current_square, move[3], num - 3, player_squares)
                return True
            elif len(move) == 3:
                self.update_board(
                    board, current_square, move[1], 1, player_squares)
                self.update_board(
                    board, current_square, move[2], num - 1, player_squares)
                return True
            elif len(move) == 2:
                self.update_board(
                    board, current_square, move[1], num, player_squares)
                return True
        return False

    def make_move(self, board, white_squares, black_squares):
        directions = self.get_directions()

        if self.player_type == const.RANDOM:
            print('Random Agent: WHITE playing')
            random.shuffle(directions)
            for square in white_squares:
                for direction in directions:
                    move = [square]
                    first = self.get_child(square, direction)
                    if self.is_valid_move(first, black_squares):
                        second = self.get_child(first, direction)
                        if not self.is_valid_move(second, black_squares):
                            move.append(first)
                        else:
                            third = self.get_child(second, direction)
                            if not self.is_valid_move(third, black_squares):
                                move.append(second)
                            else:
                                move.append(third)
                    success = self.play_move(board, move, white_squares)
                    if success:
                        board.move_found = True
                        return board
            print('Trapped by BLACK squares, WHITE lost!')
            board.move_found = False
            return board
        else:
            print('MINMAX Agent: BLACK playing')
            current_depth = self.depth
            while (current_depth > 0):
                current_depth -= 1
                best_move = list()
                max_score = -math.inf
                self.nodes_explored = 0

                for square in black_squares:
                    for direction in directions:
                        first = self.get_child(square, direction)
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

                            evaluation = self.minimizing_player(
                                temp_squares, white_squares, max_score)

                            if evaluation > max_score:
                                best_move = temp_move
                                max_score = evaluation
                                
                            current_depth -=1
                            
            success = self.play_move(board, best_move, black_squares)

            if success:
                print(str(self.nodes_explored*2) + ' node/s were explored to find the best move')
                print('The depth of the search tree traversed is ' + str(self.depth))
                board.move_found = True
                return board
            else:
                board.move_found = False
                return board
            
