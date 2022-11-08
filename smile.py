import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))


circle(screen, (255, 225, 0), (200, 175), 100)
circle(screen, (0, 0, 0), (200, 175), 100, 5)

circle(screen, (255, 0, 0), (150, 150), 25)
circle(screen, (0, 0, 0), (150, 150), 25, 5)
circle(screen, (0, 0, 0), (150, 150), 5)

circle(screen, (0, 0, 0), (200, 300), 100, 5)

circle(screen, (255, 0, 0), (250, 150), 25)
circle(screen, (0, 0, 0), (250, 150), 25, 5)
circle(screen, (0, 0, 0), (250, 150), 5)

pygame.draw.line(screen, (0, 0, 0),
                 [140, 110],
                 [180, 150], 10)
pygame.draw.line(screen, (0, 0, 0),
                 [260, 110],
                 [220, 150], 10)
pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()