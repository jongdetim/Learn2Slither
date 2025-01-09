import random
from collections import defaultdict, deque


class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.99, epsilon=0.1, buffer_size=1000, batch_size=32):
        """
        Initialize the Q-learning agent using defaultdict.
        Args:
            alpha (float): Learning rate.
            gamma (float): Discount factor.
            epsilon (float): Exploration rate.
            buffer_size (int): Maximum size of the replay buffer.
            batch_size (int): Number of experiences to sample for training.
        """
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = defaultdict(lambda: defaultdict(float))  # Default Q-values to 0.0
        
        # Replay buffer
        self.buffer = deque(maxlen=buffer_size)
        self.batch_size = batch_size

    def act(self, state, actions):
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
        max_next_q_value = max([self.q_table[next_state][a] for a in next_actions], default=0)
        td_target = reward + self.gamma * max_next_q_value
        td_delta = td_target - self.q_table[state][action]
        self.q_table[state][action] += self.alpha * td_delta

    def store_experience(self, state, action, reward, next_state, done):
        """
        Store a single experience in the replay buffer.
        Args:
            state: Current state (hashable).
            action: Action taken.
            reward (float): Reward received.
            next_state: Next state (hashable).
            done (bool): Whether the episode is finished.
        """
        self.buffer.append((state, action, reward, next_state, done))

    def train(self):
        """
        Train the Q-table using a batch of experiences from the replay buffer.
        """
        if len(self.buffer) < self.batch_size:
            return  # Not enough experiences to sample a full batch

        batch = random.sample(self.buffer, self.batch_size)
        
        for state, action, reward, next_state, done in batch:
            # Determine the list of possible actions for the next_state
            next_actions = list(self.q_table[next_state].keys()) if not done else []
            self.update(state, action, reward, next_state, next_actions)

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
            defaultdict: The nested Q-table.
        """
        return self.q_table