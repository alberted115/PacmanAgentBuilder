from Pacman_Complete.constants import *
from Pacman_Complete.vector import Vector2


def roundVector(vector: Vector2) -> Vector2:
    return Vector2(round(vector.x), round(vector.y))


def manhattanDistance(a: Vector2, b: Vector2) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)


def distanceSquared(a: Vector2, b: Vector2) -> int:
    return (a.x - b.x) ** 2 + (a.y - b.y) ** 2


def getOppositeDirection(direction: int) -> int:
    return direction * -1


def directionToString(direction: int):
    if direction == UP:
        return "UP"
    if direction == DOWN:
        return "DOWN"
    if direction == LEFT:
        return "LEFT"
    if direction == RIGHT:
        return "RIGHT"

    raise Exception(f"Direction '{direction}' not recognized")


def isPortalPath(startVector: Vector2, endVector: Vector2) -> bool:
    # real distance is TILESIZE * 26, but I use 24 to be safe
    portalDistance = TILESIZE * 24
    return abs(startVector.x - endVector.x) > portalDistance and startVector.y == endVector.y