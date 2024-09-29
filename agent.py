import torch
import random
import numpy as np
from collections import deque
import snake_IA as snake_game
from model import Linear_QNet, QTrainer
import pygame
from snake_IA import Display

pygame.init()

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    """Class that acts as a bridge between the model and the game."""
    def __init__(self):
        self.n_game = 0
        self.epsilon = 80 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(15, 512, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, display, snake, food):
        """Function that returns the game state as a list of 15 binary numbers. 3 values about walls immediately ahead;
        4 values about the snake's direction; 4 values about the position of the food relative to the snake; 3 values
        about the danger of walls according to the quadrant the snake is in; 1 value indicating if the snake and food
        are in the same quadrant, which is 1 if true, otherwise 0."""
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

        width = display.display_width
        height = display.display_height
        paredes_quadrante = []
        snx = 1 if snake.x < width // 2 else 2
        snake_quadrante = 1
        if snx == 1:
            snake_quadrante = 1 if snake.y < height // 2 else 3
        else:
            snake_quadrante = 2 if snake.y < height // 2 else 4

        if snake_quadrante == 1:
            if snake.direction ==1:
                paredes_quadrante.append(0)
                paredes_quadrante.append(0)
                paredes_quadrante.append(1)
            elif snake.direction ==2:
                paredes_quadrante.append(1)
                paredes_quadrante.append(1)
                paredes_quadrante.append(0)
            elif snake.direction ==3:
                paredes_quadrante.append(1)
                paredes_quadrante.append(0)
                paredes_quadrante.append(1)
            else:
                paredes_quadrante.append(0)
                paredes_quadrante.append(1)
                paredes_quadrante.append(0)
        elif snake_quadrante==2:
            if snake.direction == 1:
                paredes_quadrante.append(1)
                paredes_quadrante.append(0)
                paredes_quadrante.append(1)
            elif snake.direction == 2:
                paredes_quadrante.append(0)
                paredes_quadrante.append(1)
                paredes_quadrante.append(0)
            elif snake.direction == 3:
                paredes_quadrante.append(1)
                paredes_quadrante.append(1)
                paredes_quadrante.append(0)
            else:
                paredes_quadrante.append(0)
                paredes_quadrante.append(0)
                paredes_quadrante.append(1)
        elif snake_quadrante==3:
            if snake.direction == 1:
                paredes_quadrante.append(0)
                paredes_quadrante.append(1)
                paredes_quadrante.append(0)
            elif snake.direction == 2:
                paredes_quadrante.append(1)
                paredes_quadrante.append(0)
                paredes_quadrante.append(1)
            elif snake.direction == 3:
                paredes_quadrante.append(0)
                paredes_quadrante.append(0)
                paredes_quadrante.append(1)
            else:
                paredes_quadrante.append(1)
                paredes_quadrante.append(1)
                paredes_quadrante.append(0)
        else:
            if snake.direction ==1:
                paredes_quadrante.append(1)
                paredes_quadrante.append(1)
                paredes_quadrante.append(0)
            elif snake.direction ==2:
                paredes_quadrante.append(0)
                paredes_quadrante.append(0)
                paredes_quadrante.append(1)
            elif snake.direction ==3:
                paredes_quadrante.append(0)
                paredes_quadrante.append(1)
                paredes_quadrante.append(0)
            else:
                paredes_quadrante.append(1)
                paredes_quadrante.append(0)
                paredes_quadrante.append(1)

        fnx = 1 if food.x < width // 2 else 2
        food_quadrante = 1
        if fnx == 1:
            food_quadrante = 1 if food.y < height // 2 else 3
        else:
            food_quadrante = 2 if food.y < height // 2 else 4
        quadrante = [1 if snake_quadrante==food_quadrante else 0]
        a.extend(paredes_quadrante)
        a.extend(direcao)
        a.extend(comida)
        a.extend(quadrante)
        return np.array(a)

    def remember(self, state, action, reward, next_state, done):
        """Function that stores the experience in the agent's memory."""
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        """Function that trains the agent using a batch of experiences from memory."""
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        """This function updates the agent's model with the latest experience consisting of the current state, action
        taken, reward received, next state, and whether the episode has ended. This immediate update helps the agent
        quickly adapt to new information and refine its decision-making process on-the-fly."""
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state, score):
        """Function that returns the snake's action according to the trained model and the current state."""
        # random moves: tradeoff exploration / exploitation
        if self.n_game <= 30:
            self.epsilon -= 1
        else:
            self.epsilon -= score if self.epsilon - score >= 10 else 0

        final_move = [0,0,0]
        if random.randint(0,200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move

#Main game loop with pygame.
while True:
    record = 0
    agent = Agent()
    display = Display(pygame)
    snake = snake_game.Snake(pygame)
    food = snake_game.Food(pygame)
    score_game = snake_game.Score(pygame)
    frame_iteraction = 0
    while True:
        last_distance = snake_game.distance_snake_food(snake, food)
        frame_iteraction += 1
        # get old state
        state_old = agent.get_state(display, snake, food)

        # get move
        final_move = agent.get_action(state_old, record)

        snake.move_snake(final_move)
        snake.update_position()
        done = snake_game.get_is_gameover(snake, display)
        reward = snake_game.get_reward(last_distance, snake, food, done, frame_iteraction, display.display_width, display.display_height)
        if reward == 10:
            lista = snake_game.position_food(display.display_width, display.display_height, food.block, snake=snake)
            food.x = lista[0]
            food.y = lista[1]
            snake.increase_size()
            score_game.sum_score()
        elif reward == -10:
            pass
        else:
            pass
        snake.add_block_in_snake()
        score = score_game.score
        display.update_screen()
        food.draw_food(pygame, display)
        snake.draw_snake(display, pygame)
        score_game.draw_score(display)

        # perform move and get new state
        state_new = agent.get_state(display, snake, food)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory, plot result
            frame_iteraction = 0
            snake.x = display.display_width / 2
            snake.y = display.display_height / 2
            snake.length = 1
            snake.snake_list = []
            lista = snake_game.position_food(display.display_width, display.display_height, food.block, snake=snake)
            food.x = lista[0]
            food.y = lista[1]
            score_game.score = 0
            agent.n_game += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game', agent.n_game, 'Score', score, 'Record', record)
        ok = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    ok = True
        if ok:
            break
        display.update_screen()
        food.draw_food(pygame, display)
        snake.draw_snake(display, pygame)
        score_game.draw_score(display)
        pygame.display.update()
        display.clock.tick(snake.speed)
    pygame.quit()
    quit()