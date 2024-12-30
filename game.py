import pygame as pg
import random
import sys
from time import sleep

from constants import LastHappening


class Apple:
    def __init__(self, type):
        self.type = type
        self.position = (0, 0)

    def relocate(self, grid_size, occupied_positions):
        if len(occupied_positions) >= grid_size ** 2:
            print(len(occupied_positions), occupied_positions)
            input("NO SPACE FOR APPLES!!!")
        while len(occupied_positions) < grid_size ** 2:
            self.position = (random.randint(0, grid_size - 1),
                             random.randint(0, grid_size - 1))
            if self.position not in occupied_positions:
                break


class Snake:
    def __init__(self, grid_size, random_start=True):
        self.grid_size = grid_size
        self.reset(grid_size, random_start)

    def reset(self, grid_size, random_start=True):
        center = grid_size // 2
        self.input_buffer = []  # Input buffer for directional input
        if random_start:
            self.body = self._generate_random_snake()
            self.direction = self._initial_direction()
        else:
            self.body = [(2, center), (1, center), (0, center)]
            self.direction = (1, 0)  # Initially moving right

    def _generate_random_snake(self):
        """
        Generate a random contiguous starting position for snake of length 3.
        """
        # Randomly choose an initial direction
        possible_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        initial_direction = random.choice(possible_directions)

        min_x, max_x = 0, self.grid_size - 1
        min_y, max_y = 0, self.grid_size - 1
        if initial_direction == (1, 0):  # Right
            min_x = 2
            max_x = self.grid_size - 1
        elif initial_direction == (-1, 0):  # Left
            min_x = 0
            max_x = self.grid_size - 3
        elif initial_direction == (0, 1):  # Down
            min_y = 2
            max_y = self.grid_size - 1
        else:  # Up
            min_y = 0
            max_y = self.grid_size - 3

        start_x = random.randint(min_x, max_x)
        start_y = random.randint(min_y, max_y)

        # Generate contiguous body segments
        body = [
            (start_x, start_y),
            (start_x - initial_direction[0], start_y - initial_direction[1]),
            (start_x - 2 * initial_direction[0], start_y - 2 *
             initial_direction[1]),
        ]
        return body

    def _initial_direction(self):
        """
        Determine the initial movement direction based on starting position.
        """
        # The direction is determined by the order of body segments
        head, neck = self.body[0], self.body[1]
        return (head[0] - neck[0], head[1] - neck[1])

    def get_move_from_buffer(self):
        if self.input_buffer:
            # Process the first valid input in the buffer
            new_direction = self.input_buffer.pop(0)
        return new_direction

    def move(self, new_direction):
        if not self.is_opposite_direction(new_direction):
            self.direction = new_direction
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        self.body.insert(0, new_head)
        # self.body.pop()

    def grow(self):
        tail = self.body[-1]
        self.body.append(tail)

    def shrink(self):
        if len(self.body) > 0:
            self.body.pop()

    def add_direction_to_buffer(self, new_direction):
        if len(self.input_buffer) < 2 and \
                (not self.input_buffer or
                 self.input_buffer[-1] != new_direction):
            self.input_buffer.append(new_direction)

    def is_opposite_direction(self, new_direction):
        opposite_directions = {
            (1, 0): (-1, 0),   # Right vs Left
            (-1, 0): (1, 0),   # Left vs Right
            (0, 1): (0, -1),   # Down vs Up
            (0, -1): (0, 1)    # Up vs Down
        }
        return new_direction == opposite_directions.get(self.direction)


