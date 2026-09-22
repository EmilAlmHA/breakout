import asyncio

import pygame
import pygame_menu
import pygame_menu.controls as ctrl
import pygame_menu.menu
from game import Game
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BALL_COLORS

# Global variables for menu settings
difficulty = 2
ball_color = BALL_COLORS[0]
players = 1
PLAYER1 = 'Player 1'
PLAYER2 = 'Player 2'
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

def set_players(set_players, number):
    global players
    players = number
    if players == 1:
        input_name2.hide()
    else:
        input_name2.show()

def set_name1(name):
    global PLAYER1
    PLAYER1 = name

def set_name2(name):
    global PLAYER2
    PLAYER2 = name


async def menu():
    """Webbversion: pygame_menu.Menu.mainloop() ar en blockerande loop, den
    fungerar inte i en webblasare (som kraver att kontrollen lamnas tillbaka
    via await asyncio.sleep(0) varje bildruta). Kor darfor menyn manuellt
    med menu.update(events)/menu.draw(surface) istallet for mainloop(),
    se pygame_menu-dokumentationen "Manual loop mode".
    """
    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    while True:
        play_clicked = False
        quit_clicked = False

        def on_play():
            nonlocal play_clicked
            play_clicked = True

        def on_quit():
            nonlocal quit_clicked
            quit_clicked = True

        m = pygame_menu.Menu('Welcome!', 400, 450, theme=pygame_menu.themes.THEME_BLUE)
        m.add.button('Play', on_play)
        m.add.selector('Players:', [('1', 1), ('2', 2)], default=players - 1, onchange=set_players)

        global input_name1, input_name2
        input_name1 = m.add.text_input('Name: ', default=PLAYER1, onchange=set_name1)
        input_name2 = m.add.text_input('Name: ', default=PLAYER2, onchange=set_name2)
        if players == 1:
            input_name2.hide()

        m.add.selector('Difficulty: ', [('Hard', 4), ('Medium', 3), ('Easy', 2), ('Baby', 1)], onchange=set_difficulty)
        m.add.selector('Color', [('Red', 1), ('Green', 2), ('Blue', 3), ('White', 4), ('Black', 5)], onchange=set_color)
        m.add.button('Quit', on_quit)

        while not play_clicked and not quit_clicked:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    return
            m.update(events)
            m.draw(surface)
            pygame.display.update()
            await asyncio.sleep(0)

        if quit_clicked:
            return

        await asyncio.sleep(0.5)
        game = Game(ball_color, difficulty, players, PLAYER1, PLAYER2)
        await game.run(players)
        # Efter att en omgang tar slut (Game Over/klarat alla banor och ESC/QUIT
        # inte tryckts), visas menyn igen istallet for att avsluta processen.
