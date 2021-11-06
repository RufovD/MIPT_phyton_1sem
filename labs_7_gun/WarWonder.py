import math
from random import randint

import pygame
from pygame.draw import *

FPS = 100

#писание некоторых испотзуемых цветов
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (192, 192, 192)
GAME_COLORS = [BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 1200
HEIGHT = 800


#Описание бронебойных снарядов-треугольников
class Triangle:
    def __init__(self, screen: pygame.Surface):

        self.screen = screen
        self.x = 0
        self.y = 0        
        self.vx = 0
        self.vy = 0
        self.color = BLACK
        self.a = 26
        self.b = 20
        self.incline = math.asin((self.b / 2) / (self.a))
        self.time = 0
        self.angel = 0
        self.ydar = 0

    #Описание движения этих снарядов (включает вращение)
    def move(self):
        """Снаряды не отражаются от стен, не отражаются от
        ланшавта, просто врезаются в землю и остаются там. В полете 
        снаряд делает оборот. Время жизни не ограничено.
        """
        if self.ydar == 0:           
            dt = 3 / FPS
            self.vy = self.vy + 136*dt
            self.x += self.vx * dt
            self.y += self.vy * dt 
            self.time += dt
            if (self.y >= (HEIGHT - 100)) or (self.y + self.a * math.sin(self.incline + self.angel) >= (HEIGHT - 100)) or (self.y + self.a * math.sin(self.incline - self.angel) >= (HEIGHT - 100)):
                self.ydar = 1

    #Рисование бронебойного снаряда
    def draw(self):
        if self.vx > 0:
            self.angel = math.atan((self.vy) / (self.vx))
        elif self.vx < 0:
            self.angel = math.pi + math.atan((self.vy) / (self.vx))
        else:
            if self.vy >= 0:
                self.angel = math.pi / 2
            else:
                self.angel =  - math.pi / 2
                
        polygon(self.screen, self.color, [(self.x, self.y), (self.x - self.a * math.cos(self.incline + self.angel), self.y + self.a * math.sin(self.incline + self.angel)),
                                           (self.x - self.a * math.cos(self.incline - self.angel), self.y + self.a * math.sin(self.incline - self.angel)), (self.x, self.y)])
        
        polygon(self.screen, (255, 0, 0), [(self.x, self.y), (self.x - self.a * math.cos(self.incline + self.angel), self.y + self.a * math.sin(self.incline + self.angel)),
                                           (self.x - self.a * math.cos(self.incline - self.angel), self.y + self.a * math.sin(self.incline - self.angel)), (self.x, self.y)], 2)
 
    #Проверка на попадание во врага
    def hittest(self, obj):
        if (obj.r)**2 >= ((self.x - obj.x)**2 + (self.y - obj.y)**2):
            return True
        
        else:
            return False




#Описание картечи - то, на что распадается разрывной снаряд
class Buckshot:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.popal = 0
        self.x = []
        self.y = []
        self.r = 4
        self.color = GAME_COLORS[randint(0, 4)]
        self.v = 15
        self.vx = []
        self.vy = []
        self.n = 8
        for i in range(0, self.n):
            self.vx += [self.v * math.cos(2 * math.pi * i/ self.n)]
            self.vy += [self.v * math.sin(2 * math.pi * i/ self.n)]
        self.time = 0

    #Описание движения картечи
    def move(self):
        """В точке, где произошел взрыв разрывного
        снаряда, появляется его осколки - 8 шариков, 
        летящих во все стороны. Отскакивают от стен и
        ланшавта. Время жизни ограничено."""
        dt = 3 / FPS
        for i in range(0, self.n):
            self.vy[i] = self.vy[i] + 100*dt
            self.x[i] += self.vx[i] * dt
            self.y[i] += self.vy[i] * dt 
            if (self.x[i] + self.r >= WIDTH) or (self.x[i] - self.r <= 0):
                self.vx[i] = - self.vx[i]
            if (self.y[i] + self.r >= (HEIGHT - 100)) and (self.vy[i] >= 0):
                self.vy[i] = - self.vy[i]
        self.time += dt

    #Рисование картечи
    def draw(self):
        for i in range (0, self.n):
            circle(self.screen, self.color, (self.x[i], self.y[i]), self.r)

    #Проверка попадания одной из картечинок во врага
    def hittest(self, obj):
        for i in range(0, self.n):
            if (self.r + obj.r)**2 >= ((self.x[i] - obj.x)**2 + (self.y[i] - obj.y)**2):
                self.popal = 1
        if self.popal == 1:
            self.popal = 0
            return True       
        else:
            return False




#Описание разрывного снарядка-шарика
class Ball:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.x = 40
        self.y = 450
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = GAME_COLORS[randint(0, 4)]
        self.time = 0

    #Описание движения этого снаряда
    def move(self):
        """Переместить мяч по прошествии единицы времени.
        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        отскок от границ экрана есть, отражение от ланшавта тоже. Время жизни ограничено. Псоле
        окончания этого времени от снарядка остаются осколки - картечь.
        """
        dt = 3 / FPS
        self.vy = self.vy + 136*dt
        self.x += self.vx * dt
        self.y += self.vy * dt 
        self.time += dt
        if (self.x + self.r >= WIDTH) or (self.x - self.r <= 0):
            self.vx = - self.vx
        if (self.y + self.r >= (HEIGHT - 100)) and (self.vy >= 0):
            self.vy = - self.vy

        if self.time >= 3:
            new_buckshot = Buckshot(self.screen)
            for i in range (0, new_buckshot.n):               
                new_buckshot.x += [self.x]
                new_buckshot.y += [self.y]
            buckshots.append(new_buckshot)
            balls.remove(self)

    #Рисование этого снаряда
    def draw(self): pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)

    #Проверка на попадание во врага
    def hittest(self, obj):
        if (self.r + obj.r)**2 >= ((self.x - obj.x)**2 + (self.y - obj.y)**2):
            return True       
        else:
            return False




