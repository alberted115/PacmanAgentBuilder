from PacmanAgentBuilder.agents.AlbertAgent import AlbertAgent
from PacmanAgentBuilder.agents.MachineLearningAgent import MachineLearningAgent
from PacmanAgentBuilder.utils.runnerFunctions import *


stats = calculatePerformanceOverXGames(
    agentClass=MachineLearningAgent,  # Specify the agent to be evaluated.
    gameCount=100000,  # Number of games the agent will play.
    gameSpeed=1,  # Sets the speed of the game from 0.1 (slow) to 5 (fast). For a higher speed, enable lockDeltaTime.
    startLevel=0,  # Choose the starting level for the agent (0 for level one, 1 for level two, and so on).
    ghostsEnabled=True,  # Toggle ghosts on or off.
    freightEnabled=True,  # Toggle if the effect of power pellets should be ignored.
    lockDeltaTime=True,  # When enabled, the game will run at the highest possible speed.
    logging=True  # Toggle the logging of game-related information to the console while the agent is playing.
)
