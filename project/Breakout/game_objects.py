import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, speed=0):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.mask = pygame.mask.from_surface(self.image)

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

        # Bounce off objects
        collided_objects = pygame.sprite.spritecollide(self, objects_group, True, pygame.sprite.collide_mask)
        if collided_objects:
            self.speed_y = -self.speed_y

