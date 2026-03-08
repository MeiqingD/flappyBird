import sys
import os
from time import sleep
import pygame
from random import randrange
pygame.init()

frame = 0
FPS = 60 
map_width = 284
map_height = 512
pipes = [[200, 4, 4]]

gameScreen = pygame.display.set_mode((map_width, map_height))
clock = pygame.time.Clock()

def resource_path(path):
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, path)


background = pygame.image.load(resource_path("images/background.png"))
bird_wing_up = bird_wing_up_copy = pygame.image.load(resource_path("images/bird_wing_up.png"))
bird_wing_down = bird_wing_down_copy = pygame.image.load(resource_path("images/bird_wing_down.png"))
pipe_body = pygame.image.load(resource_path("images/pipe_body.png"))
pipe_end = pygame.image.load(resource_path("images/pipe_end.png"))
bird = [20, map_height // 2]
gravity = 0.55
velocity = 0

def draw_bird(x, y):
    global frame
    if 0 <= frame <= 30:
        gameScreen.blit(bird_wing_up, (x, y))
        frame += 1
    elif 30 < frame <= 60:
        gameScreen.blit(bird_wing_down, (x, y))
        frame += 1
        if frame == 60: frame = 0

def draw_pipes():
    global pipes
    for i in range(len(pipes)):
        for j in range(pipes[i][1]):
            gameScreen.blit(pipe_body, (pipes[i][0], j * 32))
        for j in range(pipes[i][1] + pipes[i][2] + 2, 16):
            gameScreen.blit(pipe_body, (pipes[i][0], j * 32))
        gameScreen.blit(pipe_end, (pipes[i][0], pipes[i][1] * 32))
        gameScreen.blit(pipe_end, (pipes[i][0], (pipes[i][1] + pipes[i][2] + 1) * 32))
        pipes[i][0] -= 1.5

def spawn_pipes():
    global pipes
    if len(pipes) < 4:
        x = pipes[-1][0] + 200
        open_pos = randrange(1, 9)
        open_size = randrange(4,7)
        pipes.append([x, open_pos, open_size])

def safe():
    global pipes
    if bird[1] < 0:
        print("hit ceiling")
        return False
    if bird[1] > map_height - 35:
        print("hit floor")
        return False
    if pipes[0][0] - 20 < bird[0] < pipes[0][0] + 69:
        if bird[1] < (pipes[0][1] + 1) * 32 - 10 or bird[1] > (pipes[0][1] + pipes[0][2]) * 32  + 10:
            print("hit pipe")
            return False
    return True

def reset():
    global frame, map_width, map_height, FPS, pipes, bird, gravity, velocity
    frame = 0
    FPS = 60 
    map_width = 284
    map_height = 512
    pipes.clear()
    bird.clear()
    pipes = [[200, 4, 4]]
    bird = [20, map_height // 2]
    gravity = 0.55
    velocity = 0


def gameLoop():
    global velocity, gravity, bird, FPS, bird_wing_up, bird_wing_down

    while True: 
        spawn_pipes()
        if pipes[0][0] <= -100:
            pipes.pop(0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                velocity = -6
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            velocity = -8
        velocity += gravity
        bird[1] += velocity
        angle = max(-45, min(45, -velocity * 4))
        bird_wing_up = pygame.transform.rotate(bird_wing_up_copy,angle)
        bird_wing_down = pygame.transform.rotate(bird_wing_down_copy, angle)
        gameScreen.blit(background, (0,0))
        draw_bird(bird[0], bird[1])
        draw_pipes()
        pygame.display.update()
        if not safe():
            sleep(3)
            reset()
        clock.tick(FPS)
gameLoop()