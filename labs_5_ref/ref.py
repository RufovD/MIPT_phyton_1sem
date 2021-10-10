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


#Функция, рисующая призраков
def ghost(x, y, size, transparency, orientation):
    #New surface so we can make it transparent
    surface = pygame.Surface((600, 800), pygame.SRCALPHA)

    #We set a relative coordinates for outline of ghost
    coords = ((x - orientation * size * 15, y),
              (x - orientation * size * 17, y + size * 24),
              (x - orientation * size * 20, y + size * 40),
              (x - orientation * size * 30, y + size * 50 ),
              (x - orientation * size * 35, y + size * 65 ),
              (x - orientation * size * 37, y + size * 80 ),
              (x - orientation * size * 33, y + size * 85 ),
              (x - orientation * size * 25, y + size *  82),
              (x - orientation * size * 15, y + size * 87),
              (x - orientation * size * 8, y + size *  89),
              (x - orientation * size * 0, y + size *  89),
              (x + orientation * size * 7, y + size *  85),
              (x + orientation * size * 16, y + size * 85),
              (x + orientation * size * 22, y + size *  87),
              (x + orientation * size * 28, y + size * 87),
              (x + orientation * size * 34, y + size * 80),
              (x + orientation * size * 40, y + size * 76),
              (x + orientation * size * 46, y + size * 72),
              (x + orientation * size * 48, y + size * 65),
              (x + orientation * size * 52, y + size * 60),
              (x + orientation * size * 52, y + size * 52),
              (x + orientation * size * 48, y + size * 49),
              (x + orientation * size * 40, y + size * 40),
              (x + orientation * size * 38, y + size * 34),
              (x + orientation * size * 35, y + size * 30),
              (x + orientation * size * 30, y + size *  26),
              (x + orientation * size * 25, y + size * 21),
              (x + orientation * size * 21, y + size * 15),
              (x + orientation * size * 20, y + size * 12),
              (x + orientation * size * 17, y + size * 8),
              (x + orientation * size * 12, y + size * 4),
              )

    #Grey polygon and black aalines follow these coordinates
    polygon(surface, (179, 179, 179, transparency), coords)
    aalines(surface, (0, 0, 0, transparency), True, coords)

    #Head and eyes
    circle(surface, (179, 179, 179, transparency),
           (x - size * orientation * 5, y + size * 10), size * 17)
    circle(surface, (135, 205, 222, transparency),
           (x - size * orientation * 15, y + size * 10), size * 4)
    circle(surface, (0, 0, 0, transparency),
           (x - size * orientation * 16, y + size * 10), size * 1.5)
    circle(surface, (135, 205, 222, transparency),
           (x + size * orientation * 2, y + size * 5), size * 4)
    circle(surface, (0, 0, 0, transparency),
           (x + size * orientation * 1, y + size * 5), size * 1.5)

    #Draw diagonal ellipses on new surfaces which will be rotated
    ellipse_surface = pygame.Surface((size * 3, size * 2), pygame.SRCALPHA)
    ellipse(ellipse_surface, (255, 255, 255, transparency),
            (0, 0, size * orientation * 3, size * 2))
    ellipse_surface = pygame.transform.rotate(ellipse_surface, 30 * orientation)
    surface.blit(ellipse_surface, (x - size * orientation * 17, y + size * 7))

    ellipse_surface = pygame.Surface((size * 3, size * 2), pygame.SRCALPHA)
    ellipse(ellipse_surface, (255, 255, 255, transparency),
            (0, 0,
             size * orientation * 3, size * 2))
    ellipse_surface = pygame.transform.rotate(ellipse_surface, 30 * orientation)
    surface.blit(ellipse_surface, (x, y + size * 2))
    
    screen.blit(surface, (0, 0))



#Собираем данные по домикам
    
print('введите число домиков нижнего слоя')
n_house_down = int(input()) #количество домиков нижнего слоя

print('введите число домиков верхнего слоя')
n_house_up = int(input()) # количество домиков верхнего слоя

x_house = [] # координата по иксу левого края домика
y_house = [] # координата по игреку середины домика
size_house = [] # увеличение размеров домика в веденное количествол раз
proz_house = [] # прозрачность домика

for i in range(0, n_house_down + n_house_up):
    
    print('введите икс домика (координата по иксу левого края домика)')
    x = int(input())
    x_house += [x]
    
    print('введите игрек домика (координата по игреку середины домика)')
    y = int(input())
    y_house += [y]
    
    print('введите размер домика (увеличение размеров домика в веденное количество раз)')
    size = float(input())
    size_house += [size]
    
    print('введите прозрачность домика (от 10 до 255)')
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
    
    print('введите серость облака (от 0 до 200)')
    serost = int(input())
    serost_cloud += [serost]
    
    print('введите икс облака (координата левого края облака)')
    x = int(input())
    x_cloud += [x]
    
    print('введите игрек облака (координата верхнего края облака)')
    y = int(input())
    y_cloud += [y]


#Собираем данные по призракам
    
print('введите число призраков')
n_ghost = int(input()) #количество призраков

x_ghost = [] # икс призрака (икс середины его головы)
y_ghost = [] # игрек призрака (игрек середины его головы)
orientation_ghost = [] # отвечает за поворот призрака
size_ghost = [] # размер призрака (увеличение его размеров в веденное количесвто раз)
proz_ghost = [] # прозрачность призрака (от 0 до 255)

for i in range(0, n_ghost):
    
    print('введите икс призрака (икс середины его головы)')
    x = int(input())
    x_ghost += [x]

    print('введите игрек призрака (игрек середины его головы)')
    y = int(input())
    y_ghost += [y]

    print('введите 1, если призрак смотри налево; -1, если направо')
    orientation = int(input())
    orientation_ghost += [orientation]

    print('введите размер призрака (увеличение его размеров в веденное количесвто раз)')
    size = float(input())
    size_ghost += [size]

    print('введите прозрачность призрака (от 10 до 255)')
    proz = int(input())
    proz_ghost += [proz]



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

#Призраки
for i in range(0, n_ghost):
    ghost(x_ghost[i], y_ghost[i], size_ghost[i], proz_ghost[i], orientation_ghost[i])



pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
