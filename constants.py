from enum import Enum, IntEnum

class LastHappening(IntEnum):
    NONE = 0
    NO_COLLISION = 1
    GREEN_APPLE_EATEN = 2
    RED_APPLE_EATEN = 3
    DIED = 4

class Rewards(Enum):
    NONE = 0
    NO_COLLISION = -1
    GREEN_APPLE_EATEN = 10
    RED_APPLE_EATEN = -10
    DIED = -1000
