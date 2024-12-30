
from constants import LastHappening

# vision is encoded as distance to nearest green [G], distance to nearest
# red [R], distance to nearest wall or body [S] * [left, up, right, down]


def interpret(grid_size, last_happening, snake, green_apples,
              red_apple) -> tuple[int, list, list]:
    '''Interprets the SnakeGame state and last happening and returns the reward
    and snake vision, and the unprocessed vision for printing.'''
    head = snake[0]
    vision = []
    raw_vision = []
    for direction in [
            (-1, 0), (0, -1), (1, 0), (0, 1)]:  # left, up, right, down
        raw_one_directional_vision = []  # for printing stdout printing
        one_directional_vision = [None, None, None]  # green, red, wall/snake
        cursor = list(head)
        cursor[0] += direction[0]
        cursor[1] += direction[1]
        distance = 1
        while 0 <= cursor[0] < grid_size and 0 <= cursor[1] < grid_size:
            if tuple(cursor) in snake:
                raw_one_directional_vision.append('S')
                if one_directional_vision[2] is None:
                    one_directional_vision[2] = distance
            elif tuple(cursor) == red_apple:
                raw_one_directional_vision.append('R')
                if one_directional_vision[1] is None:
                    one_directional_vision[1] = distance
            elif tuple(cursor) in green_apples:
                raw_one_directional_vision.append('G')
                if one_directional_vision[0] is None:
                    one_directional_vision[0] = distance
            else:
                raw_one_directional_vision.append('0')

            cursor[0] += direction[0]
            cursor[1] += direction[1]
            distance += 1

        raw_one_directional_vision.append('W')
        if one_directional_vision[2] is None:
            one_directional_vision[2] = distance

        raw_vision.append(raw_one_directional_vision)
        vision.append(one_directional_vision)

    return LastHappening.reward(last_happening), vision, raw_vision


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
