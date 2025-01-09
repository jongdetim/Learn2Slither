from game import SnakeGame
from agents import QLearningAgent
from environments import SnakeEnvironment


# def test_botgame():
#     # testing the game iwth a constant input
#     game = SnakeGame(grid_size=10, random_start=True, render=True)
#     while not game.game_over:
#         reward, vision, raw_vision = interpret(*game.get_data())
#         # action = Agent.choose_action(reward, vision)
#         action = (0, 1)
#         game.step(action)
#         time.sleep(0.1)

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
        state = environment.reset()
        total_reward = 0

        for step in range(max_steps_per_episode):
            action = agent.act(state)  # Decide action based on current state
            next_state, reward, done = environment.step(action)
            agent.store_experience(state, action, reward, next_state, done)
            state = next_state
            total_reward += reward

            if done:
                break
        
        # Train the agent at the end of the episode
        agent.train()
        print(f"Episode {episode + 1}/{episodes}, Total Reward: {total_reward}")


if __name__ == "__main__":
    game = SnakeGame(render=False)
    environment = SnakeEnvironment(game)
    agent = QLearningAgent(alpha=0.1, gamma=0.99, epsilon=0.1)
    train_agent(agent, environment, episodes=1000, max_steps_per_episode=1000)

    # Display part of the learned Q-table
    print("Sample Q-values:")
    for state, actions in list(agent.get_q_table().items())[:5]:  # Display the first 5 states
        print(f"State: {state}, Actions: {dict(actions)}")
