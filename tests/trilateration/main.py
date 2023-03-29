from PIL import Image
import pygame
import requests
import json
pygame.init()
clock = pygame.time.Clock()


class Ring():
    '''Creates a Ring instance, (x, y) are the center of the ring, (radin, radout) are the inner and outer radiuses of the ring'''
    def __init__(self, x, y, radin, radout):
        self.x = x
        self.y = y
        self.radin = radin
        self.radout = radout
    def checkpoint(self, h, k):
        '''checks if coordinates (h, k) are in Ring'''
        return self.radin**2 <= (h-self.x)**2 + (k-self.y)**2 <= self.radout**2
routerposdict = {
    '24:a4:3c:7d:fc:fb':[1215,841],
    '78:72:5d:69:a9:ff':[2061, 1968],
    '78:72:5d:ca:6b:1f':[1805, 1962],
    '78:72:5d:c4:52:bf':[1357, 1962],
    '78:72:5d:6d:41:7d':[1226, 1952],
    '78:72:5d:c4:58:ad':[782, 2066],
    '78:72:5d:99:bc:a0':[1393, 769],
    '78:72:5d:9a:31:cd':[2223, 1002],
    '78:72:5d:9a:30:c2':[1801, 998],
    '78:72:5d:c3:dd:cf':[1568, 987],
    '78:72:5d:78:de:d0':[1300, 332],
    '78:72:5d:9a:31:df':[751, 991],
    '78:72:5d:9a:2f:ff':[762, 1243],
    '78:72:5d:9a:30:df':[742, 1258],
    '78:72:5d:ca:dd:fc':[1042, 2059],
    '78:72:5d:c3:de:ff':[1540, 1937],
    '78:72:5d:c4:52:df':[1746, 1638],
    '78:72:5d:c3:dc:af':[2058, 1314],
    '78:72:5d:69:4f:c2':[789, 632],
    '78:72:5d:69:4b:00':[1494, 1304],
    '78:72:5d:c1:6e:9f':[1369, 1315],
    '78:72:5d:69:4b:0f':[1215, 1302],
    '24:a4:3c:7d:f8:92':[2347, 1222],
    '24:a4:3c:03:24:7d':[1840, 1829],
    '24:a4:3c:7d:fc:fc':[950, 1813],
    
}


area = (3272, 2339) #bottom left, top rigth
origin = (0, 0)
pointdist = 1/1

pixelToMeterCoefficient = 27.5 #error margin 0.075 pixels per meter 

im = Image.open('clearfloors/floor-2.png') 
im = im.convert('RGB')
pix = im.load()

width, height = im.size
print(width, height)
pixels = list(im.getdata())
pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]

display = pygame.display.set_mode((1920,1080))
surface = pygame.Surface((width, height))

exampleinput = {}

rings = []

for key, value in exampleinput.items():
    if key in list(routerposdict.keys()):
        print(key, value)
        rings.append(Ring(routerposdict[key][0], 27.5*routerposdict[key][1], 10**((value+40)/(-10*4))*27, 27.5*10**((value+40)/(-10*2))*27)+2)

def get_ring_intersection(rings, pointdist, area=(100, 100), origin=(0, 0)):
    max_intersection = -1
    
    xlim = round(area[0]/pointdist)
    ylim = round(area[1]/pointdist)
    funlist = [[] for _ in range(xlim)]
    for i in range(xlim):
        for j in range(ylim):
            a = 0
            for ring in rings:
                if ring.checkpoint(i*pointdist+origin[0], j*pointdist+origin[1]):
                    a += 1
            if a > max_intersection:
                max_intersection = a
            funlist[i].append(a)
    return funlist

def display_surf(exampleinput):
    surface.fill(pygame.Color(0, 0, 0, 0))
    rings = []

    for key, value in exampleinput.items():
        if key in list(routerposdict.keys()):
            print(key, value)
            rings.append(Ring(routerposdict[key][0], routerposdict[key][1], 27.5*(10**((value+40)/(-10*4))*27), 27.5*(10**((value+40)/(-10*2))*27+2)))

    maplist = get_ring_intersection(rings, 1, area=(3272, 2339))

    for i in range(height):
        for j in range(width):
            surface.set_at((j, i), (pixels[i][j][0], pixels[i][j][1], pixels[i][j][2]))

    maxv = max([max(s) for s in maplist])
    for i in range(len(maplist)):
        for j in range(len(maplist[i])):
            if maplist[i][j] != 0:
                if maplist[i][j] == maxv:
                    surface.set_at((i, j), (int(255/maplist[i][j]), 0, 0))

display_surf(exampleinput)

surfcoords = [0, 0]
running = True
k = 1
count = 0
while running:
    if count % 600 == 0:
        data = requests.get('http://172.20.29.20:5000/receive')
        inp = json.loads(data.content)
        inp = dict(zip(inp.keys(), list(map(int, inp.values()))))
        topop = []
        print(inp)
        for key, value in inp.items():
            if value < -75 or key not in routerposdict.keys():
                topop.append(key)
        for s in topop:
            inp.pop(s)
        display_surf(inp)
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