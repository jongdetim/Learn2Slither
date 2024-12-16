import pygame
import random
import sys

class Apple:
    def __init__(self, color):
        self.color = color
        self.position = (0, 0)

    def relocate(self, grid_size, occupied_positions):
        while True and len(occupied_positions) < grid_size ** 2:
            self.position = (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1))
            if (self.position) not in occupied_positions:
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
            self.body = [(center, center)]
            self.direction = (1, 0)  # Initially moving right

    def _generate_random_snake(self):
        """
        Generate a random contiguous starting position for the snake of length 3.
        """
        # Randomly choose an initial direction
        possible_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        initial_direction = random.choice(possible_directions)
        
        # Randomly choose a starting head position
        max_x = self.grid_size - 3 if initial_direction[0] != 0 else self.grid_size - 1
        max_y = self.grid_size - 3 if initial_direction[1] != 0 else self.grid_size - 1
        
        start_x = random.randint(0, max_x)
        start_y = random.randint(0, max_y)
        
        # Generate contiguous body segments
        body = [
            (start_x, start_y),
            (start_x - initial_direction[0], start_y - initial_direction[1]),
            (start_x - 2 * initial_direction[0], start_y - 2 * initial_direction[1]),
        ]
        return body

    def _initial_direction(self):
        """
        Determine the initial movement direction based on the snake's starting position.
        """
        # The direction is determined by the order of body segments
        head, neck = self.body[0], self.body[1]
        return (head[0] - neck[0], head[1] - neck[1])

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
    def __init__(self, grid_size=10, random_start=True, render=True, block_size=50, margin=50):
        self.random_start = random_start
        self.grid_size = grid_size
        self.render = render

        if render:
            self.block_size = block_size
            self.margin = margin
            self.screen_size = (grid_size * block_size) + 2 * margin  # Make the window larger than the grid
            pygame.init()
            self.screen = pygame.display.set_mode((self.screen_size, self.screen_size))
            pygame.display.set_caption("Snake")
            self.clock = pygame.time.Clock()
            self.font = pygame.font.Font(None, 69)
        
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

        self.game_over = False

    def reset_game(self):
        # Reset snake
        self.snake.reset(self.grid_size, random_start=self.random_start)

        # Reset apples
        self._relocate_apples()
        self.game_over = False

    def human_play(self, fps=5):
        if self.render == False:
            raise ValueError("Rendering must be enabled to play the game manually.")

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
                        pygame.event.clear()  # Clear the event queue to remove any lingering events
                
            # Move snake
            if not self.game_over:
                # Save current snake state before moving (if game over is not set)
                if not self.game_over:
                    self.saved_snake_body = list(self.snake.body)
                
                # Move snake
                self.snake.move()
                
                # Check for collisions
                if not self._check_collisions():
                    self.game_over = True

                # Draw game state
                self._draw()
                
                # If the game is over, render game over text
                if self.game_over:
                    self._draw_game_over()
            
            # Control frame rate
            self.clock.tick(fps)
        
        pygame.quit()
        sys.exit()

    def _draw(self):
        # Clear screen
        self.screen.fill(self.colors['background'])
        
        # Adjust drawing offset to center the grid within the window
        grid_offset = self.margin
        
        # Draw snake body (from saved state if game is over)
        snake_body_to_draw = self.snake.body
        
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
                            (grid_offset + apple.position[0] * self.block_size, 
                            grid_offset + apple.position[1] * self.block_size, 
                            self.block_size, 
                            self.block_size))
        
        # Draw red apple (from current state)
        pygame.draw.rect(self.screen, self.colors['red_apple'], 
                        (grid_offset + self.red_apple.position[0] * self.block_size, 
                        grid_offset + self.red_apple.position[1] * self.block_size, 
                        self.block_size, 
                        self.block_size))
        
        # Draw the grid (black lines)
        for x in range(self.grid_size + 1):
            pygame.draw.line(self.screen, self.colors['background'], 
                            (grid_offset + x * self.block_size, grid_offset), 
                            (grid_offset + x * self.block_size, self.screen_size - self.margin))
        for y in range(self.grid_size + 1):
            pygame.draw.line(self.screen, self.colors['background'], 
                            (grid_offset, grid_offset + y * self.block_size), 
                            (self.screen_size - self.margin, grid_offset + y * self.block_size))

        # Draw bounding box (grey lines)
        pygame.draw.rect(self.screen, (150, 150, 150), 
                        (grid_offset, grid_offset, 
                        self.grid_size * self.block_size, 
                        self.grid_size * self.block_size), 1)
        
        if not self.game_over:
            pygame.display.flip()

    def _draw_game_over(self):        
        # Display "Game Over" message in the center
        text = self.font.render("GAME OVER", True, (255, 200, 0))
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
            if head == (apple.position[0], apple.position[1]):
                self.snake.grow()
                apple.relocate(self.grid_size, self.snake.body + [apple.position for apple in self.green_apples] + [self.red_apple.position])
        
        if head == (self.red_apple.position[0], self.red_apple.position[1]):
            self.red_apple.relocate(self.grid_size, self.snake.body + [apple.position for apple in self.green_apples] + [self.red_apple.position])
            if len(self.snake.body) > 1:
                self.snake.shrink()
            else:
                return False

        # print(self.snake.body + [apple.position for apple in self.green_apples] + [self.red_apple.position])

        return True

    def _relocate_apples(self):
        occupied = set(self.snake.body)

        for apple in self.green_apples + [self.red_apple]:
            apple.relocate(self.grid_size, occupied)
            occupied.add(apple)

# this main function should be two serparate files, like 'human_play.py' and 'train_agent.py'
def main():
    # human play
    game = SnakeGame(grid_size=10, random_start=False, render=True, block_size=50, margin=50)
    game.human_play(fps=5)

    # ai agent training (to be implemented!)
    game = SnakeGame(grid_size=10, random_start=True, render=False)
    while game.game_over == False:
        last_happening, state = game.get_data()
        reward, vision = interpret(state, last_happening)
        action = agent.choose_action(reward, vision)
        game.take_action(action)

if __name__ == "__main__":
    main()
