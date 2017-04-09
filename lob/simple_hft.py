# See M. Avellaneda and S. Stoikov "High-frequency trading in a limit order book" at https://www.math.nyu.edu/faculty/avellane/HighFrequencyTrading.pdf

import math


from lob.simple_lob_func import lob_def, market_order_on_lob, base_order

#Final Time
T=1.0

#volatility
sigma = 0.2
#parameter
gamma = 1.
e=math.e


# The agent's value function
def nu(x, s, q, t):
    -e**(-gamma*x)*e**(-gamma*q*s)*e**(0.5*(T-t)*((gamma*q*s)**2))

# The agent's reservation price
def res_p(type, s, q, t):
    z = gamma*(sigma**2)*(T-t)
    if type=='a': #ask
        return s + (1-2*q)*z/2
    elif type=='b': #bid
        return s + (-1-2*q)*z/2
    elif type=='i': #indifference
        return s - q * z
    assert (False), "Wrong type."


# The agent's stationary reservation price
def res_p(type, s, q, omega):
    den = 2 * omega - (gamma**2)*(sigma**2)*(q**2)
    assert (den>0.), "Denominator must be positive."
    if type=='a': #ask
        return s + 1/gamma *(1 +((1-2*q)*(gamma**2)*(sigma**2)/den))
    elif type=='b': #bid
        return s + 1 / gamma * (1 + ((-1 - 2 * q) * (gamma ** 2) * (sigma ** 2) / den))
    else:
        assert (False), "Wrong type"

#distribution of market order size, alpha = 1.5 in Gabaix et al.
def distr_mos(size = 100., alpha= 1.5):
    if size >0:
        return size**(-alpha)
    else:
        return 1.

import numpy as np
def test_poisson_1():
    tot = 0
    for k in range(10):
        s = np.random.poisson(1)
        tot = tot + s
        print(s)
    print(tot)

def test_poisson_2():
    s = np.random.poisson(1, 10)
    print(s)
    print(s.sum())


import matplotlib.pyplot as plt
def plot_size():
    arr = np.zeros((100))
    for size in range (100):
        arr[size]=distr_mos(size=(size+1)/100000)
    plt.title("Order size density" )
    plt.xlabel("Size")
    plt.ylabel("Probability")
    plt.plot(arr)
    plt.show()

import scipy.stats as st
from scipy.integrate import quad

class market_order_pdf(st.rv_continuous):
    gabaix_exp = 1.53
    def gabaix_func(self, x):
        if x >= 1:
            return x**(- self.gabaix_exp)
        else:
            return 0.

    def _pdf(self,x):
        return self.gabaix_func(x)/self.gabaix_exp #/self.measure_integral()[0]# Normalized over its range, in this case [0,1]


def f(x):
    return 1

def test_distrib_1(the_base_order_size = base_order):
    the_upper_bound = math.inf
    the_range = 100
    mko_cv = market_order_pdf(a=1, b=the_upper_bound, name='mko_pdf')
    # print(mko_cv.expect(f))
    # print(mko_cv.cdf(1.1))
    a = mko_cv.rvs(size=the_range)
    b = np.zeros((the_range))
    for k in range(the_range):
        b[k] = the_base_order_size * mko_cv.gabaix_func(k + 2)
    print(a)
    plt.title("Order Sizes and density function for x > 1.  Mean = " + str(round(a.sum()/the_range, 2)))
    plt.xlabel("Iterator")
    plt.ylabel("Order site and density value")
    plt.plot(b)
    plt.plot(a)
    plt.show()

import seaborn as sns

def test_mko_pdf():
    the_upper_bound = math.inf
    mko_cv = market_order_pdf(a=1, b=the_upper_bound, name='mko_pdf')
    a = mko_cv.rvs(size=1000)
    sns.distplot(a, bins=10, kde=False, rug=True)
    plt.show()

def distrib_with_poisson(nr_of_orders=2000, the_base_order_size = base_order):
    print('Starting ...')
    the_upper_bound = math.inf
    s = np.random.poisson(1, nr_of_orders)
    s_tot = s.sum()
    mko_cv = market_order_pdf(a=1, b=the_upper_bound, name='mko_pdf')
    tot_a = np.zeros((nr_of_orders))
    for k in range(nr_of_orders):
        k_tot = 0.
        for j in range(s[k]):
            b = -1;
            a = random.randint(0, 1)
            if a:
                b = 1
            k_tot = b * mko_cv.rvs() + k_tot
        tot_a[k] = abs(k_tot)
    print('Finished creating the market order distribution')
    return the_base_order_size*tot_a, s


def test_distrib_with_poisson(dp, plot_hist = False):
    if plot_hist:
        sns.distplot(dp[0], bins=10, kde=False, rug=True)
    else:
        plt.title("Order Sizes and and number of orders.  Mean = " + str(round(dp[0].sum() / dp[1].sum(), 2)))
        plt.xlabel("Iterator")
        plt.ylabel("Total order site and number of orders")
        plt.plot(dp[1])
        plt.plot(dp[0])
    plt.show()


def full_market_run(start_price = 2000., nr_of_orders=2000, the_base_order_size = base_order):
    order = ['S', 0.]
    order_sizes, hits = distrib_with_poisson(nr_of_orders, the_base_order_size)
    gl = np.zeros((order_sizes.size))
    prices = np.zeros((order_sizes.size))
    for k in range(order_sizes.size):
        a = random.randint(0, 1)
        if a:
            order[0] = 'B'
        else:
            order[0] = 'S'
            a = -1
        order[1] = order_sizes[k]
        gain_loss = a * market_order_on_lob(lob_def, order)[0]
        start_price = start_price + gain_loss
        gl[k] = gain_loss
        print(order[1])
        prices[k] = start_price
    return prices, gl

import random

if __name__ == "__main__":
    #test_distrib_with_poisson(distrib_with_poisson(), plot_hist=False)
    prices, gl = full_market_run(start_price = 2000.)
    #plt.plot(prices)
    sns.distplot(gl, bins=10, kde=False, rug=True)
    plt.show()








