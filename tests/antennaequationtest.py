import math
K = -27.55 #constant
Ptx = 0 # transmitter power (dbm) !!!
CLtx = 0 # cable loss (0 if no cables)
CLrx = 0 # cable loss (0 if no cables)
AGtx = 3 # antenna gain at transmitter, dBi
AGrx = 3 # antenna gain at receiver, dBi

mcstoprx = {0:-91, 1:-91, 2:-90, 3:-87, 4:-84, 5:-79, 6:-77, 7:-76, 8:-90, 9:-89, 10:-86, 11:-83, 12:-80, 13:-75, 14:-74, 15:-72}
# MCS channel to receiver sensitivity for 5 ghz HT20


Prx = 0 # receiver sensitivity, dBm
FM = 0 # fade margin, dB
f = 6755 # signal frequency, MHz (channel 161)


FSPL = Ptx - CLtx + AGtx + AGrx - CLrx - Prx - FM
d = 10 ** ((FSPL - K - 20 * math.log10(f)) / 20 )