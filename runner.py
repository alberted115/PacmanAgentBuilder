from PacmanAgentBuilder.agents.MyFirstAgent import MyFirstAgent
from PacmanAgentBuilder.utils.runnerFunctions import *

# runGameWithHuman()
stats = calculatePerformanceOverXGames(agentClass=MyFirstAgent, gameCount=10, gameSpeed=1, startLevel=0,
                                       ghostsEnabled=True, freightEnabled=True,
                                       lockDeltaTime=True, logging=True)
