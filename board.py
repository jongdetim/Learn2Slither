import curses
import random
from collections import deque

# Constants
BOARD_SIZE = 10
SNAKE_CHAR = "█"
GREEN_APPLE = "G"
RED_APPLE = "R"
EMPTY_CELL = " "

# Colors
COLOR_WHITE = 1
COLOR_GREEN = 2
COLOR_RED = 3

class SnakeGame:
    def __init__(self):
        self.board = [[EMPTY_CELL for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.snake = deque([(0, 0), (0, 1), (0, 2)])  # Initial snake of length 3
        self.direction = (0, 1)  # Moving right
        self.spawn_apples()

    def spawn_apples(self):
        """Place green and red apples randomly on the board."""
        for _ in range(2):  # Two green apples
            self.place_apple(GREEN_APPLE)
        self.place_apple(RED_APPLE)  # One red apple

    def place_apple(self, apple_type):
        while True:
            row = random.randint(0, BOARD_SIZE - 1)
            col = random.randint(0, BOARD_SIZE - 1)
            if self.board[row][col] == EMPTY_CELL:
                self.board[row][col] = apple_type
                break

    def move_snake(self):
        """Move the snake in the current direction."""
        head_row, head_col = self.snake[-1]
        delta_row, delta_col = self.direction
        new_head = (head_row + delta_row, head_col + delta_col)

        # Check for collisions
        if (new_head[0] < 0 or new_head[0] >= BOARD_SIZE or
                new_head[1] < 0 or new_head[1] >= BOARD_SIZE or
                new_head in self.snake):
            return False  # Game over

        # Check apple type
        apple = self.board[new_head[0]][new_head[1]]
        if apple == GREEN_APPLE:
            self.snake.append(new_head)
            self.board[new_head[0]][new_head[1]] = EMPTY_CELL
            self.place_apple(GREEN_APPLE)
        elif apple == RED_APPLE:
            self.snake.append(new_head)
            self.snake.popleft()  # Shorten the snake
            self.board[new_head[0]][new_head[1]] = EMPTY_CELL
            self.place_apple(RED_APPLE)
            if len(self.snake) == 0:
                return False  # Game over
        else:
            self.snake.append(new_head)
            tail = self.snake.popleft()
            self.board[tail[0]][tail[1]] = EMPTY_CELL

        self.board[new_head[0]][new_head[1]] = SNAKE_CHAR
        return True

    def change_direction(self, key):
        """Change snake direction based on user input."""
        key_map = {
            curses.KEY_UP: (-1, 0),
            curses.KEY_DOWN: (1, 0),
            curses.KEY_LEFT: (0, -1),
            curses.KEY_RIGHT: (0, 1),
        }
        if key in key_map:
            new_dir = key_map[key]
            # Prevent the snake from reversing
            if (new_dir[0] != -self.direction[0] or new_dir[1] != -self.direction[1]):
                self.direction = new_dir

    def draw_board(self, window):
        """Render the game board."""
        window.clear()
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                char = self.board[row][col]
                if char == SNAKE_CHAR:
                    window.addstr(row, col * 2, SNAKE_CHAR, curses.color_pair(COLOR_WHITE))
                elif char == GREEN_APPLE:
                    window.addstr(row, col * 2, GREEN_APPLE, curses.color_pair(COLOR_GREEN))
                elif char == RED_APPLE:
                    window.addstr(row, col * 2, RED_APPLE, curses.color_pair(COLOR_RED))
                else:
                    window.addstr(row, col * 2, EMPTY_CELL)
        window.refresh()

def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(COLOR_WHITE, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(COLOR_GREEN, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(COLOR_RED, curses.COLOR_RED, curses.COLOR_BLACK)

    game = SnakeGame()
    stdscr.nodelay(True)
    stdscr.timeout(200)

    while True:
        game.draw_board(stdscr)
        key = stdscr.getch()
        if key != -1:
            game.change_direction(key)
        if not game.move_snake():
            break

    stdscr.addstr(BOARD_SIZE + 1, 0, "Game Over! Press any key to exit...")
    stdscr.nodelay(False)
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)