#Описание пушки, юнит, которым управляет игрок Российской империи
class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.angle = 1
        self.color = GREY
        self.x = WIDTH / 2
        self.y = 390
        self.v = 3
        self.r = 60
        self.go = 0

    #Прицеливание, перемещение ствола пушки с началом на корпусе пушки в сторону курсора
    def targetting(self, event):
        if event.pos[0] - self.x > 0:
            self.angle = math.atan((self.y - event.pos[1]) / (event.pos[0] - self.x))
        elif event.pos[0] - self.x < 0:
            self.angle = math.pi + math.atan((self.y - event.pos[1]) / (event.pos[0] - self.x))
        else:
            if self.y - event.pos[1] >= 0:
                self.angle = math.pi / 2
            else:
                self.angle =  - math.pi / 2
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    #Движение пушки при нажатии стрелочек влево или вправо
    def move(self, keys):
        if (keys[pygame.K_LEFT]) and (self.x - 82 > 0):
            self.go = -1
        if (keys[pygame.K_RIGHT]) and (self.x + 82 < WIDTH):
            self.go = 1
        self.x += self.go * self.v
        self.go = 0

    #Остановка пушки при отпускании зажатой клавиши
    def move_end(self, event):
        if (event.key == pygame.K_LEFT) or (event.key == pygame.K_RIGHT):
            self.go = 0 

    #Рисование пушки        
    def draw(self):
        circle(self.screen, GREEN, (self.x, self.y + 40 + HEIGHT - 600), self.r)
        circle(self.screen, BLACK, (self.x, self.y + 40 + HEIGHT - 600), self.r, 1)
        rect(self.screen, GREEN, (self.x - 70, self.y + 40 + HEIGHT - 600, 140, self.r))
        rect(self.screen, BLACK, (self.x - 70, self.y + 40 + HEIGHT - 600, 140, self.r), 1)
        circle(self.screen, (190, 190, 190), (self.x - 50, self.y + 80 + HEIGHT - 600), 30)
        circle(self.screen, BLACK, (self.x - 50, self.y + 80 + HEIGHT - 600), 30, 1)
        circle(self.screen, (190, 190, 190), (self.x + 50, self.y + 80 + HEIGHT - 600), 30)
        circle(self.screen, BLACK, (self.x + 50, self.y + 80 + HEIGHT - 600), 30, 1)
        polygon(self.screen, self. color, [(self.x, self.y + HEIGHT - 600), (self.x + self.f2_power * math.cos(self.angle), self.y - self.f2_power * math.sin(self.angle) + HEIGHT - 600),
                                           (self.x + self.f2_power * math.cos(self.angle) - 5 * math.sin(self.angle), self.y  + HEIGHT - 600 - self.f2_power * math.sin(self.angle) - 5 * math.cos(self.angle)),
                                           (self.x - 5 * math.sin(self.angle), self.y - 5 * math.cos(self.angle) + HEIGHT - 600), (self.x, self.y + HEIGHT - 600)])
        polygon(self.screen, BLACK, [(self.x, self.y + HEIGHT - 600), (self.x + self.f2_power * math.cos(self.angle), self.y - self.f2_power * math.sin(self.angle) + HEIGHT - 600),
                                           (self.x + self.f2_power * math.cos(self.angle) - 5 * math.sin(self.angle), self.y  + HEIGHT - 600 - self.f2_power * math.sin(self.angle) - 5 * math.cos(self.angle)),
                                           (self.x - 5 * math.sin(self.angle), self.y - 5 * math.cos(self.angle) + HEIGHT - 600), (self.x, self.y + HEIGHT - 600)], 2)
        
    #Нажата клавиша на мыши - показатель подготовки выстрела   
    def fire1_start(self, event):
        self.f2_on = 1

    #Увеличение силы выстрела при удержании кнопки мыши
    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY

    #Собственно выстрел (разрывным) в строну курсора мыши, куда была направлениа пушка с набранной силой
    def fire1_end(self, event):
        new_ball = Ball(self.screen)
        new_ball.x = self.x
        new_ball.y = self.y  + HEIGHT - 600
        new_ball.vx = self.f2_power * math.cos(self.angle) * 4
        new_ball.vy = - self.f2_power * math.sin(self.angle) * 4
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    #То же самое, но стреляем бронебойным        
    def fire2_end(self, event):
        new_triangle = Triangle(self.screen)
        new_triangle.x = self.x
        new_triangle.y = self.y + HEIGHT - 600
        new_triangle.vx = self.f2_power * math.cos(self.angle) * 4
        new_triangle.vy = - self.f2_power * math.sin(self.angle) * 4
        triangls.append(new_triangle)
        self.f2_on = 0
        self.f2_power = 10        





