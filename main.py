import sys

import agent
import board
import constants


def main():
    print("")
    print('Welcome to Conga Board!')
    print('Setting up your board ...')
    # set of squares where black has stones
    black_locations = set()
    # set of squares where black has stones
    white_locations = set()

    # create board
    conga_board = board.CongaBoard()

    # add initial positions
    black_locations.add((1, 4))
    white_locations.add((4, 1))
    max_moves = 300

    # slow play only runs one move at a time
    # fast play runs the game until a winner is found
    mode = int(sys.argv[1])

    # white is random agent
    random_agent = agent.Agent(constants.WHITE)
    # black is computer
    computer = agent.Agent(constants.BLACK)

    # current number of moves in the game
    moves = 0
    conga_board = random_agent.find_move(conga_board, white_locations, black_locations)
    conga_board.display()
    if conga_board.move_found:
        conga_board = computer.find_move(conga_board, white_locations, black_locations)
        conga_board.display()

    while conga_board.move_found:
        if mode:
            play = input('Press y to continue the game and x to exit: ')
            if play != "y":
                break
        if moves == max_moves:
            moves = 0
            # set of squares where black has stones
            black_locations = set()
            # set of squares where black has stones
            white_locations = set()

            # create board
            conga_board = board.CongaBoard()

            # add initial positions
            black_locations.add((1, 4))
            white_locations.add((4, 1))

            # # white is random agent
            random_agent = agent.Agent(constants.WHITE)
            # black is computer
            computer = agent.Agent(constants.BLACK)

        conga_board = random_agent.find_move(conga_board, white_locations, black_locations)
        conga_board.display()
        if conga_board.move_found:
            conga_board = computer.find_move(conga_board, white_locations, black_locations)
            conga_board.display()
        moves+=1

        print("")

    print("***************************")
    if mode:
        print("Total number of moves played: " + str(moves*2))
    else:
        print("Total number of moves played: " + str(moves))


if __name__ == "__main__":
    main()
