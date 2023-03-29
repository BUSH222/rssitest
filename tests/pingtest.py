from ping3 import ping, verbose_ping
import matplotlib.pyplot as plt
hostname = "192.168.1.254"
data = []
for i in range(50):
    try:
        attempts = []
        count = 0
        for i in range(100):
            attempts.append(ping(hostname))
            count += 1
        data.append(sum(attempts)/count)
        print('Good', end=' ', flush=True)
    except:
        data.append(0)
        print('ERROR', end=' ', flush=True)

plt.plot(data)
plt.show()