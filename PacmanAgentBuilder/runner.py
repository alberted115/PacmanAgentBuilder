from PacmanAgentBuilder.agents.MyFirstAgent import MyFirstAgent
from PacmanAgentBuilder.utils.runnerFunctions import *

# runGameWithHuman()
stats = calculatePerformanceOverXGames(MyFirstAgent, gameCount=10, gameSpeed=1, startLevel=0,
                                       ghostsEnabled=True, freightEnabled=True, logging=True)
