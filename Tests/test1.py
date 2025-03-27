import pygame
import pygame_menu

pygame.init()
surface = pygame.display.set_mode((600, 400))

WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)
BLACK = (0,0,0)


def set_color(value, color):
    if(value == 1):
        color = RED
    elif(value == 2):
        color = GREEN
    elif(value == 3):
        color = BLUE
    elif(value == 4):
        color = WHITE
    elif(value == 5):
        color = BLACK
    else:
        color = BLACK

    pass


def set_difficulty(value, difficulty): 

    pass

def start_game():

    pass

menu = pygame_menu.Menu('Welcome!', 400, 300, theme=pygame_menu.themes.THEME_BLUE)
menu.add.button('Play', start_game)
menu.add.text_input('Name: ', default='Change this...')
menu.add.selector('Difficulty: ', [('Hard', 1), ('Medium', 2), ('Easy', 3), ('Baby', 4)], onchange=set_difficulty)
menu.add.selector('Color', [('Red', 1), ('Green', 2), ('Blue', 3), ('White', 4), ('Black', 5)], onchange=set_color)
menu.add.button('Quit', pygame_menu.events.EXIT)
menu.mainloop(surface)