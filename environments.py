from constants import LastHappening, Directions

# -----------------------------------------------------------------------
# Objects with `reset`, `step(action)`, and optionally `render` methods.
# -----------------------------------------------------------------------


# recursively converts a nested list to a nested tuple
def convert_nested_list_to_tuple(obj):
    if isinstance(obj, list):
        return tuple(convert_nested_list_to_tuple(i) for i in obj)
    return obj


# wrapper for our SnakeGame class
class SnakeEnvironment:
    # all moves always available. possible improvement is to limit
    # available moves to avoid going back or even to avoid hitting the wall
    possible_actions = list(Directions)

    def __init__(self, snake_game):
        self.game = snake_game

    def reset(self):
        self.game.reset()
        return self.get_game_data()

    def step(self, action):
        # print(action.name)
        self.game.step(action)
        return self.get_game_data()

    def get_game_data(self): # converts vision to tuple and returns vision/state, reward, possible actions, done
        reward, rich_vision, raw_vision, done, snake_length = self.interpret(*self.game.get_data())
        if not done:
            # GRWC_vision = self.get_GRWC_vision(rich_vision)
            # GRNC_vision = self.get_GRNC_vision(rich_vision)
            eleven_state_vision = self.get_depth_vision(rich_vision)
            return eleven_state_vision, reward, self.possible_actions, done, snake_length

        return "terminal", reward, self.possible_actions, done, snake_length

    def get_depth_vision(self, rich_vision):
        '''
        Converts rich_vision to a tuple of 11 states: Green at ANY distance,
        Red at distance 1 and distance > 1,
        Wall at distance 1, 2, 3, 4+, Snake at distance 1, 2, 3, 4+
        '''
        depth_vision = []
        nearest_objects = [min((value, type) for type, value
                           in enumerate(direction) if value is not None)
                           for direction in rich_vision]
        # 0: green, 1: red, 2: wall, 3: snake
        moves = "GRWS"
        for direction in nearest_objects:
            if moves[direction[1]] == "G":
                depth_vision.append("G")
            elif moves[direction[1]] == "R":
                depth_vision.append("R1" if direction[0] == 1 else "R")
            elif moves[direction[1]] == "W":
                if direction[0] == 1:
                    depth_vision.append("W1")
                elif direction[0] == 2:
                    depth_vision.append("W2")
                elif direction[0] == 3:
                    depth_vision.append("W3")
                else:
                    depth_vision.append("W")
            elif moves[direction[1]] == "S":
                if direction[0] == 1:
                    depth_vision.append("S1")
                elif direction[0] == 2:
                    depth_vision.append("S2")
                elif direction[0] == 3:
                    depth_vision.append("S3")
                else:
                    depth_vision.append("S")
        return tuple(depth_vision)

    def get_GRWC_vision(self, rich_vision):
        '''
        Converts rich_vision to simple_vision, which is just S, W, R, G, C (for immediate S/W collision / distance of 1)
        rich_vision: list of lists of distances to nearest green, red, and wall/snake (length 12)
        simple_vision: tuple of nearest object type in each direction (length 4)
        '''
        simple_vision = []
        nearest_objects = [min((value, type) for type, value
                           in enumerate(direction) if value is not None)
                           for direction in rich_vision]
        # 0: green, 1: red, 2: wall, 3: snake
        moves = "GRWS"
        for direction in nearest_objects:
            simple_vision.append("C" if direction[0] == 1 and
                                 (moves[direction[1]] == "W" or moves[direction[1]] == "S")
                                 else moves[direction[1]])

        simple_vision = tuple(simple_vision)
        return simple_vision

    def get_GRNC_vision(self, rich_vision):
        '''
        Green (any distance)
        Red (distance=1)
        Nothing (distance>1 and S/W/R)
        Collision (distance = 1 and S/W)
        '''
        simple_vision = []
        nearest_objects = [min((value, type) for type, value
                           in enumerate(direction) if value is not None)
                           for direction in rich_vision]
        # 0: green, 1: red, 2: wall, 3: snake
        moves = "GRWS"
        for direction in nearest_objects:
            if moves[direction[1]] == "G":
                simple_vision.append("G")
            elif direction[0] == 1 and moves[direction[1]] in "WS":
                simple_vision.append("C")
            elif moves[direction[1]] in "WSR" and direction[0] > 1:
                simple_vision.append("N")
            else:
                simple_vision.append("R")
        simple_vision = tuple(simple_vision)
        return simple_vision

    # def get_GRWC_vision(self, simple_vision):
    #     '''
    #     removes S/W distinction from simple_vision
    #     '''
    #     simplest_vision = ["W" if obj == "S" else obj for obj in simple_vision]

    #     return tuple(simplest_vision)

    # def render(self):
    #     self.game.render()  # Optional for visualization

    # vision is encoded as distance to nearest green [G], distance to nearest
    # red [R], distance to nearest wall or body [S] * [left, up, right, down]
    def interpret(self, grid_size, last_happening, snake, green_apples,
                  red_apple, done):
        '''Interprets the SnakeGame state and last happening and returns the reward
        and snake vision, and the unprocessed vision for printing.'''
        if done:
            return LastHappening.reward(last_happening), [], [], done, len(snake)
        head = snake[0]
        rich_vision = []
        raw_vision = []
        # for direction in [
        #         (-1, 0), (0, -1), (1, 0), (0, 1)]:  # left, up, right, down
        for direction in self.possible_actions:
            raw_one_directional_vision = []  # for printing stdout printing
            rich_one_directional_vision = [None, None, None, None]  # green, red, wall, snake
            # rich_one_directional_vision = [None, None, None, None]  # green, red, wall, snake
            cursor = list(head)
            cursor[0] += direction.value[0]
            cursor[1] += direction.value[1]
            distance = 1
            while 0 <= cursor[0] < grid_size and 0 <= cursor[1] < grid_size:
                if tuple(cursor) in snake:
                    raw_one_directional_vision.append('S')
                    if rich_one_directional_vision[3] is None:
                        rich_one_directional_vision[3] = distance
                elif tuple(cursor) == red_apple.position:
                    raw_one_directional_vision.append('R')
                    if rich_one_directional_vision[1] is None:
                        rich_one_directional_vision[1] = distance
                elif tuple(cursor) in [green_apple.position for green_apple in green_apples]:
                    raw_one_directional_vision.append('G')
                    if rich_one_directional_vision[0] is None:
                        rich_one_directional_vision[0] = distance
                else:
                    raw_one_directional_vision.append('0')

                cursor[0] += direction.value[0]
                cursor[1] += direction.value[1]
                distance += 1

            raw_one_directional_vision.append('W')
            if rich_one_directional_vision[2] is None:
                rich_one_directional_vision[2] = distance

            raw_vision.append(raw_one_directional_vision)
            rich_vision.append(rich_one_directional_vision)

        return LastHappening.reward(last_happening), rich_vision, raw_vision, done, len(snake)

    def print_raw_snake_vision(self, grid_size, head, raw_vision) -> None:
        output = [list(' ' * (grid_size + 2)) for _ in range(grid_size + 2)]
        head = [value + 1 for value in head]
        output[head[1]][head[0]] = 'H'
        for line, direction in zip(raw_vision, [(-1, 0), (0, -1), (1, 0), (0, 1)]):
            cursor = list((head[1] + direction[1], head[0] + direction[0]))
            for char in line:
                output[cursor[0]][cursor[1]] = char
                cursor[0] += direction[1]
                cursor[1] += direction[0]

        for row in output:
            print(''.join(row))


# testing
# reward, vision, raw_vision = interpret(
#     10, LastHappening.DIED, [(2, 2)], [(1, 1)], (4, 4))
# print_snake_vision(10, (2, 2), raw_vision)
# print(reward)
