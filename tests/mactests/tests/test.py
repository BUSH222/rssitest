import re
import subprocess
import time
from pprint import pprint
#import matplotlib.pyplot as plt

t = 0
tickspeed = 3
threshold = -90




data = []
totaldata = []
while True:
    try:
        
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
            totaldata.append(data)
            pprint(data[0])
            t += tickspeed
            time.sleep(tickspeed)
        except Exception as e:
            print('tick failed', e)
            time.sleep(tickspeed)
        
    except KeyboardInterrupt:
        break

x = list(range(0, tickspeed*len(totaldata), tickspeed))

y = {}
for s in totaldata:
    for n in s:
        if n[0] in y.keys():
            if n[1] > threshold:
                y[n[0]].append(n[1])
            else:
                y[n[0]].append(-100)
        else:
            if len(y.values()) != 0:
                if n[1] > threshold:
                    y[n[0]] = [-100 for _ in range(len(max(y.values(), key=len))-1)] + [n[1]]
                else:
                    y[n[0]] = [-100 for _ in range(len(max(y.values(), key=len))-1)] + [-100]
            else:
                if n[1] > threshold:
                    y[n[0]] = [n[1]]
                else:
                    y[n[0]] = [-100]
    for key, value in y.items():
        if len(value) < len(max(y.values(), key=len)):
            y[key].append(-100)
            



# for key, value in y.items():
    
#     plt.plot(x, value + [-100 for _ in range(len(x) - len(value))], label=key)

# plt.legend()
# plt.show()


