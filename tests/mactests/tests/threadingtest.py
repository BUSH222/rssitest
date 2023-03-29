import re
import subprocess
import time
from pprint import pprint
import threading


def bruhbruhb():
    global data
    while True:
        pipe = subprocess.Popen(['airport', '-s'], stdout=subprocess.PIPE)
        text = pipe.communicate()[0].decode('utf-8')
        rawlist = re.findall(r'\S*:\S*\s-\d*', text)
        for f in rawlist:
            temp = f.split()
            rssi = temp[1]
            end = temp[0][-3:]
            start = temp[0][:-3]

            data.append([start, end, rssi])
        data.sort(key=lambda x: x[0])
        data = list(dict((x[0], x) for x in data).values())
        data = [[s[0]+s[1], int(s[2])]for s in data]
        data.sort(key=lambda x: x[1], reverse=True)
        
        pprint(data)
        time.sleep(5)


data = []
t = threading.Thread(target=bruhbruhb)

t.start()
