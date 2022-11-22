import math
from random import choice, randint

import pygame

FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600

y = 560
x = 400
phase = 0


class Ball:
    def __init__(self, screen: pygame.Surface, x, y):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """

        self.screen = screen
        self.x = x
        self.y = y
        self.r = 3
        self.vx = 0
        self.vy = 0
        self.color = BLACK
        self.live = 4

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx
        self.y -= self.vy
        self.vy = self.vy - 1

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if ((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2) ** (1 / 2) <= self.r + obj.r:
            print("Попал")
            """Детектит попадание в мишень"""
            return True
        if self.y < 0:
            self.vy = -self.vy
            self.live = self.live - 1
        if self.y > 590:
            self.vy = -self.vy
            self.live = self.live - 1
        if self.x < 0:
            self.vx = -self.vx
            self.live = self.live - 1
        if self.x > 790:
            self.vx = -self.vx
            self.live = self.live - 1
            """Гравитация и отражение от стенок"""
        return False


class Gun:
    """Положение пушки"""

    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 15
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.w = 0
        self.x = 400
        self.y = 300
        self.phi = 0

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.w = 1/50
        elif keys[pygame.K_LEFT]:
            self.w = -1/50
        else:
            self.w = 0

        self.phi += self.w
        self.x = 400 + 200 * math.sin(self.phi)
        self.y = 300 - 200 * math.cos(self.phi)

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen, self.x, self.y)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 15

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            if event.pos[0] - self.x != 0:
                self.an = math.atan((event.pos[1] - self.y) / (event.pos[0] - self.x))

        if self.f2_on:
            self.color = RED

        else:
            self.color = GREY

    def draw(self):
        pass
        """Отрисовка пушки"""

        pygame.draw.circle(screen, (GREY), (400, 300), 202)
        pygame.draw.circle(screen, (WHITE), (400, 300), 198)
        pygame.draw.circle(screen, (255, 255 - self.f2_power * 2, 0), (self.x, self.y), 26)
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), 25)
        pygame.draw.polygon(screen, (255, 255 - self.f2_power * 2, 0),
                            ([self.x - 10 * math.sin(self.an), self.y + 10 * math.cos(self.an)],
                             [self.x - 25 * math.cos(self.an), self.y - 25 * math.sin(self.an)],

                             [self.x + 10 * math.sin(self.an), self.y - 10 * math.cos(self.an)],
                             [self.x + 25 * math.cos(self.an), self.y + 25 * math.sin(self.an)],))

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    """Цель - ее начальное положение"""

    def __init__(self, screen: pygame.Surface, x=400, y=300):
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 100
        self.color = BLACK
        self.live = 10
        self.points = 0

    def new_target(self):
        """ Инициализация новой цели. """
        self.x = randint(20, 780)
        self.y = randint(50, 550)
        self.r = randint(5, 20)
        self.color = YELLOW

    def hit(self, points=1):
        """Счетчик поинтов"""
        self.points += points

    def draw(self):
        pass
        """Рисуем новую цель"""
        pygame.draw.circle(screen, (self.color),
                           [self.x, self.y], self.r)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target = Target(screen)
finished = False

while not finished:
    screen.fill(WHITE)
    gun.move()
    gun.draw()
    target.draw()
    my_font = pygame.font.match_font("Arial")
    f1 = pygame.font.Font(my_font, 36)
    text1 = f1.render("Счет " + str(target.points), True, (0, 0, 0))
    screen.blit(text1, (10, 10))

    for b in balls:
        b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for b in balls:
        b.move()
        if b.hittest(target) and target.live:
            target.hit()
            target.new_target()
        if b.live <= 0:
            balls.remove(b)
    gun.power_up()

    pygame.display.update()
pygame.quit()
