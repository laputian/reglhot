import numpy as np
import math


lob_dim = 10
print_diagnostics = True

#Market order size
base_order = 100.
#LOB tick base size
tick_base_size = 200.
#Weber and Rosenow (2005)
w_r = 0.76 #0.76
func_exp = 1 + w_r
#func_exp = 2.


def market_order_on_lob(lob_def, order):
    ord_hold = order[1]
    if ord_hold <= 0.:
        return 0.,0.
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


def lob_def( slice = 0, exp  = func_exp, tick_base_size = tick_base_size ):
    return tick_base_size * (slice ** exp )

import matplotlib.pyplot as plt
def show_mids(mids, max, min):
    plt.plot(mids)
    plt.ylabel('stock price')
    plt.xlabel('time')
    plt.title("Limit order book trading")
    plt.ylim( max +2, min -2)
    plt.show()

def mo_func(k):
    exp_inv = 1. / (func_exp + 1)
    const = (func_exp + 1) ** (exp_inv)
    return const * (base_order ** exp_inv) / (tick_base_size ** (exp_inv)) * (k ** (exp_inv))

def test_market_order_on_lob(runs = 50, base_order = base_order, tick_base_size = tick_base_size ):
    exp_inv = 1. / (func_exp + 1)
    const = (func_exp + 1) ** (exp_inv)
    prices = []
    expl = mo_func(np.arange(runs));
    for k in range(runs):
        order = ['B', base_order * k]
        prices.append(market_order_on_lob(lob_def, order=order)[0])
    fig, ax = plt.subplots()
    ax.plot(expl, label="Function - Exp 1/" + str(round(func_exp + 1, 2)))
    ax.step(range(runs), prices, label="Limit order book")
    plt.title("Exp = " + str(round(func_exp, 2)))
    plt.xlabel('Market order size')
    plt.ylabel('Price difference')
    ax.legend(loc='lower center', shadow=True, fontsize='x-large')
    plt.show()


if __name__ == "__main__":
    test_market_order_on_lob()