#Описание вертолетов - германских юнитов красного цвета
class Helicopter:
    def __init__(self, screen):
        self.r = 50
        self.x = 100
        self.y = randint(141 + self.r, HEIGHT - 101 - self.r - 160)
        self.v = randint(-100, 100)
        if abs(self.v) < 40:
            self.v = 100 - abs(self.v)
        self.color = RED
        self.screen = screen

    #Рисовние вертолетов
    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)

    #Движение вертолетов ввверх-вниз (собственно поэтому они и названы вертолетами)
    def move(self):
        dt = 5 / FPS
        self.y += self.v * dt
        if (self.y - self.r <= 140) or (self.y + self.r >=HEIGHT - 100 - 160):
            self.v = -self.v       

    #Создание нового вертолета взамен побдитого - переопределение некоторых его параметров
    def create_helicopter(self):
        self.y = randint(141 + self.r, HEIGHT - 101 - self.r - 160)
        self.v = randint(-100, 100)
        if abs(self.v) < 40:
            self.v = 100 - abs(self.v)




#Описание самолетов - германских юнитоав темно-серого цвета
class Plane:
    def __init__(self, screen):
        self.screen = screen
        self.time = 0
        self.color = (128, 128, 128)
        self.r = 40
        self.y = 50
        self.x = randint(282 + self.r, WIDTH - 152 - self.r)
        self.v = randint(-100, 100)
        if self.v == 0:
            self.v = 100

    #Рисование самолета
    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)
        pygame.draw.circle(self.screen, BLACK, (self.x, self.y), self.r, 2)

    #Движение самолетов вправо-влево (из-за этого и названы самолетами)
    def move(self):
        dt = 5 / FPS
        self.time += dt
        self.x += self.v * dt
        if (self.x - self.r - 281 <= 0) or (self.x + self.r >= WIDTH - 151):
            self.v = -self.v

        #Периодический сброс бомб с самолетов во время их движения
        if self.time >= 10:
            new_bomb = Bomb(self.screen)
            new_bomb.x = self.x
            new_bomb.y = self.y + self.r
            new_bomb.vx = self.v
            bombs.append(new_bomb)
            self.time = 0

    #Создание нового самолета взамен подбитого - переопределение некоторых его параметров
    def create_plane(self):
        self.time = 0
        self.x = randint(282 + self.r, WIDTH - 152 - self.r)
        self.v = randint(-100, 100)
        if self.v == 0:
            self.v = 100      




