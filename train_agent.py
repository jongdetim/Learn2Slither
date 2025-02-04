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
        state, _, possible_actions, _ = environment.reset()
        # start at 1000 to offset death penalty
        total_reward = 1000

        for _ in range(max_steps_per_episode):
            action = agent.act(state, possible_actions)  # Decide action based on current state
            next_state, reward, possible_actions, done = environment.step(action)
            agent.store_experience(state, action, reward, next_state, done)
            state = next_state
            total_reward += reward

            if done:
                break

        # Train the agent at the end of the episode
        agent.train()
        print(f"Episode {episode + 1}/{episodes}, Total Reward: {total_reward}")


def play_game(agent, environment, max_steps_per_episode, delay=0.2):
    """
    Play a game using the trained agent.
    
    Args:
        agent: An object with `act` method.
        environment: An object with `reset`, `step(action)`, and optionally `render` methods.
        max_steps_per_episode (int): Maximum number of steps per episode.
    """
    state, _, possible_actions, _ = environment.reset()
    total_reward = 1000

    for _ in range(max_steps_per_episode):
        action = agent.act(state, possible_actions)  # Decide action based on current state
        next_state, reward, possible_actions, done = environment.step(action)
        state = next_state
        total_reward += reward

        sleep(delay)  # Delay to better visualize the game
        if done:
            break

    print(f"Total Reward: {total_reward}")


if __name__ == "__main__":
    game = SnakeGame(render=False)
    environment = SnakeEnvironment(game)
    agent = QLearningAgent(alpha=0.1, gamma=0.99, epsilon_decay=0.995, epsilon=0.9, buffer_size=1000, batch_size=32)
    train_agent(agent, environment, episodes=1000, max_steps_per_episode=1000)

    # Display part of the learned Q-table
    print("Sample Q-values:")
    for state, actions in list(agent.get_q_table().items())[:20]:  # Display the first 5 states
        print(f"State: {state}, Actions: {dict(actions)}")

    # play a game with the model
    game.init_rendering()
    play_game(agent, environment, max_steps_per_episode=1000)

    # save model
