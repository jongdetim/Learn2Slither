from constants import LastHappening

# -----------------------------------------------------------------------
# Objects with `reset`, `step(action)`, and optionally `render` methods.
# -----------------------------------------------------------------------


# recursively converts a nested list to a nested tuple
def convert_to_tuple(obj):
    if isinstance(obj, list):
        return tuple(convert_to_tuple(i) for i in obj)
    return obj


# wrapper for our SnakeGame class
class SnakeEnvironment:
    # all moves always available. possible improvement is to limit
    # available moves to avoid going back or even to avoid hitting the wall
    possible_actions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def __init__(self, snake_game):
        self.game = snake_game

    def reset(self):
        self.game.reset()
        return self.get_game_data()

    def step(self, action):
        self.game.step(action)
        return self.get_game_data()

    def get_game_data(self): # converts vision to tuple and returns vision/state, reward, possible actions, done
        reward, rich_vision, raw_vision, done = self.interpret(*self.game.get_data())
        simple_vision = self.get_simple_vision(rich_vision)
        # print(simple_vision)
        # self.print_snake_vision(self.game.grid_size, self.game.snake[0], raw_vision)
        # return convert_to_tuple(rich_vision) if not done else "terminal", reward, self.possible_actions, done
        return simple_vision if not done else "terminal", reward, self.possible_actions, done

    def get_simple_vision(self, rich_vision):
        '''
        Converts rich_vision to simple_vision.
        rich_vision: list of lists of distances to nearest green, red, and wall/snake (length 12)
        simple_vision: tuple of nearest object type in each direction (length 4)
        '''
        simple_vision = []
        nearest_objects = [min((value, type) for type, value
                           in enumerate(direction) if value is not None)
                           for direction in rich_vision]
        # 0: green, 1: red, 2: wall/snake
        moves = "GRS"
        for direction in nearest_objects:
            simple_vision.append("C" if direction[0] == 1 and moves[direction[1]] == "S" else moves[direction[1]])
        
        simple_vision = tuple(simple_vision)
        # print(rich_vision)
        # print(simple_vision)
        return simple_vision

    # def render(self):
    #     self.game.render()  # Optional for visualization

    # vision is encoded as distance to nearest green [G], distance to nearest
    # red [R], distance to nearest wall or body [S] * [left, up, right, down]
    def interpret(self, grid_size, last_happening, snake, green_apples,
                  red_apple, done) -> tuple[int, list, list]:
        '''Interprets the SnakeGame state and last happening and returns the reward
        and snake vision, and the unprocessed vision for printing.'''
        if done:
            return LastHappening.reward(last_happening), [], [], done
        head = snake[0]
        rich_vision = []
        raw_vision = []
        for direction in [
                (-1, 0), (0, -1), (1, 0), (0, 1)]:  # left, up, right, down
            raw_one_directional_vision = []  # for printing stdout printing
            rich_one_directional_vision = [None, None, None]  # green, red, wall/snake
            cursor = list(head)
            cursor[0] += direction[0]
            cursor[1] += direction[1]
            distance = 1
            while 0 <= cursor[0] < grid_size and 0 <= cursor[1] < grid_size:
                if tuple(cursor) in snake:
                    raw_one_directional_vision.append('S')
                    if rich_one_directional_vision[2] is None:
                        rich_one_directional_vision[2] = distance
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

                cursor[0] += direction[0]
                cursor[1] += direction[1]
                distance += 1

            raw_one_directional_vision.append('W')
            if rich_one_directional_vision[2] is None:
                rich_one_directional_vision[2] = distance

            raw_vision.append(raw_one_directional_vision)
            rich_vision.append(rich_one_directional_vision)

        return LastHappening.reward(last_happening), rich_vision, raw_vision, done

    def print_snake_vision(grid_size, head, raw_vision) -> None:
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
