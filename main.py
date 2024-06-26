import board, agent, constants
import sys
# TODO
# output depth and nodes explored
# completing bonus
# row and col differences
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
    black_locations.add((1,4))
    white_locations.add((4,1))

    # restricted play only runs the game for x moves
    # unrestricted play runs the game until a winner is found
    mode = int(sys.argv[1])

    max_moves = 0
    # get num_moves if executor wants a restricted game
    if not int(mode):
        while not (int(max_moves)>0):
            max_moves = input('Enter the number of moves you want to restrict the game to: ')
            if int(max_moves)<=0:
                print("Try again! Number of moves in an active game are greater than zero\n")
    else:
        max_moves = 100

    # # white is random agent
    random_agent = agent.Agent(constants.WHITE)
    # black is computer
    computer = agent.Agent(constants.BLACK)
    
    # current number of moves in the game
    moves = 0
    conga_board = random_agent.make_move(conga_board, white_locations, black_locations)
    conga_board.display()
    moves += 1
    if conga_board.valid_move:
        conga_board = computer.make_move(conga_board, white_locations, black_locations)
        conga_board.display()
        moves += 1

    # first move set 
    # white makes the first move, followed by black
    #  
    while(conga_board.valid_move):
        # print('here')
        # print(white_locations)
        # if (moves < max_moves) :
        #     # set of squares where black has stones
        #     black_locations = set()
        #     # set of squares where black has stones
        #     white_locations = set()

        #     # create board
        #     conga_board = board.CongaBoard()

        #     # add initial positions
        #     black_locations.add((1,4))
        #     white_locations.add((4,1))

        #     # # white is random agent
        #     random_agent = agent.Agent(constants.WHITE)
        #     # black is computer
        #     computer = agent.Agent(constants.BLACK)

        conga_board = random_agent.make_move(conga_board, white_locations, black_locations)
        # print(white_locations)
        conga_board.display()
        moves += 1
        if conga_board.valid_move:
            # print('here inside')
            conga_board = computer.make_move(conga_board, white_locations, black_locations)
            conga_board.display()
            # TODO: include number of nodes explored and depth explored
            moves += 1
        print("")

        # play = input('Press Y to continue:')
        # if play != 'y' and moves > 100:
        #     break

    print("%%%%%%%%%%%%%%%%%%%%%%%%")
    # TODO: add more output lines
    print("Total number of moves played: " + str(moves))

if __name__ == "__main__":
    main()