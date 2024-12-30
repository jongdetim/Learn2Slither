from game import SnakeGame
from interpreter import interpret
from agent import Agent


def main():
    # ai agent training
    game = SnakeGame(grid_size=10, random_start=True, render=False)
    while not game.game_over:
        reward, vision, raw_vision = interpret(*game.get_data())
        action = Agent.choose_action(reward, vision)
        game.step(action)


if __name__ == "__main__":
    main()
