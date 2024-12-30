from game import SnakeGame


def main():
    # human play
    game = SnakeGame(grid_size=10, random_start=False, render=True,
                     block_size=50, margin=50)
    game.human_play(fps=5)


if __name__ == "__main__":
    main()
