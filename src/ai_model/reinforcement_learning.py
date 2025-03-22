import numpy as np

class ReinforcementLearningAgent:
    def __init__(self, actions, state_space_size=10, epsilon=0.1, discount_factor=0.99, learning_rate=0.1):
        self.actions = actions
        self.q_table = np.zeros((state_space_size, len(actions)))  # Initialize Q-table
        self.epsilon = epsilon
        self.discount_factor = discount_factor
        self.learning_rate = learning_rate

    def choose_action(self, state):
        """Choose an action based on the current state using an epsilon-greedy strategy."""
        if np.random.rand() < self.epsilon:  # Epsilon-greedy
            return np.random.choice(self.actions)  # Explore
        else:
            return np.argmax(self.q_table[state])  # Exploit

    def learn(self, state, action, reward, next_state):
        """Update the Q-table based on the action taken and the reward received."""
        best_next_action = np.argmax(self.q_table[next_state])
        td_target = reward + self.discount_factor * self.q_table[next_state][best_next_action]
        td_delta = td_target - self.q_table[state][action]
        self.q_table[state][action] += self.learning_rate * td_delta
