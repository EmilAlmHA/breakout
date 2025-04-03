import pygame
import sys
import pygame_menu
import pygame.locals

pygame.init()
surface = pygame.display.set_mode((800, 534))

pygame.display.set_caption('Testing')
clock = pygame.time.Clock()
font = pygame.font.Font(None, 50)
player_lenght = 50
hill = pygame.image.load('Tests/Success-Story-KANAGWA-1.png')
ball = pygame.image.load('Tests/volleyball-ball.png')
ball = pygame.transform.scale(ball, (20, 20))
player = pygame.image.load('Tests/longcat90.jpg')
player = pygame.transform.scale(player, (40, player_lenght))
player = pygame.transform.rotate(player, (90))


# text_surface = font.render(f'{player_lenght}', False, 'Yellow')
# player_x_pos = 400
ball_x_pos = 0
player_x_pos = 400
movement = False

# Color definitions (ensure these are correctly defined)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

current_color = 'Yellow'


def set_difficulty(value, difficulty): 
    pass


def set_color(value, color):
    global current_color
    if value == 1:
        current_color = RED
    elif value == 2:
        current_color = GREEN
    elif value == 3:
        current_color = BLUE
    elif value == 4:
        current_color = WHITE
    elif value == 5:
        current_color = BLACK


def menu():
    menu = pygame_menu.Menu('Welcome!', 400, 300, theme=pygame_menu.themes.THEME_BLUE)
    menu.add.button('Play', start_game)
    menu.add.text_input('Name: ', default='Change this...')
    menu.add.selector('Difficulty: ', [('Hard', 1), ('Medium', 2), ('Easy', 3), ('Baby', 4)], onchange=set_difficulty)
    menu.add.selector('Color', [('Red', 1), ('Green', 2), ('Blue', 3), ('White', 4), ('Black', 5)], onchange=set_color)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(surface)


def get_move():
    global movement
    for i in pygame.event.get():
        if i.event == pygame.KEYDOWN:
            movement = True

        elif i.event == pygame.KEYUP:
            movement = False
def ball_launch():
    movement = True
    ball = ball_x_pos + 20
    


def start_game():
    global player_lenght, player, player_x_pos, current_color
    pygame.event.set_blocked(pygame.MOUSEMOTION)

    
    #barrier = pygame.rect(0, 0, 800, 534)
    #player.clamp_ip(barrier)

    while True:
        for event in pygame.event.get():
            get_move()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if keys[pygame.K_UP]:
                ball_launch()
                print('Up')

            if keys[pygame.K_DOWN]:
                player_lenght -= 20
                player = pygame.transform.scale(player, (player_lenght, 40))
                print('Down')


            if keys[pygame.K_ESCAPE]:
                exit()

        keys = pygame.key.get_pressed()

            
        if keys[pygame.K_LEFT]:
            player_x_pos -= 10
            if player_x_pos <= 0:
                player_x_pos = 1
            print('Left')


        if keys[pygame.K_RIGHT]:
            player_x_pos += 10
            if player_x_pos >= 770:
                player_x_pos = 770
            print('Right')

    
           


        surface.blit(hill, (0, 0))
        surface.blit(player, (player_x_pos, 400))   
        surface.blit(ball, (player_x_pos + 20, 380))
        pygame.display.update()
        clock.tick(60)


menu()


# player_lenght += 20
# player = pygame.transform.scale(player, (player_lenght, 40))