import pygame
import pygame_menu
from game import Game
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BALL_COLORS

# Global variables for menu settings
difficulty = 2
ball_color = BALL_COLORS[0]

def set_difficulty(difficulty_level, set_difficulty):
    global difficulty
    difficulty = set_difficulty

def set_color(color_index, set_color):
    global ball_color
    ball_color = BALL_COLORS[set_color - 1]

def start_game():
    game = Game(ball_color, difficulty)
    game.run()

def instructions():
    white = (255, 255, 255)
    black = (0, 0, 0)
    x = 400
    y = 300
    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Instructions')
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('Player 1 is blue, Player 2 is green', True, white)
    text1 = font.render('Player 1: A and D for movement,', True, white)
    text2 = font.render('W to shoot ball', True, white)
    textRect = text.get_rect()
    textRect.center = (x // 1.25, y // 2)
    textRect1 = text.get_rect()
    textRect1.center = (x // 1.25, y // 1.65)
    textRect2 = text.get_rect()
    textRect2.center = (x // 1.25, y // 1.4)
    while True:
        surface.fill(black)
        surface.blit(text, textRect)
        surface.blit(text1, textRect1)
        surface.blit(text2, textRect2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
                quit()
 
        
        pygame.display.update()

def menu():
    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    menu = pygame_menu.Menu('Welcome!', 400, 300, theme=pygame_menu.themes.THEME_BLUE)
    menu.add.button('Play', start_game)
    menu.add.text_input('Name: ', default='Change this...')
    menu.add.selector('Difficulty: ', [('Hard', 4), ('Medium', 3), ('Easy', 2), ('Baby', 1)], onchange=set_difficulty)
    menu.add.selector('Color', [('Red', 1), ('Green', 2), ('Blue', 3), ('White', 4), ('Black', 5)], onchange=set_color)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(surface)