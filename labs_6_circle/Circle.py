import json
import pygame
from pygame.draw import *
from random import randint
pygame.init()

"""Описание шариков"""
class Ball:

    """При появлении"""
    def __init__(self):

        self.x = randint(110, 1090)
        self.y = randint(210, 590)
        self.r = randint(10, 100)
        self.color = COLORS[randint(0, 5)]
        self.v_x = randint(50, 500)
        self.v_y  = randint(50, 500)

    """При движении"""    
    def position(self):
        
        self.x = self.x + self.v_x * ( 1 / FPS )
        self.y = self.y + self.v_y * ( 1 / FPS )
        circle(screen, self.color, (self.x, self.y), self.r)

    """При ударе"""   
    def ydar(self):
        
        if (self.x + self.r >= border_x) or (self.x - self.r <= 0):
            self.v_x = - self.v_x
        if (self.y + self.r >= border_y) or (self.y - self.r <= 100):
            self.v_y = - self.v_y
            
    """При нажатии"""
    def smert(self, coord_click):
        
        global c, norm_c
        c = 0
        norm_c = 0
        x_click = coord_click[0]
        y_click = coord_click[1]
        if (self.r)**2 >= (x_click - self.x)**2 + (y_click - self.y)**2 :
            c = 1 #обычный подсчет очков
            norm_c = int(( self.v_x**2 + self.v_y**2 ) / ( 50 * self.r )) #нормированный подсчет очков
            self.x = randint(110, 1090)
            self.y = randint(210, 590)
            self.r = randint(10, 100)
            self.color = COLORS[randint(0, 5)]
            self.v_x = randint(50, 500)
            self.v_y  = randint(50, 500)
            circle(screen, self.color, (self.x, self.y), self.r)

"""Описание приза - квадратика"""
class Prize:

    """При создании"""
    def __init__(self):

        global health
        health = 1        
        self.lenght = 50
        self.x = randint(10 + self.lenght, border_x - 10 - self.lenght)
        self.y = randint(100 + 10 + self.lenght, border_y - 10 - self.lenght)
        self.color = (VIOLET)

    """Пока существует"""
    def life(self):
        
        if health == 1:
            rect(screen, self.color, (self.x - self.lenght / 2, self.y - self.lenght / 2, self.lenght, self.lenght))

    """При нажатии"""
    def smert(self, coord_click):
        
        global bonus
        bonus = 0
        x_click = coord_click[0]
        y_click = coord_click[1]
        
        if (abs(self.x - x_click) < self.lenght / 2) and (abs(self.y - y_click) < self.lenght / 2):

            self.x = -1000
            self.y = -1000
            bonus = 250
            health = 0

"""Описание игровых параметров (Границ игровой области, времени раунда, FPS"""
border_x = 1200
border_y = 700
play_time = 20
FPS = 200

"""Обнуление накопительных параметров (счтечики, флага, времени)"""
counter = 0
norm_counter = 0
flag = 0
time = 0

"Описание используемых цветов"
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
WHITE = (255, 255, 255)
VIOLET = (148, 0, 211)

"Создание текстовых областей для печати"
f0 = pygame.font.Font(None, 100)
f1 = pygame.font.Font(None, 140)
f2 = pygame.font.Font(None, 140)
f3 = pygame.font.Font(None, 100)
f4 = pygame.font.Font(None, 100)
f5 = pygame.font.Font(None, 100)
f6 = pygame.font.Font(None, 100)
f7 = pygame.font.Font(None, 100)
f8 = pygame.font.Font(None, 100)
f9 = pygame.font.Font(None, 100)
f10 = pygame.font.Font(None, 500)
f11 = pygame.font.Font(None, 500)
f12 = pygame.font.Font(None, 500)
f13 = pygame.font.Font(None, 40)
f14 = pygame.font.Font(None, 40)
f15 = pygame.font.Font(None, 40)
f16 = pygame.font.Font(None, 40)
f17 = pygame.font.Font(None, 40)
f18 = pygame.font.Font(None, 40)


"""
Первая вступительняа часть с правилами и предложением
для пользователя ввести свой ник
"""

screen = pygame.display.set_mode((border_x, border_y))

text13 = f13.render('Ваша задача - набрать как можно больше очков. За каждый шарик можно получить ', True,
                (WHITE))
screen.blit(text13, (10, 10))
text14 = f14.render('от 1 до 1000 очков. Шарики меньших размеров с большими скоростями стоят больше. ', True,
                (WHITE))
screen.blit(text14, (10, 40))
text17 = f17.render('Игра длится 15 секунд. В последние 2 секунды у вас есть возможность получить ', True,
                (WHITE))
screen.blit(text17, (10, 70))
text18 = f18.render('бонус в 250 очков, нажав на появившийся фиолетовый квадратик. Не просмотри его! ', True,
                (WHITE))
