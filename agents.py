from collections import defaultdict
import random

class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.99, epsilon=0.1):
        """
        Initialize the Q-learning agent using defaultdict.
        Args:
            alpha (float): Learning rate.
            gamma (float): Discount factor.
            epsilon (float): Exploration rate.
        """
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = defaultdict(lambda: defaultdict(float))  # Default Q-values to 0.0

    def choose_action(self, state, actions):
        """
        Choose an action based on epsilon-greedy policy.
        Args:
            state: Current state (hashable).
            actions (list): List of possible actions.
        Returns:
            Action: Chosen action.
        """
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(actions)  # Explore
        return max(actions, key=lambda action: self.q_table[state][action])  # Exploit

    def update(self, state, action, reward, next_state, next_actions):
        """
        Update the Q-table using the Bellman equation.
        Args:
            state: Current state (hashable).
            action: Action taken.
            reward (float): Reward received.
            next_state: Next state (hashable).
            next_actions (list): List of possible actions in the next state.
        """
        best_next_action = max(next_actions, key=lambda a: self.q_table[next_state][a], default=0)
        td_target = reward + self.gamma * self.q_table[next_state][best_next_action]
        td_delta = td_target - self.q_table[state][action]
        self.q_table[state][action] += self.alpha * td_delta

    def get_q_value(self, state, action):
        """
        Get the Q-value for a specific state-action pair.
        Args:
            state: State.
            action: Action.
        Returns:
            float: Q-value.
        """
        return self.q_table[state][action]

    def get_q_table(self):
        """
        Get the Q-table as a dictionary.
        Returns:
            defaultdict: The Q-table.
        """
        return self.q_table


# Example interaction (simulated)
def simulate_environment(agent, episodes=1000):
    """
    Simulate interaction with an environment.
    Args:
        agent (QLearningAgent): The Q-learning agent.
        episodes (int): Number of episodes.
    """
    for episode in range(episodes):
        state = (random.randint(0, 9), random.randint(0, 9))  # Example state (tuple)
        actions = ["up", "down", "left", "right"]  # Example actions
        done = False

        while not done:
            action = agent.choose_action(state, actions)
            next_state = (random.randint(0, 9), random.randint(0, 9))  # Example next state
            reward = random.uniform(-1, 1)  # Example reward
            next_actions = ["up", "down", "left", "right"]  # Example next actions
            agent.update(state, action, reward, next_state, next_actions)
            state = next_state
            done = random.choice([True, False])  # Example termination condition


if __name__ == "__main__":
    # Parameters for the agent
    alpha = 0.1
    gamma = 0.99
    epsilon = 0.1

    # Create and train the agent
    agent = QLearningAgent(alpha, gamma, epsilon)
    simulate_environment(agent)

    # Display part of the learned Q-table
    print("Sample Q-values:")
    for state, actions in list(agent.get_q_table().items())[:5]:  # Display the first 5 states
        print(f"State: {state}, Actions: {dict(actions)}")
