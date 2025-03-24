<<<<<<< HEAD
import pygame
import pygame_menu 

pygame.init()
surface = pygame.display.set_mode((600, 400))

def set_difficulty(value, difficulty): 

    pass

def start_game():

    pass

menu = pygame_menu.Menu('Welcome!', 400, 300, theme=pygame_menu.themes.THEME_BLUE)
menu.add.text_input('Name: ', default='Change this')
menu.add.selector('Difficulty: ', [('Hard', 1), ('Medium', 2), ('Easy', 3), ('Baby', 4)], onchange=set_difficulty)
menu.add.button('Play', start_game)
menu.add.button('Quit', pygame_menu.events.EXIT)
=======
import pygame
import pygame_menu 

pygame.init()
surface = pygame.display.set_mode((600, 400))

def set_difficulty(value, difficulty): 

    pass

def start_game():

    pass

menu = pygame_menu.Menu('Welcome!', 400, 300, theme=pygame_menu.themes.THEME_BLUE)
menu.add.text_input('Name: ', default='Your mom')
menu.add.selector('Difficulty: ', [('Hard', 1), ('Medium', 2), ('Easy', 3), ('Baby', 4)], onchange=set_difficulty)
menu.add.button('Play', start_game)
menu.add.button('Quit', pygame_menu.events.EXIT)
>>>>>>> a7ad4f838f663953ab60d0decb1663722521beb7
menu.mainloop(surface)