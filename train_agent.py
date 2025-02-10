from game import SnakeGame
from agents import QLearningAgent
from environments import SnakeEnvironment
from time import sleep


def train_agent(agent, environment, episodes, max_steps_per_episode):
    """
    Generalized function to train an agent in an environment.
    
    Args:
        agent: An object with `act`, `store_experience`, and `train` methods.
        environment: An object with `reset`, `step(action)`, and optionally `render` methods.
        episodes (int): Number of episodes to train.
        max_steps_per_episode (int): Maximum number of steps per episode.
    """
    for episode in range(episodes):
        state, _, possible_actions, _, stats = environment.reset()
        # start at 1000 to offset death penalty
        total_reward = 1000
        steps = 0

        for _ in range(max_steps_per_episode):
            action = agent.act(state, possible_actions)  # Decide action based on current state
            next_state, reward, possible_actions, done, stats = environment.step(action)
            agent.store_experience(state, action, reward, next_state, done)
            state = next_state
            total_reward += reward
            steps += 1

            if done:
                break

        # Train the agent at the end of the episode
        agent.train()
        print(f"Episode {episode + 1}/{episodes}, Total Reward: {total_reward}")


def play_game(agent, environment, max_steps_per_episode, delay=0.2, ignore_exploration=True):
    """
    Play a game using the trained agent, ignoring .
    
    Args:
        agent: An object with `act` method.
        environment: An object with `reset`, `step(action)`, and optionally `render` methods.
        max_steps_per_episode (int): Maximum number of steps per episode.
    """
    state, _, possible_actions, _, stats = environment.reset()
    total_reward = 1000
    steps = 0

    for _ in range(max_steps_per_episode):
        action = agent.act(state, possible_actions, ignore_exploration)  # Decide action based on current state
        next_state, reward, possible_actions, done, stats = environment.step(action)
        state = next_state
        total_reward += reward
        steps += 1

        sleep(delay)  # Delay to better visualize the game
        if done:
            break

    # print(f"Total Reward: {total_reward}")
    return total_reward, steps, stats


def benchmark_agent(agent, environment, games, max_steps_per_episode):
    """
    Benchmark the agent by playing multiple games and calculating the average snake length and step count.
    
    Args:
        agent: An object with `act` method.
        environment: An object with `reset`, `step(action)`, and optionally `render` methods.
        games (int): Number of games to play for benchmarking.
        max_steps_per_episode (int): Maximum number of steps per episode.
    """
    total_steps = 0
    total_snake_length = 0
    max_snake_length = 0

    for game in range(games):
        total_reward, step_count, snake_length = play_game(agent, environment, max_steps_per_episode, delay=0)
        total_steps += step_count
        total_snake_length += snake_length
        max_snake_length = max(max_snake_length, snake_length)
        # print(f"Game {game + 1}/{games}, Steps: {step_count}, Snake Length: {snake_length}")

    average_steps = total_steps / games
    average_snake_length = total_snake_length / games

    print(f"Average Steps: {average_steps}")
    print(f"Average Snake Length: {average_snake_length}")
    print(f"Max Snake Length: {max_snake_length}")


if __name__ == "__main__":
    game = SnakeGame(render=False)
    environment = SnakeEnvironment(game)
    agent = QLearningAgent(alpha=0.05, gamma=0.7, epsilon_decay=0.999, epsilon=0.9, buffer_size=500, batch_size=32)
    train_agent(agent, environment, episodes=10000, max_steps_per_episode=1000)

    # # Display part of the learned Q-table
    # print("Sample Q-values:")
    # for state, actions in list(agent.get_q_table().items())[:20]:  # Display the first 20 states
    #     print(f"State: {state}, Actions: {dict(actions)}")

    # # save model
    agent.save("snake_q_learning_agent.pkl")

    # load model
    agent.load("snake_q_learning_agent.pkl")
    # agent.load("minimal_inputs_5k_model.pkl")

    for state, actions in list(agent.get_q_table().items())[:20]:  # Display the first 20 states
        print(f"State: {state}, Actions: {dict(actions)}")

    # play a game with the model
    # game.init_rendering()
    benchmark_agent(agent, environment, 1, max_steps_per_episode=1000)
    # play_game(agent, environment, max_steps_per_episode=1000)
