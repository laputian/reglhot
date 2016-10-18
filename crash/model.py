from security import Stock, Holding
from invest import Investor
from random import seed, randint, shuffle, sample
from market import trade
import matplotlib.pyplot as plt
import numpy as np
import itertools



def create_investors(nr = 20, cash_base=300., secu = None):
    invs = {}
    for i in range(1, nr+1):
        holding = Holding(secu, nr=randint(30, 70))
        invs[(i)] = Investor(id=i, cash=cash_base * randint(1, 9), holdings = {holding.security.id: holding})
    return invs

def calc_tot_assets(investors):
    tot_assets = 0.
    for inv in investors.itervalues():
        tot_assets += inv.tot_assets_value()
    print 'Tot assets ' +str(tot_assets)

def calc_tot_cash(investors):
    tot_cash = 0.
    for inv in investors.itervalues():
        tot_cash += inv.cash
    print 'Tot cash ' +str(tot_cash)

def trade_run(investors, num_sell =1, secu = None ):
    for pair in itertools.combinations(sample(investors.values(), len(investors.values())), r=2):
            success = trade(pair[0], pair[1], Holding(secu, num_sell) )
            if success:
                secu.price +=  secu.price/1000
            else:
                secu.price += -secu.price/1000
    return secu.price, success

def trade_run_iterate(investors, num_sell_success = 1, num_sell_fail = 2,  init_price = 85., runs = 1000, secu = None):
    plot_arr = [init_price]
    num_sell = num_sell_success
    for _ in range(runs):
        tr = trade_run(investors, num_sell, secu)
        plot_arr.append(tr[0])
        #if the transaction is successful, i.e. if there is enough liquidity,
        # then the number of stocks to be sold in the next transaction
        # is set to num_sell_success.
        if tr[1]:
            num_sell = num_sell_success
        # if the transaction is not successful, that is, if there is a liquidity problem,
        #  the number of stocks to be sold in the next transaction
        #  is set to num_sell_fail.
        # If num_sell_fail > num_sell_success one observes increased kurtosis,
        # corresponding to panic selling
        else:
            num_sell = num_sell_fail
    return plot_arr

def gauss(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

def test_run(init_price = 85., num_sell_success = 1, num_sell_fail = 1,
             the_seed = 393, tot_runs = 1000, nr_investors = 20, cash_base=300. ):
    print("Init: "+ str(nr_investors) + " investors, initial price = "+ str(init_price))
    seed(the_seed)
    secu = Stock(id='A', price=init_price)
    investors = create_investors(nr = nr_investors, cash_base=cash_base, secu = secu)
    calc_tot_assets(investors)
    calc_tot_cash(investors)

    a = []
    b = []
    c = []
    for inv in investors.values():
        a.append(int(inv.id))
        b.append(inv.tot_assets_value())
        c.append(inv.cash)
    plt.scatter(a, b, s=80, facecolors='none', edgecolors='r', label='Total value initial')
    plt.scatter(a, c, color='r', label='Initial cash')

    plot_arr = trade_run_iterate(investors, init_price = 85.,
                  num_sell_success=num_sell_success, num_sell_fail=num_sell_fail,  runs=tot_runs, secu = secu )

    print("Final")
    calc_tot_assets(investors)
    calc_tot_cash(investors)
    x = []
    y = []
    z = []
    for inv in investors.values():
        x.append(int(inv.id))
        y.append(inv.tot_assets_value())
        z.append(inv.cash)
    plt.scatter(x, y, s=80, facecolors='none', edgecolors='g', label='Total value final')
    plt.scatter(x, z, color='g', label='Final cash')
    plt.xticks(np.arange(1, len(investors) + 1, 1.0))
    plt.xlim(0, nr_investors + 1)
    plt.title("Assets and cash distribution per investor \n Init. price = " + str(init_price))

    plt.legend(loc = 2 ,scatterpoints = 1, prop={'size':10})
    plt.show()
    plt.plot(plot_arr)
    plt.title("Stock price \n Init. price = " + str(init_price))
    plt.xlabel("Period (day ..)")
    plt.ylabel("Price")
    plt.show()

    from scipy.stats import kurtosistest

    plot_diffs = np.asarray(plot_arr)
    plot_diffs = np.roll(plot_diffs, 1) - plot_diffs
    plot_diffs[0] = 0.
    count, bins, ignored = plt.hist(plot_diffs, 100, normed=True)
    mu = np.mean(plot_diffs)
    variance = np.var(plot_diffs)
    sigma = np.sqrt(variance)
    plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *
                 np.exp( - (bins - mu)**2 / (2 * sigma**2) ),
            linewidth=2, color='r')
    plt.title("Mean = "+str(mu) + " , std ="+str(sigma) +"\n Init. price = " + str(init_price))
    plt.xlabel("Jump size vs. frequency distribution \n Kurtosis test p-value = "+str(kurtosistest(plot_diffs)[1]))
    plt.ylabel("Jump Frequency")

    plt.gcf()
    plt.show()

if __name__ == "__main__":
    test_run()




