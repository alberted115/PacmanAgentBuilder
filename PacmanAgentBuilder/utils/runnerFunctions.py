from PacmanAgentBuilder.agents.HumanAgent import HumanAgent
from PacmanAgentBuilder.agents.Iagent import IAgent
from PacmanAgentBuilder.utils.gameStats import GameStats
from Pacman_Complete.run import GameController


def runGameWithHuman(gameSpeed=1, startLives=3) -> int:
    game = GameController(gameSpeed=gameSpeed, startLives=startLives, isHumanPlayer=True)
    agent = HumanAgent(gameController=game)
    game.startGame(agent=agent)
    while True:
        game.update()
        if game.gameOver:
            print("Actions taken:", agent.actionsTaken)
            print("score:", game.score)
            print("levels completed:", game.level)
            return game.score


def runGameWithAgent(agentType: type[IAgent], gameSpeed=3, startLives=3, startLevel: int = 0,
                     ghostsEnabled: bool = True, freightEnabled: bool = True,
                     lockDeltaTime: bool = False) -> GameStats:
    if gameSpeed < 0.1 or 10 < gameSpeed:
        raise ValueError(f"gameSpeed ({gameSpeed}) must be between 0.1 and 10 (inclusive). Otherwise the game breaks.")

    game = GameController(gameSpeed=gameSpeed, startLives=startLives, isHumanPlayer=False,
                          startLevel=startLevel, ghostsEnabled=ghostsEnabled, freightEnabled=freightEnabled,
                          lockDeltaTime=lockDeltaTime)
    agent = agentType(gameController=game)
    game.startGame(agent=agent)
    while True:
        game.update()
        if game.gameOver:
            return GameStats(game, agent)


def calculatePerformanceOverXGames(agentClass: type[IAgent], gameCount: int, gameSpeed=5,
                                   startLevel: int = 0, ghostsEnabled: bool = True, freightEnabled: bool = True,
                                   lockDeltaTime=False,logging=False):
    # print agent name

    gameStats = []
    for i in range(gameCount):
        if logging:
            print(f"Running game {i + 1} of {gameCount}...")

        gameStats.append(runGameWithAgent(agentClass, gameSpeed=gameSpeed, startLives=1, startLevel=startLevel,
                                          ghostsEnabled=ghostsEnabled, freightEnabled=freightEnabled,
                                          lockDeltaTime=lockDeltaTime))

        if logging:
            print(f"Game {i + 1} result: {gameStats[i]}")

    performance = GameStats.calculateCombinedRating(gameStats)

    if logging:
        print(f"Performance over {gameCount} games: {performance}")

    return performance