#Описание аэростата - юнита светло-серого цвета, которым управляет игрок Германии
class Airship:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.r = 30
        self.time = 0
        self.color = (192, 192, 192)
        self.y = 60
        self.x = WIDTH - 152 - self.r
        self.v = -90
        
    #Движение аэростата влево-вправо  
    def move(self):
        dt = 5 / FPS
        self.time += dt
        self.x += self.v * dt
        if (self.x - self.r - 281 <= 0) or (self.x + self.r >= WIDTH - 151):
            self.v = -self.v

    #Рисовние аэростата
    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)
        pygame.draw.circle(self.screen, BLACK, (self.x, self.y), self.r, 2)

    #По нажатию пробела - сбрасывание бомбы, если произведена перезарядка, т.е. прошло некоторое время со сброса предыдущей бомбы           
    def fire(self, event):
        if (event.key == pygame.K_SPACE) and (self.time >= 7):
            new_bomb = Bomb(self.screen)
            new_bomb.x = self.x
            new_bomb.y = self.y + self.r
            new_bomb.vx = self.v
            bombs.append(new_bomb)
            self.time = 0




#Описание бомбыы    
class Bomb:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.x = 100
        self.y = 80
        self.r = 5
        self.color = BLACK
        self.vx = 0
        self.vy = 50

    #Рисование бомбы
    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)

    #Движение бомбы. Летит вниз под действием силы тяжести. Отскакивает от стен    
    def move(self):
        dt = 5 / FPS
        self.y += self.vy * dt
        self.x += self.vx * dt

        if (self.x >= WIDTH - self.r) or (self.x <= self.r):
            self.vx = -self.vx

    #Проверка, попала ли бомба в пушку
    def hit(self, obj):
        if (self.r + obj.r)**2 >= (self.x - obj.x)**2 + (-self.y + 40 + HEIGHT - 600 + obj.y )**2:
            return True
        else:
            return False

    #Стычка бомбы с землей или пушкой - бомба взрывается, поряждая короткий Взрыв    
    def clash(self):
        new_bang = Bang(screen)
        new_bang.x = self.x
        new_bang.y = self.y
        bangs.append(new_bang)
        bombs.remove(self)




#Описание взрыва            
class Bang:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.x = 0
        self.y = 0
        self.r = 30
        self.color = (255, 128, 0)
        self.time = 0

    #Рисование взрыва - оранжевый растущий круг с ограниченным временем жизни
    def draw(self):
        dt = 10 / FPS
        if self.time <= 1:
            circle(self.screen, self.color, (self.x, self.y), self.r * self.time)
            self.time += dt
        else:
            bangs.remove(self)
    
    


pygame.init()

#Текстовые поля
f1 = pygame.font.Font(None, 140)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
f2 = pygame.font.Font(None, 140)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
f3 = pygame.font.Font(None, 40)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
f4 = pygame.font.Font(None, 40)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
f5 = pygame.font.Font(None, 100)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
f6 = pygame.font.Font(None, 100)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
f7 = pygame.font.Font(None, 50)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
f8 = pygame.font.Font(None, 50)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
f9 = pygame.font.Font(None, 50)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
f10 = pygame.font.Font(None, 50)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
f11 = pygame.font.Font(None, 50)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
f12 = pygame.font.Font(None, 50)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
f13 = pygame.font.Font(None, 50)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
f14 = pygame.font.Font(None, 50)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
f15 = pygame.font.Font(None, 50)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
f16 = pygame.font.Font(None, 50)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
f16 = pygame.font.Font(None, 50)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
f17 = pygame.font.Font(None, 50)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
f18 = pygame.font.Font(None, 50)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
f19 = pygame.font.Font(None, 50)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
f20 = pygame.font.Font(None, 50)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
f21 = pygame.font.Font(None, 50)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
f22 = pygame.font.Font(None, 50)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
f23 = pygame.font.Font(None, 50)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
f24 = pygame.font.Font(None, 60)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

#Задание здоровья пушки и аэростата
health_tank = 3
health_airship = 5

#Создание списков юнитов и всех снядов
balls = []
triangls = []
helicopters = []
planes = []
bombs = []
buckshots = []
bangs = []

#Создание юнитов, заполнение списков юнитов
gun = Gun(screen)

airship = Airship(screen)