class SnakeGame:
    colors = {
        'background': (0, 0, 0),
        'snake_body': (200, 200, 200),
        'snake_head': (255, 255, 255),
        'green_apple': (0, 255, 0),
        'red_apple': (255, 0, 0)
    }

    def __init__(self, grid_size=10, random_start=True, render=True,
                 block_size=50, margin=50):
        if grid_size < 3:
            raise ValueError("Grid size must be at least 3.")
        self.random_start = random_start
        self.grid_size = grid_size
        self.render = render
        self.snake = Snake(grid_size, random_start)

        # Initialize apples
        self.green_apples = [Apple(type='green') for _ in range(2)]
        self.red_apple = Apple(type='red')
        self._reset_apples()

        self.last_happening = LastHappening.NONE
        self.game_over = False

        if render:
            self.block_size = block_size
            self.margin = margin
            # Make the window larger than the grid
            self.screen_size = (grid_size * block_size) + 2 * margin
            pg.init()
            self.screen = pg.display.set_mode((self.screen_size,
                                               self.screen_size))
            pg.display.set_caption("Snake")
            self.clock = pg.time.Clock()
            self.font = pg.font.Font(None, 69)
            self._draw()
            sleep(1)

    def reset_game(self):
        self.snake.reset(self.grid_size, random_start=self.random_start)
        self._reset_apples()
        self.game_over = False

    def step(self, move_direction):
        if self.game_over:
            raise ValueError("Game is over. Cannot take further action")
        self._update_game_state(move_direction)
        if self.render:
            self._draw()
            if self.game_over:
                self._draw_game_over()

    def human_play(self, fps=5):
        if not self.render:
            raise ValueError("Rendering must be enabled to play the game \
manually.")
        # self._draw()
        # sleep(1)
        self.clock.tick(fps)
        running = True
        while running:
            self._handle_user_events()
            if not self.game_over:
                move_direction = self.snake.get_move_from_buffer()
                self._update_game_state(move_direction)
                self._draw()
                if self.game_over:
                    self._draw_game_over()
            self.clock.tick(fps)
        pg.quit()
        sys.exit()

    def _handle_user_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self._quit_game()
            elif event.type == pg.KEYDOWN:
                self._handle_keydown(event)

    def _handle_keydown(self, event):
        if event.key == pg.K_ESCAPE:
            self._quit_game()
        elif event.key == pg.K_w:
            self.snake.add_direction_to_buffer((0, -1))
        elif event.key == pg.K_s:
            self.snake.add_direction_to_buffer((0, 1))
        elif event.key == pg.K_a:
            self.snake.add_direction_to_buffer((-1, 0))
        elif event.key == pg.K_d:
            self.snake.add_direction_to_buffer((1, 0))
        elif event.key == pg.K_SPACE and self.game_over:
            self._restart_game()

    def _quit_game(self):
        pg.quit()
        sys.exit()

    def _restart_game(self):
        self.reset_game()
        pg.event.clear()
        self._draw()
        sleep(1)
        self.clock.tick(5)

    def _update_game_state(self, move_direction):
        self.snake.move(move_direction)
        if self._check_collisions():
            # when the snake has crashed or became too small
            print("died")
            self.snake.shrink()
            self.last_happening = LastHappening.DIED
            self.game_over = True

    def get_data(self):
        return self.grid_size, self.last_happening, self.snake.body, \
                                    self.green_apples, self.red_apple

    def _draw(self):
        # Clear screen
        self.screen.fill(self.colors['background'])

        # Adjust drawing offset to center the grid within the window
        grid_offset = self.margin

        for segment in reversed(self.snake.body):
            # Head is white, body is light gray
            color = self.colors['snake_head'] if segment == self.snake.body[0]\
                else self.colors['snake_body']
            pg.draw.rect(self.screen, color,
                         (grid_offset + segment[0] * self.block_size,
                          grid_offset + segment[1] * self.block_size,
                          self.block_size,
                          self.block_size))

        # Draw green apples (from current state)
        for apple in self.green_apples:
            pg.draw.rect(self.screen, self.colors['green_apple'],
                         (grid_offset + apple.position[0] * self.block_size,
                          grid_offset + apple.position[1] * self.block_size,
                          self.block_size, self.block_size))

        # Draw red apple (from current state)
        pg.draw.rect(self.screen, self.colors['red_apple'],
                     (grid_offset + self.red_apple.position[0] *
                      self.block_size, grid_offset +
                      self.red_apple.position[1] * self.block_size,
                      self.block_size, self.block_size))

        # Draw the grid (black lines)
        for x in range(self.grid_size + 1):
            pg.draw.line(self.screen, self.colors['background'],
                         (grid_offset + x * self.block_size, grid_offset),
                         (grid_offset + x * self.block_size,
                          self.screen_size - self.margin))
        for y in range(self.grid_size + 1):
            pg.draw.line(self.screen, self.colors['background'],
                         (grid_offset, grid_offset + y * self.block_size),
                         (self.screen_size - self.margin, grid_offset + y *
                          self.block_size))

        # Draw bounding box (grey lines)
        pg.draw.rect(self.screen, (150, 150, 150),
                     (grid_offset, grid_offset,
                      self.grid_size * self.block_size,
                      self.grid_size * self.block_size), 1)

        if not self.game_over:
            pg.display.flip()

    def _draw_game_over(self):
        # Display "Game Over" message in the center
        text = self.font.render("GAME OVER", True, (255, 200, 0))
        text_rect = text.get_rect(center=(self.screen_size // 2,
                                          self.screen_size // 2))
        self.screen.blit(text, text_rect)
        pg.display.flip()

    def _check_collisions(self):
        # returns True if the snake dies, False otherwise
        head = self.snake.body[0]

        # Wall collision
        if (head[0] < 0 or head[0] >= self.grid_size or
           head[1] < 0 or head[1] >= self.grid_size):
            return True

        # Self collision
        if head in self.snake.body[1:]:
            return True

        # Apple eating
        occupied_positions = set(self.snake.body +
                                 [apple.position for apple
                                  in self.green_apples] +
                                 [self.red_apple.position])

        for apple in self.green_apples:
            if head == apple.position:
                print("Green apple eaten")
                # self.snake.grow()
                apple.relocate(self.grid_size, occupied_positions)
                self.last_happening = LastHappening.GREEN_APPLE_EATEN
                return False

        if head == self.red_apple.position:
            self.red_apple.relocate(self.grid_size, occupied_positions)

            print("Red apple eaten")
            self.snake.shrink()
            if len(self.snake.body) > 1:
                self.snake.shrink()
                self.last_happening = LastHappening.RED_APPLE_EATEN
                return False
            else:
                return True

        print("No collision")
        self.snake.shrink()
        self.last_happening = LastHappening.NO_COLLISION
        return False

    def _reset_apples(self):
        occupied = set(self.snake.body)

        for apple in self.green_apples + [self.red_apple]:
            apple.relocate(self.grid_size, occupied)
            occupied.add(apple.position)
