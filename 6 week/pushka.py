import math
from random import choice
from random import randint
import pygame

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
FPS = 30
g = 0.8


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        r - радиус мишени
        vx - скорость мяча по оси x
        xy - скорость мяча по оси y
        color - цвет мяча
        live - время жизни шарика
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """

        if self.x + self.r >= WIDTH:
            self.x = WIDTH - self.r
            self.vx = - 0.8 * self.vx
        if self.x - self.r <= 0:
            self.x = self.r
            self.vx = -0.8 * self.vx
        if self.y - self.r <= 0:
            self.y = self.r
            self.vx *= 0.8
            self.vy *= -0.8
        if self.y + self.r >= HEIGHT:
            self.y = HEIGHT - self.r
            self.vx *= 0.8
            self.vy = -0.8 * self.vy

        self.x += self.vx
        self.vy -= g
        self.y -= self.vy

    def draw(self):

        """ отрисовка патрона """
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
        # FIXME
        if ((obj.x - self.x) ** 2 + (obj.y - self.y) ** 2) ** (1 / 2) <= (self.r + obj.r):
            return True
        else:
            return False


class Gun:
    def __init__(self, screen):
        """
        screen - экран
        f2_power - мощность выстрела
        f2_on - 1 если пушка заряжена, 0 - если нет
        an - угол пушки
        color - цвет пушки
        x, y -  координаты пушки
        """
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.x = 40
        self.y = 450

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet, targets

        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.pos[1] - 450) / (event.pos[0] - 20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        """ Отрисовка мощности пушки"""
        width = 10
        coords = [
            (self.x, self.y),
            (self.x + (self.f2_power + 20) * math.cos(self.an),
             self.y + (self.f2_power + 20) * math.sin(self.an)),
            (self.x + (self.f2_power + 20) * math.cos(self.an) + width * math.sin(self.an),
             self.y + (self.f2_power + 20) * math.sin(self.an) - width * math.cos(self.an)),
            (self.x + width * math.sin(self.an), self.y - width * math.cos(self.an))
        ]
        pygame.draw.polygon(self.screen, self.color, coords, width=0)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    def __init__(self):
        """
        x y - координаты цели
        r - радиус цели
        vx, vy - скорость цели
        color - цвет мишени
        live - жизни цели
        points - очки
        """
        self.screen = screen
        self.x = randint(600, 750)
        self.y = randint(300, 550)
        self.r = randint(30, 50)
        self.vx = randint(-15, 15)
        self.vy = randint(-15, 15)
        self.color = RED
        self.live = 1
        self.point = 5

    def new_target(self):
        """ Инициализация новой цели. """
        self.__init__()

    def draw(self):
        """ отрисовка цели"""
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def move(self):
        """ движение цели """
        self.x += self.vx
        self.y += self.vy

        if self.x + self.r >= WIDTH:
            self.vx = -1 * self.vx
        if self.x - self.r <= 0:
            self.vx = -1 * self.vx
        if self.y - self.r <= 0:
            self.vy = -1 * self.vy
        if self.y + self.r >= HEIGHT:
            self.vy = -1 * self.vy


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []
targets = []
points = 0  # Счетчик игровых очков
myfont = pygame.font.SysFont("Comic Sans MS", 30)
clock = pygame.time.Clock()
gun = Gun(screen)
target = Target()
finished = False

while not finished:
    screen.fill(WHITE)
    screen.blit(myfont.render(f'Score: {points}', False, (0, 0, 0)), (10, 10))
    gun.draw()
    target.draw()
    target.move()
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
            target.live = 0
            points += target.point
            print(points)
            target.new_target()
    gun.power_up()

pygame.quit()
