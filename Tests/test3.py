import pygame
import sys
import pygame_menu
import os

pygame.init()

clock = pygame.time.Clock()
WIDTH = 800
HEIGHT = 534
surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Test 3!")

background_image = pygame.image.load(os.path.join('Tests', 'Success-Story-KANAGWA-1.png'))

player_image1 = pygame.image.load(os.path.join('Tests', 'longcat90.jpg'))
player_image2 = pygame.image.load(os.path.join('Tests', 'longcat90.jpg'))
player_lenght, player_height = 200, 50
player_image1 = pygame.transform.scale(player_image1, (player_height, player_lenght))
player_image1 = pygame.transform.rotate(player_image1, (90))
player_image2 = pygame.transform.scale(player_image2, (player_height, player_lenght))
player_image2 = pygame.transform.rotate(player_image2, (270))
player1_x_pos = 150
player1_y_pos = 50
player2_x_pos = 450
player2_y_pos = 50

ball_image = pygame.image.load(os.path.join('Tests', 'volleyball-ball.png'))
ball_length, ball_height = 14, 14
ball_image = pygame.transform.scale(ball_image, (ball_length, ball_height))
ball_x_pos = 400
ball_y_pos = 100

def set_difficulty( difficulty_level):
    global difficulty
    difficulty = difficulty_level

def set_color(color_index):
    global ball_color
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 255), (0, 0, 0)]
    ball_color = colors[color_index - 1]

def draw_window(player1, player2, ball):
    surface.fill((255, 0 , 0))
    surface.blit(background_image, (0, 0))
    surface.blit(player_image1, (player1.x, player1.y))
    surface.blit(player_image2, (player2.x, player2.y))
    surface.blit(ball_image, (ball.x, ball.y))
    pygame.display.update()



def main():
    global player_x_pos, player_y_pos, player_height, player_lenght, ball_x_pos, ball_y_pos, ball_height, ball_length
    player1 = pygame.Rect(player1_x_pos, player1_y_pos, player_lenght, player_height) 
    player2 = pygame.Rect(player2_x_pos, player2_y_pos, player_lenght, player_height) 
    ball = pygame.Rect(ball_x_pos, ball_y_pos, ball_length, ball_height)
    running = True
    while running:
        
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            
        
        draw_window(player1, player2, ball)
        


        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
                exit()
            
        if keys[pygame.K_LEFT]:
            player1.x -= 10
            if player1.x  <= 0:
                player1.x  = 1
            print('Left')


        if keys[pygame.K_RIGHT]:
            player1.x  += 10
            if player1.x + player_lenght >= WIDTH:
                player1.x  = WIDTH - player_lenght
            print('Right')

        if keys[pygame.K_a]:
            player2.x -= 10
            if player2.x  <= 0:
                player2.x  = 1
            print('Left')


        if keys[pygame.K_d]:
            player2.x  += 10
            if player2.x + player_lenght >= WIDTH:
                player2.x  = WIDTH - player_lenght
            print('Right')

    pygame.quit()

def menu():
    menu = pygame_menu.Menu('Welcome!', 400, 300, theme=pygame_menu.themes.THEME_BLUE)
    menu.add.button('Play', main)
    menu.add.text_input('Name: ', default='Change this...')
    menu.add.selector('Difficulty: ', [('Hard', 4), ('Medium', 3), ('Easy', 2), ('Baby', 1)], onchange=set_difficulty)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(surface)


menu()