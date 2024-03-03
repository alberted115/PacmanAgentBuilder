from PacmanAgentBuilder.agents.Iagent import IAgent
from Pacman_Complete.run import GameController


class GameStats(object):
    def __init__(self, game: GameController, agent: IAgent):
        self.actionsTaken = agent.actionsTaken
        self.score = game.score
        self.levelsCompleted = game.level
        self.totalPelletsEaten = game.level * 240 + agent.pelletsEatenThisLevel

    def __str__(self):
        return (f"GameStats(score={self.score}, "
                f"totalPelletsEaten={self.totalPelletsEaten}, "
                f"actionsTaken={self.actionsTaken}, "
                f"levelsCompleted={self.levelsCompleted})")

    @staticmethod
    def calculatePerformance(gameStats: list['GameStats']):
        baseScores = [game.score for game in gameStats]

        averageBaseScore = sum(baseScores) / len(baseScores)

        return {"averageScore": round(averageBaseScore, 3)}
