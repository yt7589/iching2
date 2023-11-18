#
import argparse
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import akshare as ak
import warnings
from apps.sio.app_registry import AppRegistry
import apps.sio.monte_carlo_util as mcu

class MonteCarlo(object):
    @staticmethod
    def init_app():
        # plt.style.use('seaborn')
        # plt.style.use('seaborn-colorblind') #alternative
        plt.rcParams['figure.figsize'] = [8, 4.5]
        plt.rcParams['figure.dpi'] = 300
        warnings.simplefilter(action='ignore', category=FutureWarning)
        AppRegistry.set('plt', plt)

    @staticmethod
    def startup(args:argparse.Namespace = {}) -> None:
        # MonteCarlo.price_simulate()
        MonteCarlo.option_valuation()

    @staticmethod
    def option_valuation() -> None:
        S_0 = 100
        K = 100
        r = 0.05
        sigma = 0.50
        T = 1 # 1 year
        N = 252 # 252 days in a year
        dt = T / N # time step
        N_SIMS = 1000000 # number of simulations 
        discount_factor = np.exp(-r * T)
        bsa_call_price = mcu.black_scholes_analytical(S_0=S_0, K=K, T=T, r=r, sigma=sigma, type='call')
        print(f'### bsa_price: {bsa_call_price};')
        gbm_sims = mcu.simulate_gbm(s_0=S_0, mu=r, sigma=sigma, 
                       n_sims=N_SIMS, T=T, N=N)
        premium = discount_factor * np.mean(np.maximum(0, gbm_sims[:, -1] - K))
        print(f'### premium: {premium};')
        bsa_put_price = mcu.black_scholes_analytical(S_0=S_0, K=K, T=T, r=r, sigma=sigma, type='put')
        print(f'### bsa_put_price: {bsa_put_price};')
        p1 = MonteCarlo.european_option_simulation(S_0, K, T, r, sigma, N_SIMS, type='put')
        print(f'### p1: {p1};')

    @staticmethod
    def european_option_simulation(S_0, K, T, r, sigma, n_sims, type):
        rv = np.random.normal(0, 1, size=n_sims)
        S_T = S_0 * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * rv)

        if type == 'call':
            payoff = np.maximum(0, S_T - K)
        elif type == 'put':
            payoff = np.maximum(0, K - S_T)
        else: 
            raise ValueError('Wrong input for type!')
            
        premium = np.mean(payoff) * np.exp(-r * T)
        return premium

    @staticmethod
    def price_simulate() -> None:
        # 模拟某个合约日K线（相对收益率）
        df = ak.option_cffex_sz50_daily_sina(symbol="ho2312P3200")
        df['date'] = pd.to_datetime(df['date']) # date转为时间格式
        df = df.set_index('date')
        print(df)
        print(f'Downloaded {df.shape[0]} rows of data.')
        adj_close = df['close']
        returns = adj_close.pct_change().dropna()
        print(f'returns: \n{returns};')

        ax = returns.plot()
        ax.set_title(f'price simulation', 
                    fontsize=16)

        plt.tight_layout()
        plt.savefig('ch6_im1.png')
        plt.show()

        print(f'Average return: {100 * returns.mean():.2f}%')
        train = returns['2023-01-30':'2023-10-15']
        test = returns['2023-10-16':'2023-11-06']
        T = len(test)
        N = len(test)
        S_0 = adj_close[train.index[-1]]
        N_SIM = 100
        mu = train.mean()
        sigma = train.std()
        # run the simulation
        gbm_simulations = mcu.simulate_gbm(S_0, mu, sigma, N_SIM, T, N)
        # draw the result
        # prepare objects for plotting 
        last_train_date = train.index[-1].date()
        first_test_date = test.index[0].date()
        last_test_date = test.index[-1].date()
        plot_title = (f'Price Simulation '
                    f'({first_test_date}:{last_test_date})')

        selected_indices = adj_close[last_train_date:last_test_date].index
        index = [date.date() for date in selected_indices]

        gbm_simulations_df = pd.DataFrame(np.transpose(gbm_simulations), 
                                        index=index)

        # plotting
        ax = gbm_simulations_df.plot(alpha=0.2, legend=False)
        line_1, = ax.plot(index, gbm_simulations_df.mean(axis=1), 
                        color='red')
        line_2, = ax.plot(index, adj_close[last_train_date:last_test_date], 
                        color='blue')
        ax.set_title(plot_title, fontsize=16)
        ax.legend((line_1, line_2), ('mean', 'actual'))
        plt.tight_layout()
        plt.savefig('ch6_im2.png')
        plt.show()