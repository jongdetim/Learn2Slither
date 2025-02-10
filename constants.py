from enum import Enum


class LastHappening(Enum):
    NONE = 0
    NO_COLLISION = 1
    GREEN_APPLE_EATEN = 2
    RED_APPLE_EATEN = 3
    DIED = 4

    def reward(self):
        rewards = {
            LastHappening.NONE: 0,
            LastHappening.NO_COLLISION: -1,
            LastHappening.GREEN_APPLE_EATEN: 20,
            LastHappening.RED_APPLE_EATEN: -20,
            LastHappening.DIED: -1000,
        }
        return rewards[self]

class Directions(Enum):
    LEFT = (-1, 0)
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)

    @classmethod
    def from_tuple(cls, direction_tuple):
        for direction in cls:
            if direction.value == direction_tuple:
                return direction.name
        raise ValueError(f"Invalid direction tuple: {direction_tuple}")

# Example usage
# print(Direction.from_tuple((1, 0)))  # Output: RIGHT
# print(Direction.from_tuple((-1, 0)))  # Output: LEFT
# print(Direction.from_tuple((0, 1)))  # Output: DOWN
# print(Direction.from_tuple((0, -1)))  # Output: UP