new_helicopter_1 = Helicopter(screen)
new_helicopter_1.x = 100
new_helicopter_2 = Helicopter(screen)
new_helicopter_2.x = WIDTH - 100
helicopters += [new_helicopter_1] + [new_helicopter_2]

new_plane_1 = Plane(screen)
new_plane_1.y = 160
new_plane_2 = Plane(screen)
new_plane_2.y = 270
planes += [new_plane_1] + [new_plane_2]


#подготовка к пайгеймовским циклам 
clock = pygame.time.Clock()

finished = False

#Первое окно (встечное). Описание игры, правила, предложени начать
while not finished:
    screen.fill(BLACK)
    text7 = f7.render('Добро пожаловать в WarWonder! WarWonder - это эпичный шутер ', True,
                    (255, 255, 255))
    screen.blit(text7, (20, 20))
    text8 = f8.render('на двоих игроков, которым придется столкнуться лицом к лицу в', True,
                    (255, 255, 255))
    screen.blit(text8, (20, 60))
    text9 = f9.render('динамичном сражении на полях Первой мировой. Выбирай одну из ', True,
                    (255, 255, 255))
    screen.blit(text9, (20, 100))
    text10 = f10.render('сторон: пушка Российской империи или целый авиационный полк', True,
                    (255, 255, 255))
    screen.blit(text10, (20, 140))
    text11 = f11.render('Германии. Сражайся и побеждай вместе с WarWonder! ', True,
                    (255, 255, 255))
    screen.blit(text11, (20, 180))

    text12 = f12.render('ПРАВИЛА. На стороне Российской империи - зеленая пушка. Все', True,
                    (255, 255, 255))
    screen.blit(text12, (20, 250))
    text13 = f13.render('остальное - на стороне Германии. Игрок Российской имерии ', True,
                    (255, 255, 255))
    screen.blit(text13, (20, 290))
    text14 = f14.render('управляет пушкой. Для выстрела необходимо выбрать мышью ', True,
                    (255, 255, 255))
    screen.blit(text14, (20, 330))
    text15 = f15.render('желаемый угол, затем зажать левую или правую кнопку мыши ', True,
                    (255, 255, 255))
    screen.blit(text15, (20, 370))
    text16 = f16.render('(чем дольше держать - тем сильнее выстрел, но есть предел). ', True,
                    (255, 255, 255))
    screen.blit(text16, (20, 410))
    text17 = f17.render('Левая кнопка стреляет разрывным шаром, правая - бронебойным ', True,
                    (255, 255, 255))
    screen.blit(text17, (20, 450))
    text18 = f18.render('снарядом. Игрок Германии управляет светло-серым дирижаблем, ', True,
                    (255, 255, 255))
    screen.blit(text18, (20, 490))
    text19 = f19.render('который, после нажатия на пробел, при совешенной перезарядке, ', True,
                    (255, 255, 255))
    screen.blit(text19, (20, 530))
    text20 = f20.render('сбросит бомбу. Так же могут сбрасывать бомбы некоторые другие ', True,
                    (255, 255, 255))
    screen.blit(text20, (20, 570))
    text21 = f21.render('дирижабли. Управление танком происходит при помощи стрелочек ', True,
                    (255, 255, 255))
    screen.blit(text21, (20, 610))
    text22 = f22.render('"влево", "вправо". Задача сторон - понизить здоровье управляемой ', True,
                    (255, 255, 255))
    screen.blit(text22, (20, 650))
    text23 = f23.render('вражеской техники до 0. Перезарядка дирижабля автоматическая.', True,
                    (255, 255, 255))
    screen.blit(text23, (20, 690))
    text24 = f24.render('Чтобы начать играть, нажмите на крестик', True,
                    (255, 255, 255))
    screen.blit(text24, (150, 740))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
    
finished = False

