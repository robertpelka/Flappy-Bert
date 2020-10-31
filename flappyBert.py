import random
import pygame

def draw_floor():
    screen.blit(floor_surface, (floor_x, 440))
    screen.blit(floor_surface, (floor_x+288, 440))

def create_pipe():
    random_height = random.choice(pipe_heights)
    bottom_pipe = pipe_surface.get_rect(midtop = (288, random_height))
    top_pipe = pipe_surface.get_rect(midbottom = (288, random_height-150))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 3
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.top < 0:
            flipped_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flipped_pipe, pipe)
        else:
            screen.blit(pipe_surface, pipe)

def check_colisions(pipes):
    if robert_rect.bottom >= 440:
        return False
    for pipe in pipes:
        if pipe.colliderect(robert_rect):
            return False
    return True

def rotate_robert(robert):
    new_robert = pygame.transform.rotozoom(robert, -robert_movement*2, 1)
    return new_robert

def display_score(is_game_active):
    if is_game_active:
        score_surface = game_font.render(str(score), False, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (144, 50))
        screen.blit(score_surface, score_rect)
    else:
        score_surface = game_font.render(str(score), False, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (144, 50))
        screen.blit(score_surface, score_rect)
        score_surface = game_font.render("Best: "+str(high_score), False, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (144, 90))
        screen.blit(score_surface, score_rect)

def update_high_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

pygame.init()
pygame.display.set_caption("Flappy Bert")
screen = pygame.display.set_mode((288, 512))
clock = pygame.time.Clock()

is_game_active = True
exit_pressed = False

gravity = 0.15
robert_movement = 0
floor_x = 0

score = 0
high_score = 0

game_font = pygame.font.Font("assets/font.ttf",32)

bg_surface = pygame.image.load("assets/background.png").convert()
floor_surface = pygame.image.load("assets/base.png").convert()
robert_surface = pygame.image.load("assets/robert.png").convert_alpha()
robert_rect = robert_surface.get_rect(center = (50, 256))
pipe_surface = pygame.image.load("assets/pipe.png").convert_alpha()

pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)


while not exit_pressed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_pressed = True
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and is_game_active:
                robert_movement = 0
                robert_movement -= 5
            if event.key == pygame.K_SPACE and not is_game_active:
                pipe_list = []
                robert_rect.center = (50, 256)
                robert_movement = 0
                score = 0
                is_game_active = True
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
    if exit_pressed:
        break

    # Background
    screen.blit(bg_surface, (0, 0))

    if is_game_active:
        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        pipe_heights = [200, 250, 300]

        # Plane
        rotated_robert = rotate_robert(robert_surface)
        screen.blit(rotated_robert, robert_rect)
        robert_movement += gravity
        robert_rect.centery += robert_movement

        is_game_active = check_colisions(pipe_list)

    update_high_score(score, high_score)
    display_score(is_game_active)

    # Floor
    floor_x -= 1
    draw_floor()
    if floor_x <= -288:
        floor_x = 0

    pygame.display.update()
    clock.tick(120)