import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BIG_FONT, SMALL_FONT, WHITE, BLACK
from game_objects import GameObject, Ball

class Game:
    def __init__(self, ball_color, difficulty):
        self.ball_color = ball_color  # Store ball_color
        self.difficulty = difficulty  # Store difficulty

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.player = GameObject(0, int(SCREEN_HEIGHT * 0.8), 100, 20, WHITE, 5)
        self.objects_group = pygame.sprite.Group()
        self.create_objects()

        # Use the selected ball color and difficulty
        self.ball = Ball(200, 200, difficulty, difficulty, 10, ball_color)

    def create_objects(self):
        spacing = (SCREEN_WIDTH - 10 * 40) // (10 + 1)
        for x in range(10):
            obj = GameObject(spacing + x * (40 + spacing), 100, 40, 20, WHITE)
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
        self.screen.fill(BLACK)
        self.objects_group.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        self.screen.blit(self.ball.image, self.ball.rect)
        pygame.display.update()

    def play_again(self):
        text = BIG_FONT.render('Press R To Play Again', True, BLACK)
        textx = SCREEN_WIDTH / 2 - text.get_width() / 2
        texty = SCREEN_HEIGHT / 2 - text.get_height() / 2
        pygame.draw.rect(self.screen, WHITE, ((textx - 5, texty - 5), (text.get_width() + 10, text.get_height() + 10)))
        self.screen.blit(text, (textx, texty))
        pygame.display.update()

        # Wait for the player to press R
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Restart the game
                        self.__init__(self.ball_color, self.difficulty)  # Reinitialize the game with stored values
                        self.run()  # Restart the game loop

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)