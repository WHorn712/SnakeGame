from enum import Enum
import math
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

    def update_screen(self):
        """Updates the screen color"""
        self.display.fill(Color().white)

class Score:
    """Represents the game score"""
    def __init__(self, pygame):
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
    """ENUM class that represents all the directions in which the snake moves."""
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

    def move_snake(self, action):
        """Moves the snake based on the action chosen by the Q-Learning algorithm"""
        clock_wise = [Direction.RIGHT.value, Direction.DOWN.value, Direction.LEFT.value, Direction.UP.value]
        idx = clock_wise.index(self.direction)
        if np.array_equal(action, [1,0,0]):
            new_dir = clock_wise[idx]
        elif np.array_equal(action, [0,1,0]):
            next_idx = (idx+1) % 4
            new_dir = clock_wise[next_idx]
        else:
            next_idx = (idx-1) % 4
            new_dir = clock_wise[next_idx]

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

class Food:
    """Represents the game's food. Contains all the variables and functions of the food"""
    def __init__(self, pygame):
        self.block = 10
        lista = position_food(Display(pygame).display_width, Display(pygame).display_height, self.block)
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


def position_food(display_width, display_height, block, snake=None):
    """Function that randomizes a new position for the food."""
    if snake == None:
        lista = []
        lista.append(round(random.randrange(0, display_width, block) // 10.0) * 10.0)
        lista.append(round(random.randrange(10, display_height - 10, block) // 10.0) * 10.0)
        return lista
    lista = []
    x = []
    y = []
    for i in snake.snake_list:
        x.append(i[0])
        y.append(i[1])
    ok = True
    while ok:
        lista.append(round(random.randrange(0, display_width, block) // 10.0) * 10.0)
        lista.append(round(random.randrange(10, display_height - 10, block) // 10.0) * 10.0)
        if lista[0] not in x or lista[1] not in y:
            ok = False
    return lista

def distance_snake_food(snake, food):
    """Function that returns the distance between the snake and the food in the form of a hypotenuse."""
    c = (food.x - snake.x)
    c = c*-1 if c<=0 else c
    b = (food.y - snake.y)
    b = b*-1 if b<=0 else b
    return math.sqrt((b**2)+(c**2))

def get_reward(last_distance, snake, food, game_close, frame_iteration, width, height):
    """Function that returns the snake's reward for making the movement decision."""
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

def get_is_gameover(snake, disp):
    """Function that checks if the snake has hit the wall or itself."""
    if snake.x >= disp.display_width or snake.x < 0 or snake.y >= disp.display_height or snake.y < 0:
        return True
    for x in snake.snake_list[:-1]:
        if x == [snake.x, snake.y]:
            return True
    return False
