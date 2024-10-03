import logica_negocio.snake_game as sg



class Display(sg.Display):
    """Child class inheriting from the Display class found in the logic_negocio module. It overrides the screen,
    the name, and the passage of time using pygame."""
    def __init__(self, pygame=None):
        super().__init__()
        self.display = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('SNAKE GAME')
        self.clock = pygame.time.Clock()

    def update_screen(self):
        """Updates the screen color"""
        self.display.fill(sg.Color().white)

class Score(sg.Score):
    """Child class inheriting from the Score class found in the logic_negocio module. It overrides the font of the text
    that will display the score on the screen and the function responsible for inserting the score on the screen."""
    def __init__(self, pygame=None):
        super().__init__()
        self.font_style = pygame.font.SysFont("bahnschrift", 25)

    def draw_score(self, display, color=sg.Color().black):
        """Draws the score on the screen. It has one mandatory variable, which is the screen, and an optional variable,
        which is the color of the letters"""
        value = self.font_style.render("SUA PONTUAÇÃO: " + str(self.score), True, color)
        display.display.blit(value, [0, 0])

class Snake(sg.Snake):
    """Child class inheriting from the Snake class found in the logic_negocio module. It only overrides the
    illustration on the screen using pygame"""
    def __init__(self, pygame=None):
        super().__init__(x=Display(pygame).display_width/2, y=Display(pygame).display_height/2)

    def draw_snake(self, display, pygame, color=sg.Color().black):
        """Draws the snake on the screen. Requires one mandatory variable, which is the screen, and an optional
        variable, which is the color of the snake."""
        for i in self.snake_list:
            pygame.draw.rect(display.display, color, [i[0], i[1], self.block, self.block])

class Food(sg.Food):
    """Child class inheriting from the Food class found in the logic_negocio module. It only overrides the
    illustration on the screen using pygame."""
    def __init__(self):
        super().__init__()

    def draw_food(self, pygame, disp):
        """Draws the food on the game screen. Mandatory parameters display and pygame"""
        pygame.draw.rect(disp.display, sg.Color().green, [self.x, self.y, self.block, self.block])
