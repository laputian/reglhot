import numpy as np
import math


lob_dim = 10
print_diagnostics = True

#Market order size
base_order = 1000.
#LOB tick base size
exp_const = 200
func_exp = 1.


def market_order_on_lob(lob_def, order):
    ord_hold = order[1]
    tick = 0
    slice_depth = 0
    while(ord_hold  > 0):
        slice_depth = lob_def(slice  = tick)
        lob_new = slice_depth - ord_hold
        tick = tick + 1
        ord_hold = - lob_new
        if ord_hold  <= 0.:
            break
    return tick- 1 , slice_depth + ord_hold


def lob_def( slice = 0, exp  = func_exp):
    return exp_const * (slice ** exp )

import matplotlib.pyplot as plt
def show_mids(mids, max, min):
    plt.plot(mids)
    plt.ylabel('stock price')
    plt.xlabel('time')
    plt.title("Limit order book trading")
    plt.ylim( max +2, min -2)
    plt.show()

if __name__ == "__main__":
    exp_inv = 1./(func_exp + 1)
    const = (func_exp + 1) ** (exp_inv)
    prices = []
    expl = []
    runs = 50
    for k in range(50):
        order = ['B', base_order * k]
        prices.append(market_order_on_lob(lob_def, order = order)[0])
        expl.append(const *  (base_order ** exp_inv)/ (exp_const ** (exp_inv)) * (k ** (exp_inv)))
    fig, ax = plt.subplots()
    ax.plot(expl, label="Function - Exp 1/"+ str(func_exp + 1))
    ax.step(range(runs), prices, label="Limit order book")
    plt.title("Exp = " + str(func_exp))
    plt.xlabel('Market order size')
    plt.ylabel('Price difference')
    legend = ax.legend(loc='lower center', shadow=True, fontsize='x-large')
    plt.show()









