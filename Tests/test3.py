import pygame
import pygame_menu
import os

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
ball_image = pygame.transform.scale(ball_image, (14, 14))
ball_x_pos = 300
ball_y_pos = 400

def draw_window(player1, player2):
    surface.fill((255, 0 , 0))
    surface.blit(background_image, (0, 0))
    surface.blit(player_image1, (player1.x, player1.y))
    surface.blit(player_image2, (player2.x, player2.y))
    pygame.display.update()



def main():
    global player_x_pos, player_y_pos, player_height, player_lenght
    player1 = pygame.Rect(player1_x_pos, player1_y_pos, player_lenght, player_height) 
    player2 = pygame.Rect(player2_x_pos, player2_y_pos, player_lenght, player_height) 
    running = True
    while running:
        
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            
        
        draw_window(player1, player2)
        


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
            if player1.x  >= 770:
                player1.x  = 770
            print('Right')

        if keys[pygame.K_a]:
            player2.x -= 10
            if player2.x  <= 0:
                player2.x  = 1
            print('Left')


        if keys[pygame.K_d]:
            player2.x  += 10
            if player2.x  >= 770:
                player2.x  = 770
            print('Right')

    pygame.quit()

if __name__ == "__main__":
    main()