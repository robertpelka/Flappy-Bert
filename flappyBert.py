import random
import pygame

def draw_floor():
    screen.blit(floor_surface, (floor_x, 440))
    screen.blit(floor_surface, (floor_x+288, 440))

def create_pipe():
    random_height = random.choice(pipe_heights)
    bottom_pipe = pipe_surface.get_rect(topleft = (288, random_height))
    top_pipe = pipe_surface.get_rect(bottomleft = (288, random_height-150))
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

def is_any_collision(pipes):
    if robert_rect.bottom >= 440 or robert_rect.bottom < -360:
        hit_sound.play()
        vroom_sound.stop()
        pygame.mixer.music.fadeout(500)
        return True
    for pipe in pipes:
        if pipe.colliderect(robert_rect):
            hit_sound.play()
            vroom_sound.stop()
            pygame.mixer.music.fadeout(500)
            return True
    return False

def rotate_robert(robert):
    new_robert = pygame.transform.rotozoom(robert, -robert_movement*2, 1)
    return new_robert

def display_score(is_game_active):
    if is_game_active:
        score_surface = medium_font.render(str(score), False, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (144, 50))
        screen.blit(score_surface, score_rect)
    else:
        score_surface = medium_font.render(str(score), False, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (144, 50))
        screen.blit(score_surface, score_rect)
        score_surface = medium_font.render("Best: "+str(high_score), False, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (144, 90))
        screen.blit(score_surface, score_rect)

def is_pipe_passed(pipe_position):
    if pipe_position < 50:
        return True
    else:
        return False

def update_high_score(score, high_score):
    if score > high_score:
        high_score = score
        with open("save", "w") as save:
            save.write(str(score))
    return high_score

pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)
pygame.init()
screen = pygame.display.set_mode((288, 512))
pygame.display.set_caption("Flappy Bert")
icon = pygame.image.load("assets/icon.png").convert_alpha()
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

is_game_active = False
firstPlay = True
exit_pressed = False

gravity = 0.15
robert_movement = 0
floor_x = 0

score = 0
with open("save", "r") as save:
    high_score = int(save.read())

large_font = pygame.font.Font("assets/font.ttf",42)
medium_font = pygame.font.Font("assets/font.ttf",32)
small_font = pygame.font.Font("assets/font.ttf",24)

bg_surface = pygame.image.load("assets/background.png").convert()
floor_surface = pygame.image.load("assets/base.png").convert()
robert_surface = pygame.image.load("assets/robert.png").convert_alpha()
robert_rect = robert_surface.get_rect(center = (-50, 256))
rotated_robert = robert_surface
pipe_surface = pygame.image.load("assets/pipe.png").convert_alpha()

point_sound = pygame.mixer.Sound("sound/sfx_point.wav")
hit_sound = pygame.mixer.Sound("sound/sfx_hit.wav")
vroom_sound = pygame.mixer.Sound("sound/sfx_vroom.wav")
engine_sound = pygame.mixer.music.load("sound/sfx_engine.wav")

pipe_list = []
pipe_heights = [200, 250, 300]
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1000)
pipe_number = 0
pipe_to_pass_position = 1000


while not exit_pressed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_pressed = True
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and is_game_active:
                robert_movement = 0
                robert_movement -= 5
                vroom_sound.stop()
                vroom_sound.play()
            if event.key == pygame.K_SPACE and not is_game_active:
                pipe_list = []
                pipe_number = 0
                pipe_to_pass_position = 1000
                robert_rect.center = (50, 200)
                robert_movement = 0
                score = 0
                is_game_active = True
                firstPlay = False
                pygame.mixer.music.play(-1)
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
            pipe_to_pass_position = pipe_list[pipe_number].centerx
            pipe_number +=2
    if exit_pressed:
        break

    # Background
    screen.blit(bg_surface, (0, 0))

    if is_game_active:
        # Pipes
        pipe_list = move_pipes(pipe_list)
        pipe_to_pass_position -= 3
        if is_pipe_passed(pipe_to_pass_position):
            point_sound.play()
            score += 1 
            pipe_to_pass_position = 1000

        # Plane
        rotated_robert = rotate_robert(robert_surface)
        robert_movement += gravity
        robert_rect.centery += robert_movement

        if is_any_collision(pipe_list):
            is_game_active = False

        # Floor
        floor_x -= 1
        if floor_x <= -288:
            floor_x = 0
    else:
        title_surface = large_font.render("Flappy Bert", False, (255, 255, 255))
        title_rect = title_surface.get_rect(center = (144, 170))
        screen.blit(title_surface, title_rect)
        description_surface = small_font.render("(press space)", False, (255, 255, 255))
        description__rect = description_surface.get_rect(center = (144, 220))
        screen.blit(description_surface, description__rect)

    # Draw elements
    draw_pipes(pipe_list)
    screen.blit(rotated_robert, robert_rect)
    draw_floor()

    if not firstPlay:
        high_score = update_high_score(score, high_score)
        display_score(is_game_active)


    pygame.display.update()
    clock.tick(120)