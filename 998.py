from mpmath import *


mp.dps = 3
count = 0
for i in range(1005):
    x = mpf(1)/998001
    dig = int((x * 10 ** mp.dps) % 1000)
    if count != dig:
        break
    count += 1
    mp.dps += 3
print(count)
