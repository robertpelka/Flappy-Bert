import pygame

def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 400))
    screen.blit(floor_surface, (floor_x_pos+288, 400))

pygame.init()
pygame.display.set_caption("Flappy Bert")
screen = pygame.display.set_mode((288, 512))
clock = pygame.time.Clock()
exitPressed = False

bg_surface = pygame.image.load("assets/background-day.png").convert()
floor_surface = pygame.image.load("assets/base.png").convert()
floor_x_pos = 0

while not exitPressed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exitPressed = True
            pygame.quit()
    
    if exitPressed:
        break

    screen.blit(bg_surface, (0, 0))
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -288:
        floor_x_pos = 0
    

    pygame.display.update()
    clock.tick(120)