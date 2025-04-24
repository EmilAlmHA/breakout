import pygame
import sys
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BIG_FONT, SMALL_FONT, WHITE, BLACK
from game_objects import GameObject, Ball
from maps import MAP_TEMPLATE, BLOCK_TYPES  # Ensure BLOCK_TYPES is defined in maps.py
import pygame_menu
import os

global pause 
pause = False

class Game:
    def __init__(self, ball_color, difficulty):
        self.ball_color = ball_color  # Store ball_color
        self.difficulty = difficulty  # Store difficulty

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.player = GameObject(320, int(SCREEN_HEIGHT * 0.8), 100, 20, WHITE, 5)
        self.objects_group = pygame.sprite.Group()

        # Load the map template
        self.load_map(MAP_TEMPLATE)

        # Use the selected ball color and difficulty
        self.ball = Ball(200, 200, difficulty, difficulty, 10, ball_color)

        self.score = 0 # Initialize score for current run
        self.high_score = self.load_high_score() # Load high score from highscore.txt

    def load_map(self, template):
        # Generate blocks based on the map template.
        block_width = SCREEN_WIDTH // len(template[0])  # Calculate block width
        block_height = 20  # Fixed block height

        for row_index, row in enumerate(template):
            for col_index, cell in enumerate(row):
                if cell == -1:  # Random block
                    cell = random.choice(list(BLOCK_TYPES.keys()))  # Randomly choose a block type
                if cell in BLOCK_TYPES:  # If the cell represents a valid block type
                    block_type = BLOCK_TYPES[cell]
                    x = col_index * block_width
                    y = row_index * block_height
                    block = GameObject(
                        x, y, block_width, block_height, block_type["color"]
                    )
                    self.objects_group.add(block)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit()

    def load_high_score(self):
        """Load the high score from a file."""
        if os.path.exists("highscore.txt"):
            with open("highscore.txt", "r") as file:
                return int(file.read())
        return 0

    def save_high_score(self):
        """Save the high score to a file."""
        with open("highscore.txt", "w") as file:
            file.write(str(self.high_score))

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move("left", SCREEN_WIDTH)
        if keys[pygame.K_RIGHT]:
            self.player.move("right", SCREEN_WIDTH)
        """if keys[pygame.K_SPACE]:
            pause = True
            Paused()"""

        self.ball.move(self.player, self.objects_group)

         # Check for collisions with blocks
        collided_objects = pygame.sprite.spritecollide(self.ball, self.objects_group, True, pygame.sprite.collide_mask)
        if collided_objects:
            self.score += len(collided_objects) * 10  # Increment score by 10 per block destroyed
            print(f"Score updated: {self.score}")  # Debugging output to verify score updates
            if self.score > self.high_score:
                self.high_score = self.score  # Update high score if necessary

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
        # Display the current score
        score_text = SMALL_FONT.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))  # Position at the top-left corner

        # Display the high score
        high_score_text = SMALL_FONT.render(f"High Score: {self.high_score}", True, WHITE)
        self.screen.blit(high_score_text, (10, 50))  # Position below the score
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
    
    """def Paused(self, ball_color):
        menu = pygame_menu.Menu('Paused', 400, 300, theme=pygame_menu.themes.THEME_BLUE)

        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

        menu.add.button("Continue", 150, 450, 100, 50, (0,255,0), (0,125,0), unpause)
        menu.add.button('Quit', pygame_menu.events.EXIT)
        pygame.display.update()
        
        """
