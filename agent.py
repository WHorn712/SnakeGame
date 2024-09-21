import torch
import random
import numpy as np
from collections import deque
import snake_IA as snake

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:

    def __init__(self):
        self.n_game = 0
        self.epsilon = 0 # randomness
        self.gamma = 0 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()

    def get_state(self, snake, food):
        #11 valores -> 3 perigos ; 4 direção ; 4 comidas

        pass

    def remember(self, state, action, reward, next_state, done):
        pass

    def train_long_memory(self):
        pass

    def train_short_memory(self):
        pass

    def get_action(self, state):
        pass

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = []
    record = []
    agent = Agent()
    game = snake()
    while True:
        # get old state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory, plot result
            game.reset()
            agent.n_game += 1
            agent.train_long_memory()

            if score > record:
                recor = score
                #agent.model.save()

            print('Game', agent.n_game, 'Score', score, 'Record', record)

if __name__ == '__main__':
    train()