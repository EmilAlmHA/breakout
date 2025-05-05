import pygame
from pygame.locals import *


pygame.init()

joystick1 = pygame.joystick.Joystick(0)
pygame.joystick.init()

print("Start")
while True:
    for event in pygame.event.get(): # get the events (update the joystick)
        if event.type == QUIT: # allow to click on the X button to close the window
            pygame.quit()
            exit()

    if joystick1.get_button(1) == 1 :
        print("stopped")
        break

