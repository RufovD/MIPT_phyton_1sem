import pygame
from pygame.draw import *

#Функция, рисующая облако
def cloud(x, y, serost):
    ellipse(screen, (serost, serost, serost), (x, y, 300, 50))


#Функция, рисующая домик
def house(x, y, size, transparency):
    #Создадим новую поверхность для домиков, чтобы делать их прозрачными 
    surface = pygame.Surface((600, 800), pygame.SRCALPHA)
    
    #First floor
    rect(surface, (40, 34, 11, transparency), (x, y, size * 300, size * 250))
    rect(surface, (43, 17, 0, transparency), (x + 30 * size, y + 100 * size,
                                             size * 60, size * 90))
    rect(surface, (43, 17, 0, transparency), (x + 120 * size, y + 100 * size,
                                             size * 60, size * 90))
    rect(surface, (212, 170, 0, transparency), (x + 210 * size, y + 100 * size,
                                             size * 60, size * 90))
    #Second floor
    rect(surface, (43, 34, 0, transparency), (x, y - 200 * size,
                                             size * 300, size * 200))
    rect(surface, (72, 65, 55, transparency), (x + size * 30, y - size * 200,
                                              size * 30, size * 190))
    rect(surface, (72, 65, 55, transparency), (x + size * 100, y - size * 200,
                                              size * 30, size * 190))
    rect(surface, (72, 65, 55, transparency), (x + size * 170, y - size * 200,
                                              size * 30, size * 190))
    rect(surface, (72, 65, 55, transparency), (x + size * 240, y - size * 200,
                                              size * 30, size * 190))
    
    #Balcony
    rect(surface, (26, 26, 26, transparency), (x - 30 * size, y,
                                              size * 360, size * 40))
    rect(surface, (26, 26, 26, transparency), (x - 20 * size, y - size * 40,
                                              size * 10, size * 40))
    rect(surface, (26, 26, 26, transparency), (x + size * 20, y - size * 40,
                                              size * 20, size * 40))
    rect(surface, (26, 26, 26, transparency), (x + size * 80, y - size * 40,
                                              size * 20, size * 40))
    rect(surface, (26, 26, 26, transparency), (x + size * 140, y - size * 40,
                                              size * 20, size * 40))
    rect(surface, (26, 26, 26, transparency), (x + size * 200, y - size * 40,
                                              size * 20, size * 40))
    rect(surface, (26, 26, 26, transparency), (x + size * 260, y - size * 40,
                                              size * 20, size * 40))
    rect(surface, (26, 26, 26, transparency), (x + 310 * size, y - size * 40,
                                              size * 10, size * 40))
    rect(surface, (26, 26, 26, transparency), (x - 10 * size, y - size * 60,
                                              size * 320, size * 20))

    #Roof
    rect(surface, (26, 26, 26, transparency), (x + 160 * size, y - 260 * size,
                                              10 * size, 40 * size))
    polygon(surface, (0, 0, 0, transparency), ((x - 20 * size, y - 200 * size),
                                              (x + 320 * size, y - 200 * size),
                                              (x + 290 * size, y - 230 * size),
                                              (x + 10 * size, y - 230 * size)))
    rect(surface, (26, 26, 26, transparency), (x + 40 * size, y - 260 * size,
                                              10 * size, 40 * size))
    rect(surface, (26, 26, 26, transparency), (x + 60 * size, y - 280 * size,
                                              20 * size, 65 * size))
    rect(surface, (26, 26, 26, transparency), (x + 260 * size, y - 270 * size,
                                              10 * size, 50 * size))
    screen.blit(surface, (0, 0))


#Собираем данные по домикам
print('число домиков нижнего слоя')
n_house_down = int(input()) #количество домиков нижнего слоя

print('число домиков верхнего слоя')
n_house_up = int(input()) # количество домиков верхнего слоя

x_house = [] # координата по иксу его левого края
y_house = [] # координата по игреку его середины
size_house = [] # увеличение размеров домика в веденное количествол раз
proz_house = [] # прозрачность домика

for i in range(0, n_house_down + n_house_up):
    print('икс домика (координата по иксу его левого края)')
    x = int(input())
    x_house += [x]
    print('игрек домика (координата по игреку его середины)')
    y = int(input())
    y_house += [y]
    print('размер домика (увеличение его размеров в веденное количество раз)')
    size = float(input())
    size_house += [size]
    print('прозрачность домика (от 0 до 255)')
    proz = int(input())
    proz_house += [proz]


#Собираем данные по облакам
print('введите число облаков позади всех домиков')
n_cloud_behind = int(input()) #количество облаков позади всех домиков
      
print('введите число облаков между домами')
n_cloud_middle = int(input())
      
print('введите число облаков перед всеми домиками')
n_cloud_front = int(input()) #количество облаков перед всеми домиками
      
serost_cloud = [] #серость этих облаков      
x_cloud = [] # икс координата верхнего левого края облака
y_cloud = [] # игрек координата верхнего левого края облака
      
for i in range (0, n_cloud_behind + n_cloud_middle + n_cloud_front):
    print('введите серость облака (от до)')
    serost = int(input())
    serost_cloud += [serost]
    print('введите икс облака (координата левого края облака)')
    x = int(input())
    x_cloud += [x]
    print('введите игрек облака (координата верхнего края облака) ')
    y = int(input())
    y_cloud += [y]


#Начинаем рисовать
pygame.init()

FPS = 30
screen = pygame.display.set_mode((600, 800))

rect(screen, (120, 120, 120), (0, 0, 600, 350)) # фон
circle(screen, (255, 255, 255), (520, 80), 40) # рисует луну
      
#Облака (за всеми домиками)
for i in range(0, n_cloud_behind):
    cloud(x_cloud[i], y_cloud[i], serost_cloud[i])        


#Домики (дальний слой)
for i in range(0, n_house_down):
    house(x_house[i], y_house[i], size_house[i], proz_house[i])

    
#Облака (между домиками)
for i in range(n_cloud_behind, n_cloud_middle + n_cloud_behind):
    cloud(x_cloud[i], y_cloud[i], serost_cloud[i])        


#Домики (передний слой)
for i in range(n_house_down, n_house_down + n_house_up):
    house(x_house[i], y_house[i], size_house[i], proz_house[i])


#Облака (переди всех домиков)
for i in range(n_cloud_middle + n_cloud_behind, n_cloud_middle + n_cloud_behind + n_cloud_front):
    cloud(x_cloud[i], y_cloud[i], serost_cloud[i])        


pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
