import constants as const
import math
import random


# col first, row second
# col [0], row [1]
# TODO: switch and check
class Agent:
    def __init__(self, player_type):
        super().__init__()

        self.player_type = player_type
        self.num_nodes_explored = 0
        self.depth = 0

    def get_min_eval(self, player_stones, opponent_stones, current_best):
        best_eval = math.inf

        possible_moves = list()
        for i in range(-1, 2):
            for j in range(-1, 2):
                possible_moves.append((i, j))
        possible_moves.remove((0, 0))

        for col, row in opponent_stones:
            for move in possible_moves:
                new_pos = (col + move[0], row + move[1])

                if self.is_valid_move(new_pos) and new_pos not in player_stones:
                    potential_stones = set(opponent_stones)
                    potential_stones.add(new_pos)

                    second_pos = (new_pos[0] + move[0], new_pos[1] + move[1])
                    if second_pos not in player_stones and self.is_valid_move(second_pos):
                        potential_stones.add(second_pos)
                        third_pos = (second_pos[0] + move[0], second_pos[1] + move[0])
                        if third_pos not in player_stones and self.is_valid_move(third_pos):
                            potential_stones.add(third_pos)

                    evaluation = self.eval_func(player_stones, potential_stones)
                    if evaluation < current_best:
                        return evaluation
                    if evaluation < best_eval:
                        best_eval = evaluation

        return best_eval

    def eval_func(self, player_stones, opponent_stones):
        score = 0
        score += len(player_stones) - len(opponent_stones)
        return score

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

            print('Move: Board updated by moving ' + str(stones) + ' stones from ' + str(src) + ' to ' + str(dest))

    def is_valid_move(self, dest):
        if (dest[1] >= 1) and (dest[1] <= const.ROWS) and (dest[0] >= 1) and (dest[0] <= const.COLS):
            return True
        return False

    # return (board + valid)
    def make_move(self, board, white_locations, black_locations):
        possible_moves = list()
        for i in range(-1, 2):
            for j in range(-1, 2):
                possible_moves.append((i, j))
        possible_moves.remove((0, 0))

        if self.player_type == const.RANDOM:
            print('Random Agent: WHITE playing')
            random_stones = random.sample(white_locations, len(white_locations))
            for col, row in random_stones:
                random.shuffle(possible_moves)
                for move in possible_moves:
                    new_pos = (col + move[0], row + move[1])
                    num = board.stones[col][row]

                    if self.is_valid_move(new_pos):
                        if new_pos not in black_locations:
                            second_pos = (new_pos[0] + move[0], new_pos[1] + move[1])

                            if second_pos in black_locations or not self.is_valid_move(second_pos):
                                self.update_board(board, (col, row), new_pos, num, white_locations)
                                board.is_valid_move = True
                                return board
                            else:
                                third_pos = (second_pos[0] + move[0], second_pos[1] + move[1])

                                if third_pos in black_locations or not self.is_valid_move(third_pos):
                                    self.update_board(board, (col, row), new_pos, 1, white_locations)
                                    self.update_board(board, (col, row), second_pos, num - 1, white_locations)
                                    board.is_valid_move = True
                                    return board
                                else:
                                    self.update_board(board, (col, row), new_pos, 1, white_locations)
                                    self.update_board(board, (col, row), second_pos, 2, white_locations)
                                    self.update_board(board, (col, row), third_pos, num - 3, white_locations)
                                    board.is_valid_move = True
                                    return board
            print('No possible move WHITE lost')
            board.is_valid_move = False
            return board
        else:
            best_move = []
            best_eval = -math.inf

            for col, row in black_locations:
                for move in possible_moves:
                    new_pos = col + move[0], row + move[1]
                    complete_move = []

                    if self.is_valid_move(new_pos) and new_pos not in white_locations:
                        potential_stones = set(black_locations)
                        potential_stones.add(new_pos)

                        complete_move.append((col, row))
                        complete_move.append(new_pos)

                        second_pos = (new_pos[0] + move[0], new_pos[1] + move[1])
                        if second_pos not in white_locations and self.is_valid_move(second_pos):
                            potential_stones.add(second_pos)
                            complete_move.append(second_pos)

                            third_pos = (second_pos[0] + move[0], second_pos[1] + move[1])
                            if third_pos not in white_locations and self.is_valid_move(third_pos):
                                potential_stones.add(third_pos)
                                complete_move.append(third_pos)

                        evaluation = self.get_min_eval(potential_stones, white_locations, best_eval)

                        if evaluation >= best_eval:
                            best_move = complete_move
                            best_eval = evaluation

            if len(best_move) == 0:
                print('No possible move: BLACK lost')
                board.is_valid_move = False
                return board
            else:
                num = board.stones[col][row]
                if len(best_move) == 2:
                    self.update_board(board, best_move[0], best_move[1], num, black_locations)
                    board.is_valid_move = True
                    return board
                elif len(best_move) == 3:
                    self.update_board(board, best_move[0], best_move[1], 1, black_locations)
                    self.update_board(board, best_move[0], best_move[2], num - 1, black_locations)
                    board.is_valid_move = True
                    return board
                elif len(best_move) == 4:
                    self.update_board(board, best_move[0], best_move[1], 1, black_locations)
                    self.update_board(board, best_move[0], best_move[2], 2, black_locations)
                    self.update_board(board, best_move[0], best_move[3], num - 3, black_locations)
                    board.is_valid_move = True
                    return board

            print("No move possible WHITE LOST")
