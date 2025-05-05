import pygame
pygame.init()
pygame.joystick.init()

screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Controller Input Debug")

# Initialize all joysticks
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
for j in joysticks:
    j.init()
    print(f"Detected joystick: {j.get_name()}")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Print any controller input event
        elif event.type in (
            pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP,
            pygame.JOYAXISMOTION, pygame.JOYHATMOTION
        ):
            print(event)

pygame.quit()
