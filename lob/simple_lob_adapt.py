import numpy as np

lob_dim = 10
book_depth = 110.
start_midPrice = 100.
tick_size = 1.
lob = book_depth + np.zeros(lob_dim)
num_step =50

print_diagnostics = True

ord_range = (lob_dim - 1)//2

ord_load = 35

order = ['B', ord_load]

if print_diagnostics:
    print('load_order', ord_load)
    print(lob)

buy_range = range(ord_range + 1, lob_dim + 1)
sell_range = range(ord_range, -1, -1)

#index of the first first non zero entry in a range
def extrinRange(lob, the_range):
    for k in the_range:
        if lob[k] > 0:
            return k
    return -1


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
        step = - step + 1
    else:
        for h in range(-step + 1):
            lob[ord_range + h +1] = lob_c[ord_range - step + h + 1]
        step = -step
    if print_diagnostics:
        print(order[0])
        print('step = ', step)
        print(lob)
        print('extreme for this order', extrinRange(lob, the_range))
    return lob, step



def market_run(lob = lob, test_range = num_step, buy_range = buy_range, sell_range = sell_range, order = order, price = start_midPrice)  :
    mids = []
    steptot = 0
    for i in range(test_range):
        if (order[0] =='S'):
            the_range = sell_range
        else:
            the_range = buy_range
        lob, step = lob_order(lob, the_range, order[1])
        steptot = steptot + step
        priceTot = price  + steptot * tick_size
        mids.append(priceTot)
    return lob, mids, priceTot





import matplotlib.pyplot as plt
def show_mids(mids, max, min):
    plt.plot(mids)
    plt.ylabel('stock price')
    plt.xlabel('time')
    plt.title("Limit order book trading")
    plt.ylim( max +2, min -2)
    plt.show()

if __name__ == "__main__":
    lob, mids, priceTot = market_run(lob, num_step, buy_range, sell_range, order)
    if order[0] == 'B':
        order[0]  = 'S'
    else:
        order[0] = 'B'
    mids = [start_midPrice] + mids + market_run(lob, num_step, buy_range, sell_range, order, price = priceTot)[1]
    max, min = np.amax(mids),  np.amin(mids)
    show_mids(mids=mids, max = max, min = min)














