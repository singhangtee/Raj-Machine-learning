__author__ = "SingHang Tee"
__organization__ = "COSC343/AIML402, University of Otago"
__email__ = "teesi25@student.otago.ac.nz"

import numpy as np
import pickle

agentName = "myrl_agent"

# Training specification
training = [
    ("value_agent.py", "valueplus_agent.py", 10000),
    ("random_agent.py", "value_agent.py", 10000),
]

save_filename = "saved_myrl_agent.pkl"

class RajAgent():
    def __init__(self, item_values, card_values):
        self.item_values = item_values
        self.card_values = card_values
        
        self.T = 0.1  # Temperature for exploration
        self.gamma = 0.99  # Discount factor
        self.alpha = 0.1  # Learning rate
        self.epsilon = 0.1  # Epsilon for epsilon-greedy exploration
        self.Q = {}  # Q-table

    def get_state(self, percepts):
        bidding_on, items_left, my_cards, bank, *opponents_cards = percepts
        
        return (
            bidding_on,
            tuple(items_left),
            tuple(my_cards)
        )

    def AgentFunction(self, percepts):
        state = self.get_state(percepts)
        available_actions = percepts[2]  # my_cards
        
        if state not in self.Q:
            self.Q[state] = {card: 0 for card in available_actions}
        
        if np.random.random() < self.epsilon:
            action = np.random.choice(available_actions)
        else:
            action = max(self.Q[state], key=self.Q[state].get)
        
        self.last_state = state
        self.last_action = action
        
        return action

    def train_start(self):
        self.epsilon = 0.1  # Reset epsilon for new training

    def train_session_start(self):
        pass

    def train_session_end(self):
        self.epsilon *= 0.9  # Decrease epsilon after each session

    def train_game_start(self):
        pass

    def train_game_end(self, banks):
        if hasattr(self, 'last_state') and hasattr(self, 'last_action'):
            if(banks[1] == banks[2]):
                reward = 10
            elif (banks[0] == banks[1] and banks[1] == banks[2]):
                reward = 0
            elif ((banks[0] == banks[1] or banks[0] == banks[2]) and banks[1] != banks[2]):
                reward = -10
            elif (banks[0] != banks[1] and banks[0] != banks[2]):
                if((banks[0] > banks[1] and banks[0] > banks[2])):
                    reward = 10
                elif (banks[0] < banks[1] and banks[0] < banks[2]):
                    reward = -10
                else:
                    reward = 0 # middle place highest among the three
            
            # Q-learning update
            old_value = self.Q[self.last_state][self.last_action]
            next_max = max(self.Q.get(self.last_state, {}).values(), default=0)
            
            new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)
            self.Q[self.last_state][self.last_action] = new_value
            
            # Reset for next game
            del self.last_state
            del self.last_action

    def train_end(self):
        pass

    def save(self, filename):
        print(f'Saving trained {agentName} agent to {filename}...')
        with open(filename, 'wb') as f:
            pickle.dump(self.__dict__, f)

    def load(self, filename):
        print(f'Loading trained {agentName} agent from {filename}...')
        with open(filename, 'rb') as f:
            self.__dict__.update(pickle.load(f))