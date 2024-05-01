from PacmanAgentBuilder.agents.Iagent import IAgent
from PacmanAgentBuilder.utils.gameStats import GameStats
from Pacman_Complete.run import GameController


def runGameWithAgent(agentType: type[IAgent], gameSpeed=3, startLives=5, startLevel: int = 0,
                     ghostsEnabled: bool = True, freightEnabled: bool = True, lockDeltaTime: bool = False) -> GameStats:
    """
        Runs a single game with the specified agent.

        :param agentType: Specify the agent to be evaluated.
        :param gameSpeed: Sets the speed of the game from 0.1 (slow) to 5 (fast). Note: For a higher speed, enable lockDeltaTime.
        :param startLives: The number of lives the agent starts with.
        :param startLevel: Choose the starting level for the agent (0 for level one, 1 for level two, and so on).
        :param ghostsEnabled: Toggle ghosts on or off.
        :param freightEnabled: Toggle if the effect of power pellets should be ignored (ghosts turning blue and stops chasing).
        :param lockDeltaTime: When enabled, the game will run at the highest possible speed regardless of the gameSpeed setting. This provides a stable test environment as the game speed is bottlenecked by your hardware, and can therefore not go faster than your hardware can handle.
        :return: GameStats object containing the statistics of the game.
    """

    if gameSpeed < 0.1 or 5 < gameSpeed:
        raise ValueError(f"gameSpeed ({gameSpeed}) must be between 0.1 and 10 (inclusive). Otherwise the game breaks.")

    game = GameController(
        gameSpeed=gameSpeed,
        startLives=startLives,
        startLevel=startLevel,
        ghostsEnabled=ghostsEnabled,
        freightEnabled=freightEnabled,
        lockDeltaTime=lockDeltaTime
    )
    agent = agentType(gameController=game)

    game.startGame(agent=agent)
    while True:
        game.update()
        if game.gameOver:
            return GameStats(game, agent)


def calculatePerformanceOverXGames(agentClass: type[IAgent], gameCount: int, gameSpeed=5,
                                   startLevel: int = 0, ghostsEnabled: bool = True, freightEnabled: bool = True,
                                   lockDeltaTime=False, logging=False):
    """
        Calculates the performance of the specified agent over a number of games.

        :param agentClass: Specify the agent to be evaluated.
        :param gameCount: Number of games the agent will play.
        :param gameSpeed: Sets the speed of the game from 0.1 (slow) to 5 (fast). Note: For a higher speed, enable lockDeltaTime.
        :param startLevel: Choose the starting level for the agent (0 for level one, 1 for level two, and so on).
        :param ghostsEnabled: Toggle ghosts on or off.
        :param freightEnabled: Toggle if the effect of power pellets should be ignored (ghosts turning blue and stops chasing).
        :param lockDeltaTime: When enabled, the game will run at the highest possible speed regardless of the gameSpeed setting. This provides a stable test environment as the game speed is bottlenecked by your hardware, and can therefore not go faster than your hardware can handle.
        :param logging: Toggle the logging of game-related information to the console while the agent is playing.
        :return: Performance object containing the performance of the agent over the specified number of games.
        """

    if logging:
        print(f"\nAgent: {agentClass.__name__}\n")

    gameStats = []
    for i in range(gameCount):
        if logging:
            print(f"Running game {i + 1} of {gameCount}...")

        gameStats.append(runGameWithAgent(agentClass, gameSpeed=gameSpeed, startLives=5, startLevel=startLevel,
                                          ghostsEnabled=ghostsEnabled, freightEnabled=freightEnabled,
                                          lockDeltaTime=lockDeltaTime))

        if logging:
            print(f"Game {i + 1} result: {gameStats[i]}")

    performance = GameStats.calculatePerformance(gameStats)

    if logging:
        print(f"Performance over {gameCount} games: {performance}")

    return performance
