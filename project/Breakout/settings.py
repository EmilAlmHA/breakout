import pygame

# Screen dimensions
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# Colors
BALL_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 255), (0, 0, 0)]
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Fonts
pygame.init()
BIG_FONT = pygame.font.Font(None, 80)
SMALL_FONT = pygame.font.Font(None, 45)
SMALL_SMALL_FONT = pygame.font.Font(None, 20)

#Sounds
bounce_paddel = pygame.mixer.Sound("boing.ogg")
bounce_paddel.set_volume(0.4)

#break_block = pygame.mixer.Sound("breaking-a-vase.wav")

#Name
PLAYER1 = SMALL_SMALL_FONT, BLACK
PLAYER2 = SMALL_SMALL_FONT, BLACK