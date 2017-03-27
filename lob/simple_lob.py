import numpy as np

lob_dim = 32
start_book_depth = 110.
start_midPrice = 100.
tick_size = 1.
lob_tick_depth = 0 * np.ones(lob_dim)
lob = start_book_depth + (lob_tick_depth * np.ones(lob_dim))

ord_range = (lob_dim - 1)//2

order = ['S', 105]

buy_range = range(ord_range + 1, lob_dim)
sell_range = range(ord_range, 0, -1)

def extrinRange(lob, the_range):
    for k in the_range:
        if lob[k] > 0:
            return k

def midPrice(lob, buy_range, sell_range):
    buy_min = start_midPrice + tick_size * extrinRange(lob, buy_range)
    sell_max = start_midPrice + tick_size * extrinRange(lob, sell_range)
    return (buy_min + sell_max)/2

def lob_order(lob, the_range, ord_residual):
    for k in the_range:
        lob_new =  lob[k] - ord_residual
        ord_hold =  - lob_new
        lob[k] = max(0, lob_new)
        if ord_hold <= 0. :
            break
        ord_residual = ord_hold
    return lob

print(midPrice(lob, buy_range, sell_range))

if order[0] == 'B':
    the_range = buy_range
else:
    the_range = sell_range

ord_residual = order[1]


lob = lob_order(lob, the_range, ord_residual)
print(lob)
print(midPrice(lob, buy_range, sell_range))

mids =   []

test_range = 50

for i in range(test_range):
    order = 50
    if (i <test_range/3 or i > 3*test_range/4):
        the_range = sell_range
    else:
        the_range = buy_range
    lob_order(lob, the_range, order)
    print(lob)
    mid = midPrice(lob, the_range, sell_range)
    print(mid)
    mids.append(mid)

import matplotlib.pyplot as plt
plt.plot(mids)
plt.ylabel('stock price')
plt.ylabel('time')
plt.show()








