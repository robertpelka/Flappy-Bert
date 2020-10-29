import pygame
import random

def draw_floor():
    screen.blit(floorSurface, (floorX, 440))
    screen.blit(floorSurface, (floorX+288, 440))

def create_pipe():
    randomHeight = random.choice(pipeHeights)
    bottomPipe = pipeSurface.get_rect(midtop = (288, randomHeight))
    topPipe = pipeSurface.get_rect(midbottom = (288, randomHeight-150))
    return bottomPipe, topPipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.top < 0:
            flippedPipe = pygame.transform.flip(pipeSurface, False, True)
            screen.blit(flippedPipe, pipe)
        else:
            screen.blit(pipeSurface, pipe)

def check_colisions(pipes):
    if robertRect.bottom >= 440:
        return False
    for pipe in pipes:
        if pipe.colliderect(robertRect):
            return False
    return True


pygame.init()
pygame.display.set_caption("Flappy Bert")
screen = pygame.display.set_mode((288, 512))
clock = pygame.time.Clock()

isGameActive = True
exitPressed = False

gravity = 0.25
robertMovement = 0
floorX = 0

bgSurface = pygame.image.load("assets/background.png").convert()
floorSurface = pygame.image.load("assets/base.png").convert()
robertSurface = pygame.image.load("assets/robert.png").convert_alpha()
robertRect = robertSurface.get_rect(center = (50, 256))
pipeSurface = pygame.image.load("assets/pipe.png").convert_alpha()

pipeList = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)


while not exitPressed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exitPressed = True
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and isGameActive:
                robertMovement = 0
                robertMovement -= 6
            if event.key == pygame.K_SPACE and not isGameActive:
                pipeList = []
                robertRect.center = (50, 256)
                robertMovement = 0
                isGameActive = True
        if event.type == SPAWNPIPE:
            pipeList.extend(create_pipe())
    if exitPressed:
        break

    # Background
    screen.blit(bgSurface, (0, 0))

    if isGameActive:
        # Pipes
        pipeList = move_pipes(pipeList)
        draw_pipes(pipeList)
        pipeHeights = [200, 250, 300]

        # Plane 
        screen.blit(robertSurface, robertRect)
        robertMovement += gravity
        robertRect.centery += robertMovement

        isGameActive = check_colisions(pipeList)

    # Floor
    floorX -= 1
    draw_floor()
    if floorX <= -288:
        floorX = 0

    pygame.display.update()
    clock.tick(120)