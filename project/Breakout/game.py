import asyncio
import random

import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BIG_FONT, SMALL_FONT, SMALL_SMALL_FONT, WHITE, BLACK, RED, GREEN, BLUE
from game_objects import GameObject, Ball, instruction, PowerUp, ExplosionEffect
from maps import MAP_TEMPLATES, BLOCK_TYPES
import os

class Game:
    def __init__(self, ball_color, difficulty, players, PLAYER1, PLAYER2):
        self.ball_color = ball_color  # Store ball_color
        self.difficulty = difficulty  # Store difficulty
        if (players == 1):
            self.PLAYER1 = PLAYER1
            self.PLAYER2 = PLAYER2
        else:
            self.PLAYER1 = PLAYER1
            self.PLAYER2 = PLAYER2
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        if(players == 1):
            self.player1 = GameObject(250, int(SCREEN_HEIGHT * 0.8), 150, 20, BLUE, 5)
            self.objects_group = pygame.sprite.Group()
            self.player2 = GameObject(520000, int(SCREEN_HEIGHT * 0.8), 100, 20, GREEN, 5)
        else:
            self.player1 = GameObject(120, int(SCREEN_HEIGHT * 0.8), 100, 20, BLUE, 5)
            self.objects_group = pygame.sprite.Group()
            self.player2 = GameObject(320, int(SCREEN_HEIGHT * 0.8), 100, 20, GREEN, 5)
            self.objects_group = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.explosions = []

        self.instructions = True
        self.level_index = 0
        self.map_templates = random.sample(MAP_TEMPLATES, len(MAP_TEMPLATES))
        self.load_map(self.map_templates[self.level_index])
        self.lives = 3  # 3 lives per stage

        pygame.joystick.init()
        self.joystick1 = None
        self.joystick2 = None
        if pygame.joystick.get_count() > 0:
            self.joystick1 = pygame.joystick.Joystick(0)
            self.joystick1.init()

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
        self.brick_sound = pygame.mixer.Sound('bricks.ogg')
        self.bounce_sound = pygame.mixer.Sound('boing.ogg')
        self.music = 'Pixel-Peeker-Polka.ogg'
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

    def _draw_center_message(self, message, font=None):
        font = font or SMALL_FONT
        text = font.render(message, True, BLACK)
        textx = SCREEN_WIDTH / 2 - text.get_width() / 2
        texty = SCREEN_HEIGHT / 2 - text.get_height() / 2
        pygame.draw.rect(self.screen, WHITE, ((textx - 5, texty - 5), (text.get_width() + 10, text.get_height() + 10)))
        self.screen.blit(text, (textx, texty))
        pygame.display.update()

    def explode_blocks(self, center_block):
        cx, cy = center_block.rect.center
        bw = center_block.rect.width + 4
        bh = center_block.rect.height + 4

        to_remove = [
        block for block in list(self.objects_group)
        if abs(cx - block.rect.centerx) <= bw and abs(cy - block.rect.centery) <= bh
        ]

        for block in to_remove:
            self.explosions.append(ExplosionEffect(block.rect.topleft, block.rect.size))

            effect = block.modifiers.get("effect")
            if effect == "explosive" and block != center_block:
                self.explode_blocks(block)  # Chain reaction
            self.score += block.modifiers.get("score", 10)
            self.objects_group.remove(block)
            pygame.mixer.Channel(0).play(self.brick_sound, maxtime=600)

    def trigger_powerup(self, block):
        """Trigger the power-up effect of a block, if it has one."""
        effect = block.modifiers.get("effect")

        if effect == "explosive":
            return

        if effect:
            powerup = PowerUp(block.rect.x, block.rect.y, effect, color=block.base_color)
            self.powerups.add(powerup)


    def enlarge_paddle(self, players):
        """Increase the paddle size."""
        if(players == 1):
            self.player1.rect.width += 50
            self.player1.image = pygame.Surface((self.player1.rect.width, self.player1.rect.height))
            self.player1.image.fill(BLUE)
            self.player1.mask = pygame.mask.from_surface(self.player1.image)

        else:
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


    def update(self, PLAYER1, PLAYER2, players):
        """Kor en bildrutas spellogik. Returnerar None som vanligt, eller
        "gameover"/"won" nar omgangen ska ta slut, sa att run() (i stallet
        for sys.exit()/rekursiva self.run()-anrop, vilket blockerar webblasaren)
        kan visa ett meddelande och vanta pa R utan att avsluta processen.
        """
        self.balls.update()
        self.objects_group.update()
        self.powerups.update()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if self.player2.rect.left > self.player1.rect.right:
                if (players == 1):
                    self.player2.move("left", SCREEN_WIDTH + 10000)
                else:
                    self.player2.move("left", SCREEN_WIDTH)
        if keys[pygame.K_RIGHT]:
            if (players == 1):
                self.player2.move("right", SCREEN_WIDTH + 10000)
            else:
                self.player2.move("right", SCREEN_WIDTH)

        if keys[pygame.K_a]:
            self.player1.move("left", SCREEN_WIDTH)
        if keys[pygame.K_d]:
            if self.player1.rect.right < self.player2.rect.left:
                self.player1.move("right", SCREEN_WIDTH)

        if pygame.joystick.get_count() > 0:
        # Controller movement Player 1
            if self.joystick1:
                axis_x = self.joystick1.get_axis(0)  # D-pad left/right
                if axis_x < -0.5:
                    self.player1.move("left", SCREEN_WIDTH)
                elif axis_x > 0.5:
                    if self.player1.rect.right < self.player2.rect.left:
                        self.player1.move("right", SCREEN_WIDTH)
            # Shoot with Triangle
            if self.ball_attached and self.joystick1.get_button(0):
                self.ball_attached = False
                self.instructions = False
                for ball in self.balls:
                    ball.speed_x = self.difficulty
                    ball.speed_y = -self.difficulty

        # Controller movement for player 2
            if self.joystick2:
                axis_x2 = self.joystick2.get_axis(0)
                if(players == 1):
                    if axis_x2 < -0.5:
                        if self.player1.rect.right < self.player2.rect.left:
                            self.player2.move("left", SCREEN_WIDTH + 10000)
                    if axis_x2 > 0.5:
                        self.player2.move("right", SCREEN_WIDTH + 10000)

                elif(players == 2):
                    if axis_x2 < -0.5:
                        if self.player1.rect.right < self.player2.rect.left:
                            self.player2.move("left", SCREEN_WIDTH)
                    elif axis_x2 > 0.5:
                        self.player2.move("right", SCREEN_WIDTH)

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
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound('boing.ogg'), maxtime=600)

            collided_objects = pygame.sprite.spritecollide(ball, self.objects_group, False, pygame.sprite.collide_mask)
            for block in collided_objects:
                if hasattr(block, "durability"):
                    block.durability -= 1
                    if block.durability <= 0:
                        if block.modifiers.get("effect") == "explosive":
                            self.explode_blocks(block)
                        self.trigger_powerup(block)  # Trigger the power-up before removing the block
                        self.objects_group.remove(block)
                        self.score += block.modifiers.get("score", 10)
                        pygame.mixer.Channel(0).play(self.brick_sound, maxtime=600)
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
                        self.enlarge_paddle(players)
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
                self.save_high_score()
                return "gameover"

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
                self.save_high_score()
                return "won"

        return None


    def draw(self, PLAYER1, PLAYER2, players):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (0, 50))
        self.objects_group.draw(self.screen)
        if(players == 1):
            self.screen.blit(self.player1.image, self.player1.rect)
            player1name = SMALL_SMALL_FONT.render(f"{PLAYER1}", True, WHITE)
            self.screen.blit(player1name, (self.player1.rect.topleft, self.player1.rect.bottomright))
        else:
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

        for explosion in self.explosions[:]:
            if not explosion.draw(self.screen):
                self.explosions.remove(explosion)

        pygame.display.update()

    async def run(self, players):
        """Webbversion av spelloopen. Original-koden hade tre olika blockerande
        while-loopar (spelloop, paus-loop i wait(), game-over-loop i play_again())
        som anropade varandra rekursivt och avslutade processen med sys.exit().
        Ingetdera funkar i en webblasare: en enda loop som "await asyncio.sleep(0)"
        varje bildruta kravs, sa allt ar hopslaget till EN loop med ett litet
        tillstand (paused/game_over_message) istallet.
        """
        paused = False
        game_over_message = None

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    if game_over_message and event.key == pygame.K_r:
                        self.level_index = 0
                        self.lives = 3
                        self.score = 0
                        self.map_templates = random.sample(MAP_TEMPLATES, len(MAP_TEMPLATES))
                        self.objects_group = pygame.sprite.Group()
                        self.load_map(self.map_templates[self.level_index])
                        self.balls = pygame.sprite.Group()
                        self.balls.add(Ball(0, 0, 0, 0, 10, self.ball_color))
                        self.ball_attached = True
                        game_over_message = None
                    elif paused and event.key == pygame.K_UP:
                        paused = False

            keys = pygame.key.get_pressed()
            if not game_over_message:
                if keys[pygame.K_SPACE]:
                    paused = True
                if not paused:
                    result = self.update(self.PLAYER1, self.PLAYER2, players)
                    if result:
                        game_over_message = (
                            'You completed all levels!' if result == 'won' else 'Game Over!'
                        )

            self.draw(self.PLAYER1, self.PLAYER2, players)

            if paused:
                self._draw_center_message('Paused, press UP KEY to continue')
            elif game_over_message:
                self._draw_center_message(f'{game_over_message} Press R To Play Again', BIG_FONT)

            self.clock.tick(60)
            await asyncio.sleep(0)
