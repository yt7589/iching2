# 蝶式价差统计套利演示
from typing import Any, List
import numpy as np
import matplotlib.pyplot as plt            

class RiskFreeArbitrage(object):
    def __init__(self):
        self.name = 'apps.osd.risk_free_arbitrage.RiskFreeArbitrage'

    def _calculate_profit(spot_price:float, contracts:List) -> float:
        price = 0.0
        for contract in contracts:
            price += RiskFreeArbitrage._option_profit(
                option_type=contract['option_type'],
                spot_price=spot_price, 
                executive_price=contract['executive_price'], 
                option_price=contract['option_price'], 
                share=contract['share']
            )
        return price
    
    def _option_profit(option_type:int, spot_price:float, executive_price:float, option_price:float, share:int = 1) -> float:
        if option_type == 1:
            return RiskFreeArbitrage._call_option_profit(spot_price=spot_price, executive_price=executive_price, option_price=option_price, share=share)
        else:
            return RiskFreeArbitrage._put_option_profit(spot_price=spot_price, executive_price=executive_price, option_price=option_price, share=share)

    def _call_option_profit(spot_price:float, executive_price:float, option_price:float, share:int = 1) -> float:
        if spot_price <= executive_price:
            return -option_price*share
        else:
            return (spot_price - executive_price - option_price)*share
        
    def _put_option_profit(spot_price:float, executive_price:float, option_price:float, share:int = 1) -> float:
        if spot_price <= executive_price:
            return option_price*share
        else:
            return -(spot_price - executive_price - option_price)*share
        
    def _prepare_draw() -> None:
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = 'SimHei' # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号
        plt.figure(figsize=(5, 5),dpi=80)
    def _draw_dsjctl_profit(profit_func:Any, start:float, stop:float, contracts:List, color:str):
        x = np.linspace(start=start, stop=stop, num=100)
        y = [RiskFreeArbitrage._calculate_profit(xi, contracts=contracts) for xi in x]
        # 设置坐标轴区间
        plt.xlim(start, stop)
        # plt.ylim(-600, 1200)
        # 设置坐标轴标签
        plt.xlabel("现货价格")
        plt.ylabel("利润")
        plt.plot(x, y, color=color, ls='-', linewidth=2, alpha=1.0)
    def _show_draw() ->None:
        plt.show()
        
    