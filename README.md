# Problem 2: Game of Conga

## Directory Layout

* main.py - executes the program
* board.py - creates an instance of conga board for the game
* agent.py - create random and computer agent players
* constants.py - common file for constants used in the application
* Makefile

## Running the program

Use the Makefile provided in the directory to run the program.

Commands permitted by the Makefile:

1. `make fast_play` - Plays a game with random and computer agent until one of them wins. No user input required throughput the game
2. `make slow_play` - Displays one move at a time, asks the user to press 'y' if they want to see the next move and 'x' to exit the game
3. `make clean`

## Understanding Output

### Players

The first few lines of the output introduce you to the player.

* WHITE is the RANDOM AGENT
* BLACK is the MINMAX AGENT

### Board Display

The row and column numbers are assigned represented in the question. Each square contains the number of stones in that location. BLACK occupied squares are in RED and WHITE occupied squares are in GREEN.

### Following player moves

The terminal also outputs whose turn it is to play followed by the steps they took as part of their move and displays the above board.

In the case of a BLACK/ computer agent, the number of nodes explored and the depth of the search tree traversed as part of selecting that the best move is also printed to the console.

### **Terminal State**

When one of the players runs out of moves to play, the program recognizes this by printing to the console the name of the player along with the board state at the point where the losing player is trapped
