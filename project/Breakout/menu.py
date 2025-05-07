import pygame
import pygame_menu
import pygame_menu.controls as ctrl
from game import Game
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BALL_COLORS

# Global variables for menu settings
difficulty = 2
ball_color = BALL_COLORS[0]
pygame.joystick.init()
joystick1 = None
joystick2 = None
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    
    if pygame.joystick.get_count() > 1:
        joystick2 = pygame.joystick.Joystick(1)
        joystick2.init()
        
    if pygame.joystick.get_count() == 0:
        keys = pygame.key.get_pressed()
        ctrl.KEY_APPLY = keys[pygame.K_RETURN]


def set_difficulty(difficulty_level, set_difficulty):
    global difficulty
    difficulty = set_difficulty

def set_color(color_index, set_color):
    global ball_color
    ball_color = BALL_COLORS[set_color - 1]

def start_game():
    pygame.time.wait(500)
    game = Game(ball_color, difficulty)
    game.run()


def menu():
    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    menu = pygame_menu.Menu('Welcome!', 400, 300, theme=pygame_menu.themes.THEME_BLUE)
    menu.add.button('Play', start_game)
    menu.add.text_input('Name: ', default='Change this...')
    menu.add.selector('Difficulty: ', [('Hard', 4), ('Medium', 3), ('Easy', 2), ('Baby', 1)], onchange=set_difficulty)
    menu.add.selector('Color', [('Red', 1), ('Green', 2), ('Blue', 3), ('White', 4), ('Black', 5)], onchange=set_color)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(surface)