import pygame
import sys

pygame.init()

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
bigfont = pygame.font.Font(None, 80)
smallfont = pygame.font.Font(None, 45)

class GameObject:
    def __init__(self, width, height, speed):
        self.speed = speed
        self.width = width
        self.height = height
        self.pos = pygame.Rect(0, height, self.width, 20)
        self.color = (255, 255, 255)

    def move(self, direction=None, screen_width=640, screen_height=480):
        if direction == "left":
            self.pos.left -= self.speed
        elif direction == "right":
            self.pos.left += self.speed

        # Limit movement to boundaries of screen
        if self.pos.left < 0:
            self.pos.left = 0
        if self.pos.right > screen_width:
            self.pos.right = screen_width
        if self.pos.top < 0:
            self.pos.top = 0
        if self.pos.bottom > screen_height:
            self.pos.bottom = screen_height

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.pos)

class Ball:
    def __init__(self, x, y, speed_x, speed_y, radius):
        self.pos = pygame.Rect(x, y, radius * 2, radius * 2)
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.radius = radius
        self.color = (255, 0, 0)

    def move(self, paddle):
        self.pos.x += self.speed_x
        self.pos.y += self.speed_y

        # Bounce off walls
        if self.pos.left <= 0 or self.pos.right >= SCREEN_WIDTH:
            self.speed_x = -self.speed_x
        if self.pos.top <= 0:
            self.speed_y = -self.speed_y

        # Bounce off paddle
        if self.pos.colliderect(paddle.pos):
            self.speed_y = -self.speed_y
            self.speed_x += 0.3
            self.speed_y += - 1

        # bounce off objects
        for obj in game.objects:
            if self.pos.colliderect(obj.pos):
                self.speed_y = -self.speed_y
                
    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, self.pos)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.player = GameObject(100, 10, 5)
        self.player.pos = pygame.Rect(0, int(SCREEN_HEIGHT * 0.8), 100, 20)
        self.objects = []
        self.create_objects()

        self.ball = Ball(200, 200, 1, 1, 10)

    def create_objects(self):
        spacing = (SCREEN_WIDTH - 10 * 40) // (10 + 1)
        for x in range(10):
            o = GameObject(40, 10, 0)
            o.pos = pygame.Rect(spacing + x * (40 + spacing), 100, 40, 20)
            self.objects.append(o)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit()

    def update(self):
        keys = pygame.key.get_pressed()
        #if keys[pygame.K_UP]:
            #self.player.move("up", SCREEN_WIDTH, SCREEN_HEIGHT)
        #if keys[pygame.K_DOWN]:
           # self.player.move("down", SCREEN_WIDTH, SCREEN_HEIGHT)
        if keys[pygame.K_LEFT]:
            self.player.move("left", SCREEN_WIDTH, SCREEN_HEIGHT)
        if keys[pygame.K_RIGHT]:
            self.player.move("right", SCREEN_WIDTH, SCREEN_HEIGHT)

        self.ball.move(self.player)

        # Game over condition
        if self.ball.pos.bottom >= SCREEN_HEIGHT:
            print("Game Over!")
            self.play_again()
            pygame.time.wait(2000)
            sys.exit()

    def draw(self):
        self.screen.fill((0, 0, 0))
        for obj in self.objects:
            obj.draw(self.screen)
        self.player.draw(self.screen)
        self.ball.draw(self.screen)
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
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

game = Game()
game.run()
