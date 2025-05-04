import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, bounce_paddel

class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, speed=0, durability=1, modifiers=None):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.durability = durability
        self.mask = pygame.mask.from_surface(self.image)

        self.color = color
        self.base_color = color
        self.modifiers = modifiers or {}

        if self.durability is not None:
            self.update_appearance()
        else:
            self.image.fill(color)


    def update_appearance(self):
        # Reverse the brightness: higher durability = darker
        max_durability = 3  # Adjust this if your blocks can go higher
        darkness_factor = max(0.3, 1 - (self.durability - 1) / (max_durability - 1))
        faded_color = tuple(int(c * darkness_factor) for c in self.base_color)
        self.image.fill(faded_color)


    def move(self, direction=None, screen_width=SCREEN_WIDTH):
        if direction == "left":
            self.rect.x -= self.speed
        elif direction == "right":
            self.rect.x += self.speed

        # Limit movement to screen boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, speed_x, speed_y, radius, color):
        super().__init__()
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, color, (0, 0, radius * 2, radius * 2))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.mask = pygame.mask.from_surface(self.image)

    def move(self, paddle, objects_group):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.speed_x == 0 and self.speed_y == 0:
            return

        # Bounce off walls
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed_x = -self.speed_x
        if self.rect.top <= 0:
            self.speed_y = -self.speed_y

        # Bounce off paddle
        if pygame.sprite.collide_mask(self, paddle):
            # Calculate hit position: distance from paddle center (normalized -1 to 1)
            hit_pos = (self.rect.centerx - paddle.rect.centerx) / (paddle.rect.width / 2)
            self.speed_y = -abs(self.speed_y)
            # Adjust X velocity based on where the ball hit the paddle
            self.speed_x = hit_pos * 5  # Tweak multiplier for difficulty
            self.speed_y += random.uniform(-0.5, -0.2)  
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('boing.wav'), maxtime=600)

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, effect, color=(255, 255, 0)):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.effect = effect
        self.speed = 2
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.y += self.speed

class instruction:
    def instructions(surface):
        white = (255, 255, 255)
        black = (0, 0, 0)
        
        
        font = pygame.font.Font('freesansbold.ttf', 24)
        text = font.render('Blue: A and D for movement,', True, white)
        text1 = font.render('W to shoot ball', True, white)
        text2 = font.render('Green: Left and Right arrow for movement', True, white)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2.75, SCREEN_HEIGHT // 2)
        textRect1 = text.get_rect()
        textRect1.center = (SCREEN_WIDTH // 2.75, SCREEN_HEIGHT // 1.65)
        textRect2 = text.get_rect()
        textRect2.center = (SCREEN_WIDTH // 2.75, SCREEN_HEIGHT // 1.4)
            

        surface.blit(text, textRect)
        surface.blit(text1, textRect1)
        surface.blit(text2, textRect2)
            
        pygame.display.update()