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

area = (3272, 2339) #bottom left, top rigth
origin = (0, 0)
pointdist = 1/1

rings = []



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
    print(len(funlist))
    
    with open('textfile.txt', 'w') as funfile:
        funfile.write('\n'.join([str(p) for p in funlist]))
    print(max_intersection)

get_ring_intersection(rings, pointdist, area)

