import pygame
from pygame.draw import *
from random import randint
from math import cos, sin

pygame.init()

FPS = 60
screen = pygame.display.set_mode((1200, 900))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

count = 0
balls = []


class Ball:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.x = randint(100, 1100)
        self.y = randint(100, 900)
        self.r = 100
        self.vy = randint(10, 20) / 10
        self.vx = randint(10, 20) / 10
        self.ay = 1 * sin(self.y)
        self.ax = 1 * cos(self.x)
        self.color = COLORS[5]
        self.number = 1
        self.need_to_be_killed = False

    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.vx += self.ax
        self.vy += self.ay

        if self.y < 0:
            self.vy = -self.vy
            self.y = 0
        if self.y > 900:
            self.vy = -self.vy
            self.y = 900
        if self.x < 0:
            self.vx = -self.vx
            self.x = 0
        if self.x > 1200:
            self.vx = -self.vx
            self.x = 1200

    def draw(self):
        pygame.draw.circle(screen, (255, 225, 0), (self.x, self.y - 25), 100)
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y - 25), 100, 5)

        pygame.draw.circle(screen, (255, 0, 0), (self.x - 50, self.y - 50), 25)
        pygame.draw.circle(screen, (0, 0, 0), (self.x - 50, self.y - 50), 25, 5)
        pygame.draw.circle(screen, (0, 0, 0), (self.x - 50, self.y - 50), 5)

        pygame.draw.circle(screen, (255, 0, 0), (self.x + 50, self.y - 50), 25)
        pygame.draw.circle(screen, (0, 0, 0), (self.x + 50, self.y - 50), 25, 5)
        pygame.draw.circle(screen, (0, 0, 0), (self.x + 50, self.y - 50), 5)

        pygame.draw.line(screen, (0, 0, 0),
                         [self.x - 60, self.y - 90],
                         [self.x - 20, self.y - 50], 10)
        pygame.draw.line(screen, (0, 0, 0),
                         [self.x + 60, self.y - 90],
                         [self.x + 20, self.y - 50], 10)

    def targetting(self, event):
        global count
        if (event.pos[0] - self.x) ** 2 + (event.pos[1] - self.y) ** 2 < self.r ** 2:
            count += 5
            print(count)
            self.need_to_be_killed = True


class Ball2:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.x = randint(100, 1100)
        self.y = randint(100, 900)
        self.r = randint(25, 50)
        self.vy = randint(1, 10)
        self.vx = randint(1, 10)
        self.color = COLORS[randint(0, 5)]
        self.number = 2
        self.need_to_be_killed = False

    def move(self):
        self.x += self.vx
        self.y += self.vy
        if self.y < 0:
            self.vy = -self.vy
            self.y = 0
        if self.y > 900:
            self.vy = -self.vy
            self.y = 900
        if self.x < 0:
            self.vx = -self.vx
            self.x = 0
        if self.x > 1200:
            self.vx = -self.vx
            self.x = 1200

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r)

    def targetting(self, event):
        global count
        if (event.pos[0] - self.x) ** 2 + (event.pos[1] - self.y) ** 2 < self.r ** 2:
            count += 1
            print(count)
            self.need_to_be_killed = True


for i in range(10):
    new_ball = Ball2(screen)
    balls.append(new_ball)

new_ball = Ball(screen)
balls.append(new_ball)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for ball in balls:
                print('Click!')
                ball.targetting(event)
                if ball.need_to_be_killed == True:
                    balls.remove(ball)
                    if ball.number == 1:
                        balls.append(Ball(screen))
                    else:
                        balls.append(Ball2(screen))
    my_font = pygame.font.match_font("Arial")
    f1 = pygame.font.Font(my_font, 36)
    text1 = f1.render("Счет " + str(count), True, (255, 255, 255))

    for ball in balls:
        ball.move()
        ball.draw()
    screen.blit(text1, (10, 10))
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