screen.blit(text18, (10, 100))
text15 = f15.render('В правом угу экрана будет счетчик пойманных шариков. В центре сверху - счетчик ', True,
                (WHITE))
screen.blit(text15, (10, 130))
text16 = f16.render('ваших очков. Именно он и будет влиять на результат. Нажимайте на шарики. Удачи! ', True,
                (WHITE))
screen.blit(text16, (10, 160))        
text0 = f0.render('Введите ваш ник в консоль', True,
                (WHITE))
screen.blit(text0, (100, 350))
        
pygame.display.update()
        
print('введите ваш ник')
name = str(input())
        
screen.fill(BLACK)



pygame.display.update()
clock = pygame.time.Clock()
finished = False



"""Введение основных игровых объектов"""
ball_1 = Ball()
ball_2 = Ball()
ball_3 = Ball()
prizze = Prize()

"""Запуск основного игрового цикла"""
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True    
    """
    Таймер (обратный отсчет с тройки)
    """

    """три"""    
    if time <= 1:
        text10 = f10.render('3', True,
                        (255, 255, 255))
        screen.blit(text10, (550, 200))

        pygame.display.update()

        screen.fill(BLACK)

        time += 1/FPS

    """два"""    
    if (time > 1) and (time <= 2) :
        text11 = f11.render('2', True,
                        (255, 255, 255))
        screen.blit(text11, (520, 200))

        pygame.display.update()

        screen.fill(BLACK)    

        time += 1/FPS        
    """один"""    
    if (time > 2) and (time <= 3) :
        text12 = f12.render('1', True,
                        (255, 255, 255))
        screen.blit(text12, (520, 200))

        pygame.display.update()

        screen.fill(BLACK)

        time += 1/FPS
    
    """
    Начало игрового процесса
    """
    if (time > 3) and (time <= play_time + 3) :
            
        pygame.display.update()

        """Действия при клике"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            ball_1.smert(event.pos)
            counter += c
            norm_counter += norm_c
            
            ball_2.smert(event.pos)
            counter += c
            norm_counter += norm_c
            
            ball_3.smert(event.pos)
            counter += c
            norm_counter += norm_c

            if health == 1:
                prizze.smert(event.pos)
                norm_counter += bonus

        """Внешний вид (счетчики, смена кадра, прямоугольник для счетчиков)"""    
        screen.fill(BLACK)
        
        rect(screen, WHITE, (0, 0, 1200, 100))
        
        text1 = f1.render(str(counter), True,
                      (0, 0, 0))
        screen.blit(text1, (10, 5))
        
        text2 = f2.render(str(norm_counter), True,
                      (0, 0, 0))
        screen.blit(text2, (500, 5))

        """Анализ движения и положения"""
        ball_1.position()
        ball_1.ydar()
        ball_2.position()
        ball_2.ydar()
        ball_3.position()
        ball_3.ydar()

        if (time >= play_time + 3 - 2) and health == 1:
            prizze.life()
            
        """Тик времени"""
        time += 1/FPS



    """Финальный экран"""
    elif time > play_time + 3:

        """Вывод полученного результата игрока"""
        screen.fill(BLACK)
        text3 = f3.render('Ваш результат: ' + str(norm_counter) , True,
                      (255, 255, 255))
        screen.blit(text3, (10, 10))

        if flag == 0:            
            with open ('bestresults.json') as r1:
                results = json.load(r1)

            with open ('bestplayers.json') as p1:
                players = json.load(p1)

            for i in range(0, 5):
                if norm_counter > results[i]:
                    for j in range(3, i-1, -1):
                        results[j+1] = results[j]
                        players[j+1] = players[j]
                    results[i] = norm_counter
                    players[i] = name
                    break
            
            with open ('bestresults.json', 'w') as r2:
                json.dump(results, r2)

            with open ('bestplayers.json', 'w') as p2:
                json.dump(players, p2)
                
            flag += 1

        """Рейтинг"""
        text4 = f4.render('Лучшие результаты:' , True,
                      (WHITE))
        screen.blit(text4, (10, 200))
        text5 = f5.render('1. ' + str(players[0]) + ': ' + str(results[0]) , True,
                      (255, 215, 0))
        screen.blit(text5, (10, 280))
        text6 = f6.render('2. ' + str(players[1]) + ': ' + str(results[1]) , True,
                      (200, 200, 200))
        screen.blit(text6, (10, 350))       
        text7 = f7.render('3. ' + str(players[2]) + ': ' + str(results[2]) , True,
                      (205, 127, 50))
        screen.blit(text7, (10, 420))
        text8 = f8.render('4. ' + str(players[3]) + ': ' + str(results[3]) , True,
                      (WHITE))
        screen.blit(text8, (10, 490))
        text9 = f9.render('5. ' + str(players[4]) + ': ' + str(results[4]) , True,
                      (WHITE))
        screen.blit(text9, (10, 560))


        
        pygame.display.update()

        
pygame.quit()
