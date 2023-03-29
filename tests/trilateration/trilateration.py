from PIL import Image
import pygame
import requests
import json
from easy_trilateration.model import *  
from easy_trilateration.least_squares import easy_least_squares 
import easy_trilateration 
pygame.init()
clock = pygame.time.Clock()


routerposdict = {
    '24:a4:3c:7d:fc:f':[1215,841],
    '78:72:5d:69:a9:f':[2061, 1968],
    '78:72:5d:ca:6b:1':[1805, 1962],
    '78:72:5d:c4:52:b':[1357, 1962],
    '78:72:5d:6d:41:7':[1226, 1952],
    '78:72:5d:c4:58:a':[782, 2066],
    '78:72:5d:99:bc:a':[1393, 769],
    '78:72:5d:9a:31:c':[2223, 1002],
    '78:72:5d:9a:30:c':[1801, 998],
    '78:72:5d:c3:dd:c':[1568, 987],
    '78:72:5d:78:de:d':[1300, 332],
    '78:72:5d:9a:31:d':[751, 991],
    '78:72:5d:9a:2f:f':[762, 1243],
    '78:72:5d:9a:30:d':[742, 1258],
    '78:72:5d:ca:dd:f':[1042, 2059],
    '78:72:5d:c3:de:f':[1540, 1937],
    '78:72:5d:c4:52:d':[1746, 1638],
    '78:72:5d:c3:dc:a':[2058, 1314],
    '78:72:5d:69:4f:c':[789, 632],
    '78:72:5d:69:4b:0':[1494, 1304],
    '78:72:5d:c1:6e:9':[1369, 1315],
    '78:72:5d:69:4b:0':[1215, 1302],
    '24:a4:3c:7d:f8:9':[2347, 1222],
    '24:a4:3c:03:24:7':[1840, 1829],
    '24:a4:3c:7d:fc:f':[950, 1813],
}

pixelToMeterCoefficient = 27.5 #error margin 0.075 pixels per meter 


display = pygame.display.set_mode((1920,1080))
surface = pygame.Surface((3268, 2338))
background = pygame.image.load("clearfloors/floor-2.png").convert()
surface.blit(background, (0, 0))



surfcoords = [0, 0]
running = True
k = 1
count = 0
while running:
    
    if count % 600 == 0:
        surface.fill((0, 0, 0))
        surface = pygame.Surface((3268, 2338))
        background = pygame.image.load("clearfloors/floor-2.png").convert()
        surface.blit(background, (0, 0))

        try:
            data = requests.get('http://172.20.29.20:5000/receive')
            inp = json.loads(data.content)
            inp = dict(zip(inp.keys(), list(map(int, inp.values()))))
        except:
            inp = {}
            inp = dict(zip(inp.keys(), list(map(int, inp.values()))))
        inp2 = dict(inp)
        for key, value in inp2.items():
            inp[key[:-1]] = inp.pop(key)
        
        
        topop = []
        for key, value in inp.items():
            if value < -80 or key not in routerposdict.keys():
                topop.append(key)
        for s in topop:
            inp.pop(s)
        print(inp)
        funlist = []
        for key, value in inp.items():
            funlist.append(Circle(routerposdict[key][0], routerposdict[key][1], (2+10**((value+40)/(-10*2)))))
        result, meta = easy_least_squares(funlist)  
        
        pygame.draw.circle(surface, (255, 255, 0), (round(result.center.x), round(result.center.y)), round(abs(result.radius)))
        print((round(result.center.x), round(result.center.y)), round(abs(result.radius)))




    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT:
                k = 5
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT:
                k = 1
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        surfcoords[0] -= 5*k
    elif keys[pygame.K_LEFT]:
        surfcoords[0] += 5*k
    if keys[pygame.K_DOWN]:
        surfcoords[1] -= 5*k
    elif keys[pygame.K_UP]:
        surfcoords[1] += 5*k
    if keys[pygame.K_SPACE]:
        print(surfcoords)
    display.blit(surface, surfcoords)
    pygame.display.update()
    count += 1
    clock.tick(60)

pygame.quit()