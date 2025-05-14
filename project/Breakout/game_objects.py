import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, bounce_paddel

class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, speed=0, durability=1, modifiers=None):
        super().__init__()
        self.image = pygame.Surface((width - 1, height - 1))
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

        # Add a symbol if the block has a power-up effect
        if "effect" in self.modifiers:
            self.add_symbol(self.modifiers["effect"])

    def update_appearance(self):
        # Reverse the brightness: higher durability = darker
        max_durability = 3  # Adjust this if your blocks can go higher
        darkness_factor = max(0.3, 1 - (self.durability - 1) / (max_durability - 1))
        faded_color = tuple(int(c * darkness_factor) for c in self.base_color)
        self.image.fill(faded_color)

    def add_symbol(self, effect):
        """Add a symbol to the block based on its effect."""
        font = pygame.font.Font(None, 14)  # Adjust font size as needed
        symbol = ""
        if effect == "paddle_enlarge":
            symbol = "L"  # L for Enlarge
        elif effect == "spawn_ball":
            symbol = "B"  # B for Ball
        elif effect == "explosive":
            symbol = "E"  # E for Explosive

        text = font.render(symbol, True, (0, 0, 0))  # Black text
        text_rect = text.get_rect(center=(self.image.get_width() // 2, self.image.get_height() // 2))
        self.image.blit(text, text_rect)

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
        self.bounce_sound = pygame.mixer.Sound('boing.wav')  # Load sound once

    def move(self, paddle1, paddle2, objects_group):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.speed_x == 0 and self.speed_y == 0:
            return

        # Bounce off walls
        if self.rect.left <= 0:
            self.rect.left = 0  # Ensure the ball stays within the left boundary
            self.speed_x = -self.speed_x
        elif self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH  # Ensure the ball stays within the right boundary
            self.speed_x = -self.speed_x

        if self.rect.top <= 0:
            self.rect.top = 0  # Ensure the ball stays within the top boundary
            self.speed_y = -self.speed_y

        # Bounce off Player 1 paddle
        if pygame.sprite.collide_mask(self, paddle1):
            self.handle_paddle_collision(paddle1)

        # Bounce off Player 2 paddle
        if pygame.sprite.collide_mask(self, paddle2):
            self.handle_paddle_collision(paddle2)

    def handle_paddle_collision(self, paddle):
        """Handle collision with a paddle."""
        if self.rect.bottom > paddle.rect.top:
            self.rect.bottom = paddle.rect.top

        # Calculate normalized hit position (-1.0 to 1.0)
        hit_pos = (self.rect.centerx - paddle.rect.centerx) / (paddle.rect.width / 2)

        # Base bounce: upward and angled based on hit position
        base_speed = max(abs(self.speed_x), abs(self.speed_y))

        # Apply speed increase
        speed_gain = 0.3  # You can adjust this
        new_speed = base_speed + speed_gain

        # Direction determined by hit_pos
        self.speed_x = hit_pos * new_speed
        self.speed_x = max(-10, min(10, self.speed_x))  # Clamp for control

        self.speed_y = -abs(new_speed)  # Always bounce upward with new speed

        # Optional vertical variation
        self.speed_y += random.uniform(-0.3, -0.1)


        # Play bounce sound
        pygame.mixer.Channel(1).play(self.bounce_sound, maxtime=600)


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, effect, color=(255, 255, 0)):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.effect = effect
        self.speed = 1
        self.mask = pygame.mask.from_surface(self.image)

        # Add a symbol to the power-up
        self.add_symbol(effect)

    def add_symbol(self, effect):
        """Add a symbol to the power-up based on its effect."""
        font = pygame.font.Font(None, 12)  # Adjust font size as needed
        symbol = ""
        if effect == "paddle_enlarge":
            symbol = "L"  # L for Enlarge
        elif effect == "spawn_ball":
            symbol = "B"  # B for Ball
        elif effect == "explosive":
            symbol = "E"  # E for Explosive

        text = font.render(symbol, True, (0, 0, 0))  # Black text
        text_rect = text.get_rect(center=(self.image.get_width() // 2, self.image.get_height() // 2))
        self.image.blit(text, text_rect)

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
        text3 = font.render('Controller: Left and Right, P1 Triangle to shoot', True, white)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2.75, SCREEN_HEIGHT // 2)
        textRect1 = text.get_rect()
        textRect1.center = (SCREEN_WIDTH // 2.75, SCREEN_HEIGHT // 1.65)
        textRect2 = text.get_rect()
        textRect2.center = (SCREEN_WIDTH // 2.75, SCREEN_HEIGHT // 1.4)
        textRect3 = text.get_rect()
        textRect3.center = (SCREEN_WIDTH // 2.75, SCREEN_HEIGHT // 1.15)
            

        surface.blit(text, textRect)
        surface.blit(text1, textRect1)
        surface.blit(text2, textRect2)
        surface.blit(text3, textRect3)
            
        pygame.display.update()

class ExplosionEffect:
    def __init__(self, pos, size, lifetime=200):
        self.rect = pygame.Rect(pos, size)
        self.color = (255, 100, 0)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = lifetime

    def draw(self, surface):
        elapsed = pygame.time.get_ticks() - self.start_time
        if elapsed > self.lifetime:
            return False
        alpha = max(0, 255 - int(255 * (elapsed / self.lifetime)))

        temp_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        temp_surface.fill((*self.color, alpha))
        surface.blit(temp_surface, self.rect.topleft)
        return True