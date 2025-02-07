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
