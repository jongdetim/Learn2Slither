from constants import LastHappening
from game import SnakeGame
from agents import QLearningAgent
from environments import SnakeEnvironment
from time import sleep


def train_agent(agent, environment, episodes):
    """
    Generalized function to train an agent in an environment.
    
    Args:
        agent: An object with `act`, `store_experience`, and `train` methods.
        environment: An object with `reset`, `step(action)`, and optionally `render` methods.
        episodes (int): Number of episodes to train.
    """
    for episode in range(episodes):
        state, _, possible_actions, done, stats = environment.reset()
        total_reward = 0
        step = 0

        while not done:
            action = agent.act(state, possible_actions)  # Decide action based on current state
            next_state, reward, possible_actions, done, stats = environment.step(action)
            agent.store_experience(state, action, reward, next_state, done)
            state = next_state
            total_reward += reward
            step += 1

        # Train the agent at the end of the episode
        agent.train()
        print(f"Episode {episode + 1}/{episodes}, Total Reward: {total_reward}")
        print(f"Snake Length: {stats} steps: {step}")


def play_game(agent, environment, delay=0.2, ignore_exploration=True):
    """
    Play a game using the trained agent.

    Args:
        agent: An object with `act` method.
        environment: An object with `reset`, `step(action)`, and optionally `render` methods.
    """
    state, _, possible_actions, done, stats = environment.reset()
    total_reward = 0
    steps = 0

    while not done:
        action = agent.act(state, possible_actions, ignore_exploration)  # Decide action based on current state
        next_state, reward, possible_actions, done, stats = environment.step(action)
        state = next_state
        total_reward += reward
        steps += 1

        sleep(delay)  # Delay to better visualize the game

    print(f"Total Reward: {total_reward}")
    print(f"Snake Length: {stats} steps: {steps}")
    if total_reward == -1000 and stats == 3 and steps == 1:
        sleep(1)
    return total_reward, steps, stats


def benchmark_agent(agent, environment, games):
    """
    Benchmark the agent by playing multiple games and calculating the average snake length and step count.

    Args:
        agent: An object with `act` method.
        environment: An object with `reset`, `step(action)`, and optionally `render` methods.
        games (int): Number of games to play for benchmarking.
    """
    total_steps = 0
    total_snake_length = 0
    max_snake_length = 0
    total_rewards = 0

    for game in range(games):
        total_reward, step_count, snake_length = play_game(agent, environment, delay=0)
        total_steps += step_count
        total_snake_length += snake_length
        total_rewards += total_reward
        max_snake_length = max(max_snake_length, snake_length)
        # print(f"Game {game + 1}/{games}, Steps: {step_count}, Snake Length: {snake_length}")

    average_steps = total_steps / games
    average_snake_length = total_snake_length / games
    average_total_reward = total_rewards / games

    print(f"Average Steps: {average_steps}")
    print(f"Average Snake Length: {average_snake_length}")
    print(f"Max Snake Length: {max_snake_length}")
    print(f"Average Total Reward: {average_total_reward}")


if __name__ == "__main__":
    game = SnakeGame(render=True)
    environment = SnakeEnvironment(game)
    environment.max_steps = 500  # Set max steps per episode
    agent = QLearningAgent(alpha=0.1, gamma=0.9, epsilon_decay=0.9998, epsilon=0.9, minimum_epsilon=0.02, buffer_size=16000, batch_size=256)

    # train_agent(agent, environment, episodes=100)

    # # save model
    # agent.save("test7.pkl")

    # load model
    agent.load("test7.pkl")
    # agent.load("best_model_GRNC_10k_agent.pkl")
    # agent.load("depth_vision_agent_10k.pkl")
    # agent.load("depth_vision_agent_15k_08gamma.pkl")
    # agent.load("depth_vision_agent_10k_5-100-1000rewards_09gamma_200maxsteps_punish_on_timeout.pkl")

    # for state, actions in list(agent.get_q_table().items())[:20]:  # Display the first 20 states
    #     print(f"State: {state}, Actions: {dict(actions)}")

    print(agent.q_table.__len__())
    environment.max_steps = 1000  # See how the agent performs with a higher max step count
    benchmark_agent(agent, environment, 100)
    # play a game with the model
    game.init_rendering()
    play_game(agent, environment)
