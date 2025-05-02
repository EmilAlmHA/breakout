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

        # Bounce off walls
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed_x = -self.speed_x
        if self.rect.top <= 0:
            self.speed_y = -self.speed_y

        # Bounce off paddle
        if pygame.sprite.collide_mask(self, paddle):
            self.speed_y = -self.speed_y
            self.speed_x += random.uniform(0.2, 0.8)
            self.speed_y += random.uniform(-0.8, -0.2)
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('boing.wav'), maxtime=600)


