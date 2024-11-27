import pygame
import random
import sys

class Apple:
    def __init__(self, color):
        self.color = color
        self.x = 0
        self.y = 0

    def relocate(self, grid_size, occupied_positions):
        while True:
            self.x = random.randint(0, grid_size - 1)
            self.y = random.randint(0, grid_size - 1)
            if (self.x, self.y) not in occupied_positions:
                break

class Snake:
    def __init__(self, grid_size):
        center = grid_size // 2
        self.body = [(center, center)]
        self.direction = (1, 0)  # Initially moving right
        self.grid_size = grid_size
        self.input_buffer = []  # Input buffer for direction changes

    def move(self):
        if self.input_buffer:
            # Process the first valid input in the buffer
            new_direction = self.input_buffer.pop(0)
            if not self.is_opposite_direction(new_direction):
                self.direction = new_direction
        
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        self.body.insert(0, new_head)
        self.body.pop()

    def grow(self):
        tail = self.body[-1]
        self.body.append(tail)

    def shrink(self):
        if len(self.body) > 1:
            self.body.pop()

    def add_direction_to_buffer(self, new_direction):
        if len(self.input_buffer) < 2 and (not self.input_buffer or self.input_buffer[-1] != new_direction):
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
    def __init__(self, grid_size=10, block_size=50, margin=50):
        pygame.init()
        
        self.grid_size = grid_size
        self.block_size = block_size
        self.margin = margin
        self.screen_size = (grid_size * block_size) + 2 * margin  # Make the window larger than the grid
        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size))
        pygame.display.set_caption("Snake Game")
        
        self.snake = Snake(grid_size)
        
        # Colors
        self.colors = {
            'background': (0, 0, 0),
            'snake_body': (200, 200, 200),
            'snake_head': (255, 255, 255),
            'green_apple': (0, 255, 0),
            'red_apple': (255, 0, 0)
        }
        
        # Initialize apples
        self.green_apples = [Apple(color='green') for _ in range(2)]
        self.red_apple = Apple(color='red')
        
        # Randomize initial apple positions
        self._relocate_apples()
        
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.font = pygame.font.Font(None, 36)

    def reset_game(self):
        # Reset snake
        center = self.grid_size // 2
        self.snake.body = [(center, center)]
        self.snake.direction = (1, 0)  # Initially moving right
        self.snake.next_direction = self.snake.direction

        # Reset apples
        self._relocate_apples()
        self.game_over = False

    def play(self):
        move_event = pygame.USEREVENT + 1
        pygame.time.set_timer(move_event, 200)  # Move every 200 ms
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_w:
                        self.snake.add_direction_to_buffer((0, -1))
                    elif event.key == pygame.K_s:
                        self.snake.add_direction_to_buffer((0, 1))
                    elif event.key == pygame.K_a:
                        self.snake.add_direction_to_buffer((-1, 0))
                    elif event.key == pygame.K_d:
                        self.snake.add_direction_to_buffer((1, 0))
                    elif event.key == pygame.K_SPACE and self.game_over:
                        # Start a new game
                        self.reset_game()
                
                # Move snake on timer event
                if event.type == move_event and not self.game_over:
                    # Save current snake state before moving (if game over is not set)
                    if not self.game_over:
                        self.saved_snake_body = list(self.snake.body)
                    
                    # Move snake
                    self.snake.move()
                    
                    # Check for collisions
                    if not self._check_collisions():
                        self.game_over = True
            
            # Draw game state only if the game is still running
            if not self.game_over:
                self._draw()
            
            # If the game is over, render the saved state
            if self.game_over:
                self.snake.body = self.saved_snake_body
                self._draw()
                self._draw_game_over()
            
            # Control frame rate
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

    def _draw(self):
        # Clear screen
        self.screen.fill(self.colors['background'])
        
        # Adjust drawing offset to center the grid within the window
        grid_offset = self.margin
        
        # Draw snake body (from saved state if game is over)
        snake_body_to_draw = self.saved_snake_body if self.game_over else self.snake.body
        
        for i, segment in enumerate(snake_body_to_draw):
            # Head is white, body is light gray
            color = self.colors['snake_head'] if i == 0 else self.colors['snake_body']
            pygame.draw.rect(self.screen, color, 
                            (grid_offset + segment[0] * self.block_size, 
                            grid_offset + segment[1] * self.block_size, 
                            self.block_size, 
                            self.block_size))
        
        # Draw green apples (from current state)
        for apple in self.green_apples:
            pygame.draw.rect(self.screen, self.colors['green_apple'], 
                            (grid_offset + apple.x * self.block_size, 
                            grid_offset + apple.y * self.block_size, 
                            self.block_size, 
                            self.block_size))
        
        # Draw red apple (from current state)
        pygame.draw.rect(self.screen, self.colors['red_apple'], 
                        (grid_offset + self.red_apple.x * self.block_size, 
                        grid_offset + self.red_apple.y * self.block_size, 
                        self.block_size, 
                        self.block_size))
        
        # Draw the grid (grey lines)
        grid_color = (169, 169, 169)  # Light grey color for the grid
        for x in range(self.grid_size + 1):
            pygame.draw.line(self.screen, grid_color, 
                            (grid_offset + x * self.block_size, grid_offset), 
                            (grid_offset + x * self.block_size, self.screen_size - self.margin))
        for y in range(self.grid_size + 1):
            pygame.draw.line(self.screen, grid_color, 
                            (grid_offset, grid_offset + y * self.block_size), 
                            (self.screen_size - self.margin, grid_offset + y * self.block_size))
        if not self.game_over:
            pygame.display.flip()

    def _draw_game_over(self):        
        # Display "Game Over" message in the center
        text = self.font.render("Game Over", True, (255, 0, 0))
        text_rect = text.get_rect(center=(self.screen_size // 2, self.screen_size // 2))
        self.screen.blit(text, text_rect)
        
        pygame.display.flip()


    def _check_collisions(self):
        head = self.snake.body[0]
        
        # Wall collision
        if (head[0] < 0 or head[0] >= self.grid_size or 
            head[1] < 0 or head[1] >= self.grid_size):
            return False
        
        # Self collision (checking all body segments except the neck)
        if head in self.snake.body[1:]:
            return False
        
        # Apple eating
        for apple in self.green_apples:
            if head == (apple.x, apple.y):
                self.snake.grow()
                apple.relocate(self.grid_size, set(self.snake.body + self.green_apples + [self.red_apple]))
        
        if head == (self.red_apple.x, self.red_apple.y):
            self.snake.shrink()
            self.red_apple.relocate(self.grid_size, set(self.snake.body + [self.red_apple] + self.green_apples))

        # print(len(set(self.snake.body + [self.red_apple] + self.green_apples)))

        return True

    def _relocate_apples(self):
        occupied = set(self.snake.body)
        occupied.update((apple.x, apple.y) for apple in self.green_apples + [self.red_apple])

        for apple in self.green_apples + [self.red_apple]:
            apple.relocate(self.grid_size, occupied)
            occupied.add((apple.x, apple.y))

def main():
    game = SnakeGame(grid_size=10, block_size=50)
    game.play()

if __name__ == "__main__":
    main()
