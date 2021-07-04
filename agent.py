import constants as const
import math
import random


class Agent:
    def __init__(self, player_type):
        super().__init__()

        self.player_type = player_type
        self.num_nodes_explored = 0
        self.depth = 4

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
    def minimizing_player(self, white_squares, black_squares, current_best):
        best_eval = math.inf

        directions = self.get_directions()
        for square in black_squares:
            for direction in directions:
                first = self.get_child(square, direction)

                if self.is_valid_move(first, white_squares):
                    potential_stones = set(black_squares)
                    potential_stones.add(first)

                    second = self.get_child(first, direction)
                    if self.is_valid_move(second, white_squares):
                        potential_stones.add(second)

                        third = self.get_child(second, direction)
                        if self.is_valid_move(third, white_squares):
                            potential_stones.add(third)

                    evaluation = self.utility_function(
                        white_squares, potential_stones)

                    if evaluation < current_best:
                        return evaluation

                    if evaluation < best_eval:
                        best_eval = evaluation

        return best_eval

    def utility_function(self, max_squares, min_squares):
        squares_score = 0
        moves_score = 0

        possible_moves = list()
        for i in range(-1, 2):
            for j in range(-1, 2):
                possible_moves.append((i, j))
        possible_moves.remove((0, 0))

        for square in max_squares:
            squares_score += 10
            for move in possible_moves:
                first = self.get_child(square, move)
                if self.is_valid_move(first, min_squares):
                    moves_score += 1

        for square in min_squares:
            squares_score -= 10
            for move in possible_moves:
                first = self.get_child(square, move)
                if self.is_valid_move(first, max_squares):
                    moves_score -= 1

        return squares_score

    # moving stones on the board
    def update_board(self, board, src, dest, given_stones, player_squares):
        total_stones = board.stones[src[0]][src[1]]
        if given_stones > total_stones:
            stones = total_stones
        else:
            stones = given_stones
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

    def make_move(self, board, white_locations, black_locations):
        possible_moves = list()
        for i in range(-1, 2):
            for j in range(-1, 2):
                possible_moves.append((i, j))
        possible_moves.remove((0, 0))

        if self.player_type == const.RANDOM:
            print('Random Agent: WHITE playing')
            random_stones = random.sample(
                white_locations, len(white_locations))
            for col, row in random_stones:
                random.shuffle(possible_moves)
                for move in possible_moves:
                    first = (col + move[0], row + move[1])
                    num = board.stones[col][row]

                    if self.is_inside_board(first) \
                            and first not in black_locations:
                        second = (first[0] + move[0], first[1] + move[1])

                        if second in black_locations or not self.is_inside_board(second):
                            self.update_board(
                                board, (col, row), first, num, white_locations)
                            board.move_found = True
                            return board
                        else:
                            third = (second[0] + move[0], second[1] + move[1])

                            if third in black_locations or not self.is_inside_board(third):
                                self.update_board(
                                    board, (col, row), first, 1, white_locations)
                                self.update_board(
                                    board, (col, row), second, num - 1, white_locations)
                                board.move_found = True
                                return board
                            else:
                                self.update_board(
                                    board, (col, row), first, 1, white_locations)
                                self.update_board(
                                    board, (col, row), second, 2, white_locations)
                                self.update_board(
                                    board, (col, row), third, num - 3, white_locations)
                                board.move_found = True
                                return board
            print('No possible move WHITE lost')
            board.move_found = False
            return board
        else:
            best_move = []
            best_eval = -math.inf

            for col, row in black_locations:
                for move in possible_moves:
                    first = col + move[0], row + move[1]
                    complete_move = []

                    if self.is_inside_board(first) and first not in white_locations:
                        potential_stones = set(black_locations)
                        potential_stones.add(first)

                        complete_move.append((col, row))
                        complete_move.append(first)

                        second = (first[0] + move[0], first[1] + move[1])
                        if second not in white_locations and self.is_inside_board(second):
                            potential_stones.add(second)
                            complete_move.append(second)

                            third = (second[0] + move[0], second[1] + move[1])
                            if third not in white_locations and self.is_inside_board(third):
                                potential_stones.add(third)
                                complete_move.append(third)

                        evaluation = self.minimizing_player(
                            potential_stones, white_locations, best_eval)

                        if evaluation >= best_eval:
                            best_move = complete_move
                            best_eval = evaluation

            if len(best_move) == 0:
                print('No possible move: BLACK lost')
                board.move_found = False
                return board
            else:
                num = board.stones[col][row]
                if len(best_move) == 2:
                    self.update_board(
                        board, best_move[0], best_move[1], num, black_locations)
                    board.move_found = True
                    return board
                elif len(best_move) == 3:
                    self.update_board(
                        board, best_move[0], best_move[1], 1, black_locations)
                    self.update_board(
                        board, best_move[0], best_move[2], num - 1, black_locations)
                    board.move_found = True
                    return board
                elif len(best_move) == 4:
                    self.update_board(
                        board, best_move[0], best_move[1], 1, black_locations)
                    self.update_board(
                        board, best_move[0], best_move[2], 2, black_locations)
                    self.update_board(
                        board, best_move[0], best_move[3], num - 3, black_locations)
                    board.move_found = True
                    return board

            print("No move possible WHITE LOST")
