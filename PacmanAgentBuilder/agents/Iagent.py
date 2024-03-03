from abc import abstractmethod, ABC

from PacmanAgentBuilder.utils.observation import Observation


class IAgent(ABC):
    """
    THis is the interface for the agent. All agents must implement this interface.
    """
    @abstractmethod
    def __init__(self, gameController):
        self.gameController = gameController
        self.actionsTaken = 0
        self.pelletsEatenThisLevel = 0


    @abstractmethod
    def calculateNextMove(self):
        raise Exception("NotImplementedException")

    def takeStats(self, obs: Observation):
        self.actionsTaken += 1
        self.pelletsEatenThisLevel = obs.pelletGroup.numEaten
        pass

