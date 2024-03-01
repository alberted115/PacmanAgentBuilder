# PacmanAgentBuilder
This is the pacman game from [pacmancode.com](https://pacmancode.com/) with extentions that make agent building easier.


## Getting started
1. Clone the Repository and open it in Rider
2. Create a local python intepreter
3. Install pygame and numpy
4. add a python run configuration to Rider that runs the *pacmanAgentBuilder/runner.py* file, and with the */pacman_complete* folder as the working folder.
5. write you agent code in the */pacmanAgentBuilder/agents/MyFirstAgent*
6. Run the configuration to see your agent play! The agent will play 10 games and the average score will be printed to the console.

> I recommend you periodicly create a new agent class, so you can see previous version of your agent.


## Changing game variables
For better testing you can change the following arguments in the *pacmanAgentBuilder/runner.py* file:
- which agent you want to run
- how many games the agent will play
- how fast the game should run. between 0.1 and 10 (going over 10 breaks the game. If you have a low-end pc, going over 5 might even break the game)
- the start level. Basically which level the agent should start on (0 is the first level, 1 is the second)
- If ghosts should be enabled
- If the power of power-pellets should be ignored
- If the program should log information to the console.

# Classes
## Observation class
This is a class that is used in the agent building.
It contains all the nessesary information that the agent will need to beat the game.


## DebugHelper class
This is a class with static methods that can help with debugging. These methods can be called from anywhere in your agent code. \
**These methods Includes:**
- DebugHelper.pauseGame()
- DebugHelper.drawLine()
- DebugHelper.drawDot()
- DebugHelper.drawMap()


## Utils functions
The Utils file contains a few function that may be helpful when building an agent. \
These include:
- manhattanDistance()
- distanceSquared()
- directionToString()


## GameStats class
This is the class that is returned when you run a game with an agent. It contains information about the game played like score, pellets eaten and actionsTaken (how many times the agent was asked for a move by the game)

the *calculateCombinedRating* method is the fitness method used to determine the performance of an agent over x games. It currently calculates the average score. If you want a more complex fitness function, **feel free to edit the method!**
