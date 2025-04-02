import pygame
import sys
import random
import pygame_menu  # Import pygame_menu

pygame.init()

clock = pygame.time.Clock()
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen = pygame.image.load('Success-Story-KANAGWA-1.png')
bigfont = pygame.font.Font(None, 80)
smallfont = pygame.font.Font(None, 45)

# Global variables for menu settings, difficulty (initial speed of the ball), and ball color
difficulty = 2
ball_color = (255, 0, 0)

def set_difficulty(value, difficulty_level):
    global difficulty
    difficulty = difficulty_level

def set_color(value, color_index):
    global ball_color
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 255), (0, 0, 0)]
    ball_color = colors[color_index - 1]

def start_game():
    game = Game()
    game.run()

def menu():
    menu = pygame_menu.Menu('Welcome!', 400, 300, theme=pygame_menu.themes.THEME_BLUE)
    menu.add.button('Play', start_game)
    menu.add.text_input('Name: ', default='Change this...')
    menu.add.selector('Difficulty: ', [('Hard', 4), ('Medium', 3), ('Easy', 2), ('Baby', 1)], onchange=set_difficulty)
    menu.add.selector('Color', [('Red', 1), ('Green', 2), ('Blue', 3), ('White', 4), ('Black', 5)], onchange=set_color)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(surface)

class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, speed=0):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.mask = pygame.mask.from_surface(self.image)  # Create a mask for pixel-perfect collision

    def move(self, direction=None, screen_width=640):
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
        self.image = pygame.Surface((radius * 2, radius * 2))
        pygame.draw.ellipse(self.image, color, (0, 0, radius * 2, radius * 2))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.mask = pygame.mask.from_surface(self.image)  # Create a mask for pixel-perfect collision

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

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.player = GameObject(0, int(SCREEN_HEIGHT * 0.8), 100, 20, (255, 255, 255), 5)
        self.objects_group = pygame.sprite.Group()
        self.create_objects()

        # Use the selected ball color and difficulty
        self.ball = Ball(200, 200, difficulty, difficulty, 10, ball_color)

    def create_objects(self):
        spacing = (SCREEN_WIDTH - 10 * 40) // (10 + 1)
        for x in range(10):
            obj = GameObject(spacing + x * (40 + spacing), 100, 40, 20, (255, 255, 255))
            self.objects_group.add(obj)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit()

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move("left", SCREEN_WIDTH)
        if keys[pygame.K_RIGHT]:
            self.player.move("right", SCREEN_WIDTH)

        self.ball.move(self.player, self.objects_group)

        # Game over condition
        if self.ball.rect.bottom >= SCREEN_HEIGHT:
            print("Game Over!")
            self.play_again()
            pygame.time.wait(2000)
            sys.exit()

    def draw(self):
        surface.blit(screen, (-75, 0))
        self.objects_group.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        self.screen.blit(self.ball.image, self.ball.rect)
        pygame.display.update()

    def play_again(self):
        text = bigfont.render('Press R To Play Again', True, (0, 0, 0))
        textx = SCREEN_WIDTH / 2 - text.get_width() / 2
        texty = SCREEN_HEIGHT / 2 - text.get_height() / 2
        textx_size = text.get_width()
        texty_size = text.get_height()
        pygame.draw.rect(self.screen, (255, 255, 255), ((textx - 5, texty - 5),
                                                        (textx_size + 10, texty_size + 10)))
        self.screen.blit(text, (SCREEN_WIDTH / 2 - text.get_width() / 2,
                                SCREEN_HEIGHT / 2 - text.get_height() / 2))
        pygame.display.update()

        # Wait for the player to press R
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Restart the game
                        self.__init__()  # Reinitialize the game
                        self.run()  # Restart the game loop

    def run(self):
        while True:
            pygame.display.update()
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

# Start the menu
menu()
