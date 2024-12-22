
from constants import LastHappening

# zet dit als enum class in constants als Rewards
REWARDS = [None] * 5
REWARDS[LastHappening.NONE] = 0
REWARDS[LastHappening.NO_COLLISION] = -1
REWARDS[LastHappening.GREEN_APPLE_EATEN] = 10
REWARDS[LastHappening.RED_APPLE_EATEN] = -10
REWARDS[LastHappening.DIED] = -1000

# vision is encoded as distance to nearest green, distance to nearest red, distance to nearest wall or body * [left, up, right, down]

def interpret(grid_size, last_happening, snake, green_apples, red_apple) -> tuple[int, list, list]:
    '''Interprets the SnakeGame state and last happening and returns the reward and snake vision'''
    head = snake[0]
    vision = []
    raw_vision = []
    for direction in [(-1, 0), (0, -1), (1, 0), (0, 1)]: #left, up, right, down
        raw_one_directional_vision = [] # used for printing according to subject
        one_directional_vision = [None, None, None] # green, red, wall/snake
        current = list(head)
        current[0] += direction[0]
        current[1] += direction[1]
        distance = 1
        while 0 <= current[0] < grid_size and 0 <= current[1] < grid_size:
            print(current)
            if tuple(current) in snake:
                raw_one_directional_vision.append('S')
                if one_directional_vision[2] == None:
                    one_directional_vision[2] = distance
            elif tuple(current) in red_apple:
                raw_one_directional_vision.append('R')
                if one_directional_vision[1] == None:
                    one_directional_vision[1] = distance
            elif tuple(current) in green_apples:
                raw_one_directional_vision.append('G')
                if one_directional_vision[0] == None:
                    one_directional_vision[0] = distance
            else:
                raw_one_directional_vision.append('0')

            current[0] += direction[0]
            current[1] += direction[1]
            distance += 1

        else:
            raw_one_directional_vision.append('W')
            if one_directional_vision[2] == None:
                one_directional_vision[2] = distance
        
        raw_vision.append(raw_one_directional_vision)
        vision.append(one_directional_vision)

    return REWARDS[last_happening], vision, raw_vision


print(interpret(10, LastHappening.NONE, [(4,4),(4,5)], [(2,2), (4,2)], (4,8)))
