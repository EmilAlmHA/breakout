import pygame
import sys

class GameObject:
    def __init__(self, width, height, speed):
        self.speed = speed
        self.width = width
        self.height = height
        self.pos = pygame.Rect(0, height, self.width, 20)  # Balken är 20 pixlar hög
        self.color = (255, 255, 255)  # Vit färg för balken

    def move(self, direction=None):
        if direction == "up":
            self.pos.top -= self.speed
        elif direction == "down":
            self.pos.top += self.speed
        elif direction == "left":
            self.pos.left -= self.speed
        elif direction == "right":
            self.pos.left += self.speed

        # Begränsa rörelse så att spelaren inte går utanför skärmen
        if self.pos.left < 0:
            self.pos.left = 0
        if self.pos.right > 640:
            self.pos.right = 640

    def draw(self, screen):
        # Rita en rektangel istället för en bild (en balk med bindestreck)
        pygame.draw.rect(screen, self.color, self.pos)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()
        
        self.player = GameObject(100, 10, 5)  # Balken är 100 pixlar lång och 10 pixlar hög
        self.objects = []
        self.create_objects()

    def create_objects(self):
        for x in range(10):
            o = GameObject(40, 10, 0)  # Skapa objekt (hinder eller monster)
            o.pos = pygame.Rect(x * 60, 100, 40, 20)  # Placera ut objekten
            self.objects.append(o)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.player.move("up")
        if keys[pygame.K_DOWN]:
            self.player.move("down")
        if keys[pygame.K_LEFT]:
            self.player.move("left")
        if keys[pygame.K_RIGHT]:
            self.player.move("right")
        
        # Flytta objekt (om du har rörliga objekt)
        for obj in self.objects:
            obj.move()

    def draw(self):
        # Rita bakgrunden (kan vara en solid färg eller en bild)
        self.screen.fill((0, 0, 0))  # Svart bakgrund

        # Rita alla objekt
        for obj in self.objects:
            obj.draw(self.screen)

        # Rita spelarbalken (bestående av bindestreck)
        self.player.draw(self.screen)
        
        pygame.display.update()

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

# Starta och kör spelet
game = Game()
game.run()
