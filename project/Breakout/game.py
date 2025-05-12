import pygame
import sys
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BIG_FONT, SMALL_FONT, SMALL_SMALL_FONT, WHITE, BLACK, RED, GREEN, BLUE, break_block
from game_objects import GameObject, Ball, instruction, PowerUp
from maps import MAP_TEMPLATES, BLOCK_TYPES  
import os

class Game:
    def __init__(self, ball_color, difficulty, PLAYER1, PLAYER2):
        self.ball_color = ball_color  # Store ball_color
        self.difficulty = difficulty  # Store difficulty
        self.PLAYER1 = PLAYER1
        self.PLAYER2 = PLAYER2
        print(PLAYER1, PLAYER2)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.player1 = GameObject(120, int(SCREEN_HEIGHT * 0.8), 100, 20, BLUE, 5)
        self.objects_group = pygame.sprite.Group()
        self.player2 = GameObject(320, int(SCREEN_HEIGHT * 0.8), 100, 20, GREEN, 5)
        self.objects_group = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()

        self.level_index = 0
        self.map_templates = random.sample(MAP_TEMPLATES, len(MAP_TEMPLATES))
        self.load_map(self.map_templates[self.level_index])
        self.lives = 3  # 3 lives per stage

        pygame.joystick.init()
        self.joystick1 = None
        self.joystick2 = None
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()

        if pygame.joystick.get_count() > 1:
            self.joystick2 = pygame.joystick.Joystick(1)
            self.joystick2.init()


        # Use the selected ball color and difficulty
        self.balls = pygame.sprite.Group()
        ball = Ball(0, 0, 0, 0, 10, ball_color)
        self.balls.add(ball)
        self.ball_attached = True   #Ball starts waiting on paddle

        self.score = 0  # Initialize score for current run
        self.high_score = self.load_high_score() # Load high score from highscore.txt

        self.background = pygame.image.load("fire.png").convert()
        self.brick_sound = pygame.mixer.Sound('bricks.wav')
        self.bounce_sound = pygame.mixer.Sound('boing.wav')
        self.music = 'Pixel-Peeker-Polka.wav'
        pygame.mixer.music.load(self.music)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

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
                        x, y, 
                        block_width, 
                        block_height, 
                        block_type["color"],
                        durability=block_type.get("durability", 1),
                        modifiers={k: v for k, v in block_type.items() if k not in ["color", "durability"]}
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
        if self.score > self.high_score:
            self.high_score = self.score
            """Save the high score to a file."""
            with open("highscore.txt", "w") as file:
                file.write(str(self.high_score))

    def wait(self):
        text = SMALL_FONT.render('Paused, press UP KEY to continue', True, BLACK)
        textx = SCREEN_WIDTH / 2 - text.get_width() / 2
        texty = SCREEN_HEIGHT / 2 - text.get_height() / 2
        pygame.draw.rect(self.screen, WHITE, ((textx - 5, texty - 5), (text.get_width() + 10, text.get_height() + 10)))
        self.screen.blit(text, (textx, texty))
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:  # start the game
                        self.run()  # start the game loop
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Exit game
                        sys.exit()
                        

    def explode_blocks(self, center_block):
        cx, cy = center_block.rect.center
        max_dist_x = center_block.rect.width + 4
        max_dist_y = center_block.rect.height + 4

        # Only check nearby blocks
        nearby_blocks = [
            block for block in self.objects_group
            if abs(cx - block.rect.centerx) <= max_dist_x and abs(cy - block.rect.centery) <= max_dist_y
        ]

        for block in nearby_blocks:
            self.objects_group.remove(block)
            self.score += block.modifiers.get("score", 10)



    def enlarge_paddle(self):
        """Increase the paddle size."""
        self.player1.rect.width += 20
        self.player1.image = pygame.Surface((self.player1.rect.width, self.player1.rect.height))
        self.player1.image.fill(BLUE)
        self.player1.mask = pygame.mask.from_surface(self.player1.image)

        self.player2.rect.width += 20
        self.player2.image = pygame.Surface((self.player2.rect.width, self.player2.rect.height))
        self.player2.image.fill(GREEN)
        self.player2.mask = pygame.mask.from_surface(self.player2.image)

    def spawn_ball(self):
        """Spawn an additional ball."""
        if self.balls:  # Ensure there is at least one ball to reference
            reference_ball = self.balls[0]
            new_ball = Ball(
                reference_ball.rect.x, reference_ball.rect.y,  # Use the position of an existing ball
                random.choice([-3, 3]), random.choice([-3, 3]),  # Random speed
                10, self.ball_color
            )
            self.balls.add(new_ball)  # Add the new ball to the list of balls

    
    def instructions(self):
        """"""
    

    def update(self, PLAYER1, PLAYER2):
        self.balls.update()
        self.objects_group.update()
        self.powerups.update()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if self.player2.rect.left > self.player1.rect.right:
                self.player2.move("left", SCREEN_WIDTH)
        if keys[pygame.K_RIGHT]:
            self.player2.move("right", SCREEN_WIDTH)

        if keys[pygame.K_a]:
            self.player1.move("left", SCREEN_WIDTH)
        if keys[pygame.K_d]:
            if self.player1.rect.right < self.player2.rect.left:
                self.player1.move("right", SCREEN_WIDTH)        
        
        if keys[pygame.K_SPACE]:
            self.wait()

        if pygame.joystick.get_count() > 0:
        # Controller movement Player 1
            if self.joystick:
                axis_x = self.joystick.get_axis(0)  # D-pad left/right
                if axis_x < -0.5:
                    self.player1.move("left", SCREEN_WIDTH)
                elif axis_x > 0.5:
                    if self.player1.rect.right < self.player2.rect.left:
                        self.player1.move("right", SCREEN_WIDTH)

            # Shoot with Triangle
            if self.ball_attached and self.joystick.get_button(0):  
                self.ball_attached = False
                self.instructions = False
                for ball in self.balls:
                    ball.speed_x = self.difficulty
                    ball.speed_y = -self.difficulty

        # Controller movement for player 2
            if self.joystick2:
                axis_x2 = self.joystick2.get_axis(0)
                if axis_x2 < -0.5:
                    if self.player1.rect.right < self.player2.rect.left:
                        self.player2.move("left", SCREEN_WIDTH)
                if axis_x2 > 0.5: self.player2.move("right", SCREEN_WIDTH)

        if self.ball_attached:
            for ball in self.balls:
                ball.rect.midbottom = (self.player1.rect.centerx, self.player1.rect.top - 1)

            
            if keys[pygame.K_w]:
                self.ball_attached = False # Shoot the ball
                self.instructions = False
                for ball in self.balls:
                    ball.speed_x = self.difficulty
                    ball.speed_y = -self.difficulty
                    

        new_balls = pygame.sprite.Group()
        for ball in self.balls:
            # Pass both Player 1 and Player 2 paddles to the move method
            spawned_ball = ball.move(self.player1, self.player2, self.objects_group)
            if spawned_ball:
                new_balls.add(spawned_ball)

        self.balls.add(new_balls)

        for ball in self.balls:
            if pygame.sprite.collide_mask(ball, self.player2):
                ball.speed_y = -ball.speed_y  # Ball bounces off player2
                ball.speed_x += random.uniform(0.2, 0.8)  # Add some randomness to the bounce
                ball.speed_y += random.uniform(-0.8, -0.2)
                if not pygame.mixer.Channel(1).get_busy():
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound('boing.wav'), maxtime=600)

            collided_objects = pygame.sprite.spritecollide(ball, self.objects_group, False, pygame.sprite.collide_mask)
            for block in collided_objects:
                if hasattr(block, "durability"):
                    block.durability -= 1
                    if block.durability <= 0:
                        score_gain = block.modifiers.get("score", 10)
                        self.score += score_gain

                        # Drop a power-up for some effects
                        effect = block.modifiers.get("effect")
                        if effect in ["paddle_enlarge", "spawn_ball"]:
                            powerup = PowerUp(block.rect.x, block.rect.y, effect, color=block.base_color)
                            self.powerups.add(powerup)
                        elif effect == "explosive":
                            self.explode_blocks(block)
                        effect = block.modifiers.get("effect")

                        self.objects_group.remove(block)
                        pygame.mixer.Channel(0).play(pygame.mixer.Sound('bricks.wav'), maxtime=600)
                    else:
                        block.update_appearance()
                if abs(ball.rect.bottom - block.rect.top) < 10 and ball.speed_y > 0:
                    ball.speed_y = -abs(ball.speed_y) # hitting the block from above
                elif abs(ball.rect.top - block.rect.bottom) < 10 and ball.speed_y < 0:
                    ball.speed_y = abs(ball.speed_y) # hitting from below
                elif abs(ball.rect.right - block.rect.left) < 10 and ball.speed_x > 0:
                    ball.speed_x = abs(ball.speed_x) # hitting the left side
                elif abs(ball.rect.left - block.rect.right) < 10 and ball.speed_x < 0:
                    ball.speed_x = abs(ball.speed_x) # hitting the right side
                else:
                    # Fallback if funkyness
                    ball.speed_y = -ball.speed_y
                
            self.powerups.update()

            for powerup in list(self.powerups):
                if pygame.sprite.collide_mask(powerup, self.player1) or pygame.sprite.collide_mask(powerup, self.player2):
                    if powerup.effect == "paddle_enlarge":
                        self.enlarge_paddle()
                    elif powerup.effect == "spawn_ball":
                        new_ball = Ball(powerup.rect.centerx, powerup.rect.centery, random.choice([-3, 3]), -3, 10, self.ball_color)
                        self.balls.add(new_ball)
                    self.powerups.remove(powerup)

        for ball in list(self.balls):
            if ball.rect.bottom >= SCREEN_HEIGHT:
                self.balls.remove(ball)

        if len(self.balls) == 0:
            self.lives -= 1
            if self.lives > 0:
                self.balls = pygame.sprite.Group()
                self.balls.add(Ball(0, 0, 0, 0, 10, self.ball_color))
                self.ball_attached = True
            else:
                print("Game Over!")
                self.save_high_score()
                self.play_again()
                pygame.time.wait(2000)
                sys.exit()

        if not self.objects_group: # no blocks left
            self.level_index += 1
            if self.level_index < len(self.map_templates):
                self.powerups.empty()
                self.load_map(self.map_templates[self.level_index])
                self.player1.rect.width = 100
                self.player1.image = pygame.Surface((self.player1.rect.width, self.player1.rect.height))
                self.player1.image.fill(BLUE)
                self.player2.rect.width = 100
                self.player2.image = pygame.Surface((self.player2.rect.width, self.player2.rect.height))
                self.player2.image.fill(GREEN)
                self.balls = pygame.sprite.Group()
                self.balls.add(Ball(0, 0, 0, 0, 10, self.ball_color))
                self.ball_attached = True
            else:
                print("You completed all levels!")
                self.save_high_score()
                self.play_again()
                return
    

    def draw(self, PLAYER1, PLAYER2):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (0, 50))
        self.objects_group.draw(self.screen)
        self.screen.blit(self.player1.image, self.player1.rect)
        player1name = SMALL_SMALL_FONT.render(f"{PLAYER1}", True, WHITE)
        self.screen.blit(player1name, (self.player1.rect.topleft, self.player1.rect.bottomright))
        self.screen.blit(self.player2.image, self.player2.rect)
        player2name = SMALL_SMALL_FONT.render(f"{PLAYER2}", True, BLACK)
        self.screen.blit(player2name, (self.player2.rect.topleft, self.player2.rect.bottomright))
        self.balls.draw(self.screen)
        self.powerups.draw(self.screen)

        if self.instructions:
            instruction.instructions(self.screen)

        # Display current lives
        # For black outline, prints the text in black 4 times slightly shifted
        lives_text = SMALL_SMALL_FONT.render(f"Lives: {self.lives}", True, BLACK)
        self.screen.blit(lives_text, (9, 39))
        self.screen.blit(lives_text, (9, 41))
        self.screen.blit(lives_text, (11, 39))
        self.screen.blit(lives_text, (11, 41))
        # "real" text
        lives_text = SMALL_SMALL_FONT.render(f"Lives: {self.lives}", True, RED)
        self.screen.blit(lives_text, (10, 40))

        # Display the current score
        # Outline
        score_text = SMALL_SMALL_FONT.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (9, 9))
        self.screen.blit(score_text, (9, 11))
        self.screen.blit(score_text, (11, 9))
        self.screen.blit(score_text, (11, 11))
        # Real text
        score_text = SMALL_SMALL_FONT.render(f"Score: {self.score}", True, GREEN)
        self.screen.blit(score_text, (10, 10))  # Position at the top-left corner

        # Display the high score
        # Outline
        high_score_text = SMALL_SMALL_FONT.render(f"High Score: {self.high_score}", True, BLACK)
        self.screen.blit(high_score_text, (9, 24))
        self.screen.blit(high_score_text, (9, 26))
        self.screen.blit(high_score_text, (11, 24))
        self.screen.blit(high_score_text, (11, 26))
        # Real text
        high_score_text = SMALL_SMALL_FONT.render(f"High Score: {self.high_score}", True, GREEN)
        self.screen.blit(high_score_text, (10, 25))  # Position below the score
        
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
                        self.level_index = 0 # reset to first level
                        self.__init__(self.ball_color, self.difficulty, self.PLAYER1, self.PLAYER2)  # Reinitialize the game with stored values
                        self.run()  # Restart the game loop
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()

    def run(self):
        instruction()
        while True:
            self.handle_events()
            self.update(self.PLAYER1 ,self.PLAYER2)
            self.draw(self.PLAYER1, self.PLAYER2)
            self.clock.tick(60)

