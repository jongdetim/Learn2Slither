from game import SnakeGame
from interpreter import interpret
# from agent import Agent

import time

def main():
    # ai agent training
    game = SnakeGame(grid_size=10, random_start=True, render=True)
    while not game.game_over:
        reward, vision, raw_vision = interpret(*game.get_data())
        # action = Agent.choose_action(reward, vision)
        action = (0, 1)
        game.step(action)
        time.sleep(0.1)


if __name__ == "__main__":
    main()
