import torch
import random
import numpy as np
from collections import deque
import snake_IA as snake
import model

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:

    def __init__(self):
        self.n_game = 0
        self.epsilon = 0 # randomness
        self.gamma = 0 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = None
        self.trainer = None

    def get_state(self, display, snake, food):
        #11 valores -> 3 perigos ; 4 direção ; 4 comidas
        a = []
        if snake.direction == 1:
            a.append(1 if snake.x==display.display_width-1 else 0)
            a.append(1 if snake.y == display.display_height - 1 else 0)
            a.append(1 if snake.y == 1 else 0)
        elif snake.direction == 2:
            a.append(1 if snake.x == 1 else 0)
            a.append(1 if snake.y == 1 else 0)
            a.append(1 if snake.y == display.display_height-1 else 0)
        elif snake.direction == 3:
            a.append(1 if snake.y == 1 else 0)
            a.append(1 if snake.x == display.display_width-1 else 0)
            a.append(1 if snake.x == 1 else 0)
        else:
            a.append(1 if snake.y == display.display_height-1 else 0)
            a.append(1 if snake.x == 1 else 0)
            a.append(1 if snake.x == display.display_width-1 else 0)
        direcao = []
        direcao.append(1 if snake.direction == 2 else 0)
        direcao.append(1 if snake.direction == 1 else 0)
        direcao.append(1 if snake.direction == 3 else 0)
        direcao.append(1 if snake.direction == 4 else 0)

        comida = []
        comida.append(1 if food.x - snake.x < 0 else 0)
        comida.append(1 if food.x - snake.x > 0 else 0)
        comida.append(1 if food.y - snake.y < 0 else 0)
        comida.append(1 if food.y - snake.y > 0 else 0)

        a.extend(direcao)
        a.extend(comida)

        return np.array(a)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_game
        final_move = [0,0,0]
        if random.randint(0,200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model.predict(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move

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
                agent.model.save()

            print('Game', agent.n_game, 'Score', score, 'Record', record)

if __name__ == '__main__':
    train()