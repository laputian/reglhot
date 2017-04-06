# See M. Avellaneda and S. Stoikov "High-frequency trading in a limit order book" at https://www.math.nyu.edu/faculty/avellane/HighFrequencyTrading.pdf

import math

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
def test_poisson():
    tot = 0
    for k in range(10):
        s = np.random.poisson(1)
        tot = tot + s
        print(s)
    print(tot)

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




class my_pdf(st.rv_continuous):
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

def test_distrib():
    my_cv = my_pdf(a=1, b=100, name='my_pdf')
    print(my_cv.expect(f))
    print(my_cv.cdf(1.1))
    a = my_cv.rvs(size=100)
    b = np.zeros((100))
    for k in range(100):
        b[k] = 100*my_cv.gabaix_func(k+2)
    print(a)
    plt.plot(b)
    plt.plot(a)
    plt.show()

if __name__ == "__main__":
    test_distrib()