#Второе окно (игровое) - тут происходят основные действия
while not finished:
    
    #Рисовние неба, ланшавта
    screen.fill((204, 255, 255))
    rect(screen, (102, 51, 0), (0, HEIGHT - 100, WIDTH, 100))
    rect(screen, (0, 102, 0), (0, HEIGHT - 100, WIDTH, 40))
    rect(screen, (0, 0, 0), (-10, HEIGHT - 100, WIDTH + 10, 40), 3)

    #Отображение информауия о здоровье пушки и аэростата
    text1 = f1.render(str(health_tank), True,
                    (100, 0, 0))
    screen.blit(text1, (80, 40))
    text2 = f2.render(str(health_airship), True,
                    (100, 0, 0))
    screen.blit(text2, (WIDTH - 210, 40))
    
    text3 = f3.render('Здоровье пушки' , True,
                  (100, 0, 0))
    screen.blit(text3, (15, 5))

    text4 = f4.render('Здоровье аэростата', True,
                  (100, 0, 0))
    screen.blit(text4, (WIDTH - 290, 5))

    #Рисование и движение некоторых объектов + проверка на попадание бомбы
    gun.draw()

    airship.move()
    airship.draw()
    
    for h in helicopters:
        h.move()
        h.draw()

    for p in planes:
        p.move()
        p.draw()
        
    for b in balls:
        b.move()
        b.draw()
        
    for t in triangls:
        t.move()
        t.draw()

    for bm in bombs:
        bm.move()
        if bm.hit(gun):
            bm.clash()
            health_tank = health_tank - 1
        if (bm.y >= (HEIGHT - 100)):
            bm.clash()
        bm.draw()

    for bg in bangs:
        bg.draw()

    for bs in buckshots:
        bs.move()
        bs.draw()

    pygame.display.update()    
    clock.tick(FPS)
    
    #Обработка событий от пользователя
    for event in pygame.event.get():
        
        #Желание досрочно закончить
        if event.type == pygame.QUIT:
            finished = True
            
        else:
            #Нажатие клавиши, приводящее к остановке пушки
            if event.type == pygame.KEYUP:
               gun.move_end(event)
            #Движение мыши, приводящее к прицеливанию пушки
            if event.type == pygame.MOUSEMOTION:
                gun.targetting(event)
            #Нажатие на кнопку мыши - подготовка к выстрелу
            if event.type == pygame.MOUSEBUTTONDOWN:
                gun.fire1_start(event)
            #Отпускание кнопки мыши, приводящее к выстрелу разрывным (1) или бронебойным (2)
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    gun.fire1_end(event)
                if event.button == 3:
                    gun.fire2_end(event)
            #Нажатие на пробел - сбрасывание бомбы с аэростата
            if event.type == pygame.KEYDOWN:              
                airship.fire(event)
    #Нажатие на стрелочки для движения пушки
    keys = pygame.key.get_pressed()
    gun.move(keys)

    #Проверка попадания бронебойного    
    for t in triangls:
        for h in helicopters:
            if t.hittest(h):
                h.create_helicopter()
                triangls.remove(t)
        for p in planes:
            if t.hittest(p):
                p.create_plane()
                triangls.remove(t)
        if t.hittest(airship):
            health_airship = health_airship - 1
            triangls.remove(t)
    #Проверка попадания разрывного, в неразорвавшемся виде        
    for b in balls:
        for h in helicopters:           
            if b.hittest(h):
                h.create_helicopter()
                balls.remove(b)
        for p in planes:
            if b.hittest(p):
                p.create_plane()
                balls.remove(b)
        if b.hittest(airship):
            health_airship = health_airship - 1
            balls.remove(b)

    #Проверка попадания картечи             
    for bs in buckshots:
        for h in helicopters:
            if bs.hittest(h):
                h.create_helicopter()
        for p in planes:
            if bs.hittest(p):
                p.create_plane()
        if bs.hittest(airship):
            health_airship = health_airship - 1
            buckshots.remove(bs)
        #Удаление картечи по прошествии некотрого времени            
        if bs.time >= 3:
            buckshots.remove(bs)

    #Увеличение силы выстрела, ели необходимо
    gun.power_up()

    #Проверка на конец игры - иссчение запаса здоровья пушки или аэростата
    if (health_tank <= 0) or (health_airship <= 0):
        finished = True

finished = False

#Третье окно (итоговое) - объявляет победителя
while not finished:
    screen.fill(BLACK)
    text5 = f5.render('ПОБЕДИТЕЛЬ' , True,
                  (255, 255, 255))
    screen.blit(text5, (350, 300))

    if health_tank <= 0:
        text6 = f6.render('Германия' , True,
                      (255, 255, 255))
        screen.blit(text6, (430, 400))
    elif health_airship <= 0:
        text6 = f6.render('Российская империя' , True,
                      (255, 255, 255))
        screen.blit(text6, (250, 400))
    else:
        text6 = f6.render('????' , True,
                      (255, 255, 255))
        screen.blit(text6, (490, 400))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        
    
pygame.quit()
