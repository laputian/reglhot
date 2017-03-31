import numpy as np

lob_dim = 10
start_book_depth = 110.
start_midPrice = 100.
tick_size = 5.
lob = start_book_depth + np.zeros(lob_dim)
num_step =10

print_diagnostics = True

ord_range = (lob_dim - 1)//2

ord_load = 135

order = ['S', ord_load]

if print_diagnostics:
    print(lob)

buy_range = range(ord_range + 1, lob_dim + 1)
sell_range = range(ord_range, -1, -1)

#index of the first first non zero entry in a range
def extrinRange(lob, the_range):
    for k in the_range:
        if lob[k] > 0:
            return k
    return -1

def midPrice(lob, buy_range, sell_range, ord_range = ord_range):
    buy_min = start_midPrice + tick_size * (extrinRange(lob, buy_range) - ord_range)
    sell_max = start_midPrice - tick_size * (ord_range - extrinRange(lob, sell_range))
    if print_diagnostics:
        print(order[0])
        print('extr in sell range', extrinRange(lob, sell_range))
        print('sell_max', sell_max)
        print('extr in buy range',extrinRange(lob, buy_range))
        print('buy_min', buy_min)
    return (buy_min + sell_max)/2.

def resetLob(lob, buy_range, sell_range):
    buy_index = extrinRange(lob, buy_range)
    sell_index = extrinRange(lob, sell_range)
    print(buy_index, sell_index)


def lob_order(lob, the_range, ord_residual, ord_range = ord_range):
    for k in the_range:
        lob_new =  lob[k] - ord_residual
        ord_hold =  - lob_new
        lob[k] = max(0, lob_new)
        if ord_hold <= 0. :
            break
        ord_residual = ord_hold
    extr = extrinRange(lob, the_range)
    lob_c = lob.copy()
    step = ord_range - extr + 1
    if step > 0:
        for h in range(step if step > 1 else 0):
            lob[ord_range - h] = lob_c[ord_range - step -h + 1]
    else:
        for h in range(-step + 1):
            lob[ord_range + h +1] = lob_c[ord_range - step + h + 1]
    if print_diagnostics:
        print(lob)
        print('extreme for this order', extrinRange(lob, the_range))
    return lob



def market_run(lob = lob, test_range = num_step, buy_range = buy_range, sell_range = sell_range, order = order)  :
    mids = []
    for i in range(test_range):
        if (order[0] =='S'):
            the_range = sell_range
        else:
            the_range = buy_range
        lob = lob_order(lob, the_range, order[1])
        mid = midPrice(lob, buy_range, sell_range)
        if print_diagnostics:
            print('mid', mid)
        mids.append(mid)
    return lob, mids





import matplotlib.pyplot as plt
def show_mids(mids):
    plt.plot(mids)
    plt.ylabel('stock price')
    plt.xlabel('time')
    plt.title("Limit order book trading")
    plt.ylim(85,110)
    plt.show()

if __name__ == "__main__":
    lob, mids = market_run(lob, num_step, buy_range, sell_range, order)
    if order[0] == 'B':
        order[0]  = 'S'
    else:
        order[0] = 'B'
    mids = mids + market_run(lob, num_step, buy_range, sell_range, order)[1]
    show_mids(mids=mids)














