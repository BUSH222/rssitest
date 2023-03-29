import re
import subprocess
import time
from pprint import pprint


def getallrssi():
    pipe = subprocess.Popen(['airport', '-s'], stdout=subprocess.PIPE)
    text = pipe.communicate()[0].decode('utf-8')
    rawlist = re.findall(r'\S*:\S*\s-\d*', text)
    data = []
    try:
        for f in rawlist:
            temp = f.split()
            rssi = temp[1]
            end = ':xx'
            start = temp[0][:-3]

            data.append([start, end, rssi])
        data.sort(key=lambda x: x[0])
        data = list(dict((x[0], x) for x in data).values())
        data = [[s[0]+s[1], int(s[2])]for s in data]
        data.sort(key=lambda x: x[1], reverse=True)
        pprint('Strongest signal rssi:', data[0][1])
        return data
    except Exception as e:
        print('tick failed', e)
        return None
    
