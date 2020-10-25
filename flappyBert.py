import pygame

def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 400))
    screen.blit(floor_surface, (floor_x_pos+288, 400))

pygame.init()
pygame.display.set_caption("Flappy Bert")
screen = pygame.display.set_mode((288, 512))
clock = pygame.time.Clock()
exitPressed = False
gravity = 0.25
robert_movement = 0

bg_surface = pygame.image.load("assets/background.png").convert()
floor_surface = pygame.image.load("assets/base.png").convert()
floor_x_pos = 0

robert_surface = pygame.image.load("assets/robert.png").convert_alpha()
robert_rect = robert_surface.get_rect(center = (50, 256))

while not exitPressed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exitPressed = True
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                robert_movement = 0
                robert_movement -= 6
    
    if exitPressed:
        break

    screen.blit(bg_surface, (0, 0))
    screen.blit(robert_surface, robert_rect)
    robert_movement += gravity
    robert_rect.centery += robert_movement
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -288:
        floor_x_pos = 0
    

    pygame.display.update()
    clock.tick(120)