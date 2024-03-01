# PacmanAgentBuilder
This is the Pac-Man game from [pacmancode.com](https://pacmancode.com/) with extensions that make agent building easier.

## Getting started
1. Clone the repository and open it in Rider.
2. Create a local Python interpreter.
3. Install `pygame` and `numpy`.
4. Add a Python run configuration to Rider that runs the `pacmanAgentBuilder/runner.py` file, with the `/pacman_complete` folder as the working directory.
5. Write your agent code in the `/pacmanAgentBuilder/agents/MyFirstAgent`.
6. Run the configuration to see your agent play! The agent will play 10 games, and the average score will be printed to the console.

> I recommend you periodically create a new agent class so that you can compare with previous versions of your agent.

## Changing game variables
For better testing, you can change the following arguments in the `pacmanAgentBuilder/runner.py` file:
- Which agent you want to run.
- How many games the agent will play.
- How fast the game should run. Between 0.1 and 10 (going over 10 may cause the game to break. If you have a low-end PC, going over 5 might also cause issues).
- The start level, which determines the level the agent should start on (0 is the first level, 1 is the second).
- If ghosts should be enabled.
- If the power of power pellets should be ignored.
- Whether the program should log information to the console.

## Classes
### Observation class
This is a class that is used in agent building.
It contains all the necessary information that the agent will need to beat the game.

### DebugHelper class
This is a class with static methods that can help with debugging. These methods can be called from anywhere in your agent code. It also has a few colors that can be used when calling the draw methods.
**These methods include:**
- `DebugHelper.pauseGame()`
- `DebugHelper.drawLine()`
- `DebugHelper.drawDot()`
- `DebugHelper.drawMap()`

### Utils functions
The Utils file contains a few functions that may be helpful when building an agent. These include:
- `manhattanDistance()`
- `distanceSquared()`
- `directionToString()`

### GameStats class
This is the class that is returned when you run a game with an agent. It contains information about the game played, such as score, pellets eaten, and actionsTaken (how many times the agent was asked for a move by the game).

The `calculateCombinedRating` method is the fitness function used to determine the performance of an agent over x games. It currently calculates the average score. If you want a more complex fitness function, **feel free to edit the method!**
