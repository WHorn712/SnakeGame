from enum import Enum
import math
import pygame

import random
import numpy as np



class Color:
    """Stores the necessary colors for the game"""
    def __init__(self):
        self.white = (255, 255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (213, 50, 80)
        self.green = (0, 255, 0)
        self.blue = (50, 153, 213)

class Display:
    """Represents the game screen"""
    def __init__(self, pygame):
        self.display_width = 600
        self.display_height = 400
        self.display = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('SNAKE GAME')
        self.clock = pygame.time.Clock()

    def draw_message_gameOver(self, msg, color=Color().red):
        """Draws the game over message on the screen. It has a mandatory parameter that represents the message
        to be displayed, and an optional parameter that represents the color of the message"""
        msg = Score().font_style.render(msg, True, color)
        self.display.blit(msg, [self.display_width / 6, self.display_height / 3])

    def update_screen(self):
        """Updates the screen color"""
        self.display.fill(Color().white)

class Score:
    """Represents the game score"""
    def __init__(self):
        self.font_style = pygame.font.SysFont("bahnschrift", 25)
        self.score = 0
        self.disp = 0
        self.frame_iteration = 0

    def sum_score(self):
        """Increases the score variable by 1"""
        self.score += 1

    def sum_disp(self):
        """Increases the disp variable by 1"""
        self.disp += 1
        repeticoes = self.disp
        print(self.disp)

    def draw_score(self, display, color=Color().black):
        """Draws the score on the screen. It has one mandatory variable, which is the screen, and an optional variable,
        which is the color of the letters"""
        value = self.font_style.render("SUA PONTUAÇÃO: " + str(self.score), True, color)
        display.display.blit(value, [0, 0])

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

class Snake:
    """Represents the game's snake, contains all the variables and functions that the snake needs in the game"""
    def __init__(self, pygame, snake_block=10, snake_speed=15):
        self.x = Display(pygame).display_width / 2
        self.y = Display(pygame).display_height / 2
        self.x1_change = 0
        self.y1_change = 0
        self.block = snake_block
        self.speed = snake_speed
        self.snake_list = []
        self.length = 1
        self.direction = 1

    def draw_snake(self, display, pygame, color=Color().black):
        """Draws the snake on the screen. Requires one mandatory variable, which is the screen, and an optional
        variable, which is the color of the snake."""
        for i in self.snake_list:
            pygame.draw.rect(display.display, color, [i[0], i[1], self.block, self.block])

    def move_snake(self, new_dir):
        """Moves the snake based on the action chosen by the Q-Learning algorithm"""
        if new_dir == 3:
            if self.direction != 4:
                self.y1_change = -self.block
                self.x1_change = 0
                self.direction = 3
        elif new_dir == 4:
            if self.direction != 3:
                self.y1_change = self.block
                self.x1_change = 0
                self.direction = 4
        elif new_dir == 2:
            if self.direction != 1:
                self.x1_change = -self.block
                self.y1_change = 0
                self.direction = 2
        else:
            if self.direction != 2:
                self.x1_change = self.block
                self.y1_change = 0
                self.direction = 1

    def update_position(self):
        """Changes the snake's x and y variables according to xchange and ychange"""
        self.x += self.x1_change
        self.y += self.y1_change

    def add_block_in_snake(self):
        """Adds a block to the snake"""
        head = [self.x, self.y]
        self.snake_list.append(head)
        if len(self.snake_list) > self.length:
            del self.snake_list[0]

    def increase_size(self):
        """Adds one to the snake's size variable"""
        self.length += 1

repeticoes = 0
def position_food(display_width, display_height, block, n_game):
    lista = []
    lista.append(round(random.randrange(0, display_width, block) // 10.0) * 10.0)
    lista.append(round(random.randrange(10, display_height - 10, block) // 10.0) * 10.0)
    return lista

class Food:
    """Represents the game's food. Contains all the variables and functions of the food"""
    def __init__(self, pygame):
        self.block = 10
        lista = position_food(Display(pygame).display_width, Display(pygame).display_height, self.block, 0)
        self.x = lista[0]
        self.y = lista[1]

    def draw_food(self, pygame, disp):
        """Draws the food on the game screen. Mandatory parameters display and pygame"""
        pygame.draw.rect(disp.display, Color().green, [self.x, self.y, self.block, self.block])

    def analyze_score(self, snake, score, display):
        """Analyzes if the snake has eaten the food in the current frame. If so, all the variable changes are made"""
        if snake.x == self.x and snake.y == self.y:
            lista = position_food(display.display_width, display.display_height, self.block)
            self.x = lista[0]
            self.y = lista[1]
            snake.increase_size()
            score.sum_score()


def get_state(snake, food):
    state = (
        snake.x,
        snake.y,
        food.x,
        food.y,
        snake.direction
    )
    return state

actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
def distance_snake_food(snake, food):
    c = (food.x - snake.x)
    c = c*-1 if c<=0 else c
    b = (food.y - snake.y)
    b = b*-1 if b<=0 else b
    return math.sqrt((b**2)+(c**2))


def get_reward(last_distance, snake, food, game_close, frame_iteration, width, height):
    for x in snake.snake_list[:-1]:
        if x == [snake.x, snake.y]:
            return -11
    if game_close or frame_iteration > 100*snake.length:
        return -10
    elif snake.x == food.x and snake.y == food.y:
        return 10
    elif distance_snake_food(snake, food) < last_distance:
        return 5
    else:
        return -5

q_table = {}

alpha = 0.1
gamma = 0.9
epsilon = 0.1
num_episodes = 1000
state = [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1]

def choose_action(state):
    if random.uniform(0, 1) < epsilon:
        return random.randint(0, len(actions) - 1)
    else:
        if state not in q_table:
            q_table[state] = [0] * len(actions)
        return np.argmax(q_table[state])

def update_q_table(state, action, reward, next_state):
    if state not in q_table:
        q_table[state] = [0] * len(actions)
    if next_state not in q_table:
        q_table[next_state] = [0] * len(actions)
    best_next_action = np.argmax(q_table[next_state])
    td_target = reward + gamma * q_table[next_state][best_next_action]
    td_error = td_target - q_table[state][action]
    q_table[state][action] += alpha * td_error

def get_is_gameover(snake, disp):
    if snake.x >= disp.display_width or snake.x < 0 or snake.y >= disp.display_height or snake.y < 0:
        return True
    for x in snake.snake_list[:-1]:
        if x == [snake.x, snake.y]:
            return -11
    return False

while True:
    ok = False
    plot_scores = []
    plot_mean_scores = []
    total_score = []
    record = 0
    display = Display(pygame)
    snake = Snake(pygame)
    food = Food(pygame)
    score_game = Score()
    frame_iteraction = 0
    while True:
        last_distance = distance_snake_food(snake, food)
        frame_iteraction += 1

        move_new_dir = 0
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    move_new_dir = 1
                if event.key == pygame.K_LEFT:
                    move_new_dir = 2
                if event.key == pygame.K_UP:
                    move_new_dir = 3
                if event.key == pygame.K_DOWN:
                    move_new_dir = 4
        snake.move_snake(move_new_dir)
        snake.update_position()
        done = get_is_gameover(snake, display)
        if snake.x == food.x and snake.y == food.y:
            lista = position_food(display.display_width, display.display_height, food.block, frame_iteraction)
            food.x = lista[0]
            food.y = lista[1]
            snake.increase_size()
            score_game.sum_score()

        snake.add_block_in_snake()
        score = score_game.score
        display.update_screen()
        food.draw_food(pygame, display)
        snake.draw_snake(display, pygame)
        score_game.draw_score(display)

        if done:
            # train long memory, plot result
            frame_iteraction = 0
            snake.x = display.display_width / 2
            snake.y = display.display_height / 2
            snake.length = 1
            snake.snake_list = []
            lista = position_food(display.display_width, display.display_height, food.block, frame_iteraction)
            food.x = lista[0]
            food.y = lista[1]
            score_game.score = 0
            frame_iteraction = 0
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
