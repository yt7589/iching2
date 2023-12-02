# Option Strategy Demo App
import argparse
from apps.osd.risk_free_arbitrage import RiskFreeArbitrage

def main(args:argparse.Namespace = {}) -> None:
    print(f'期权策略演示系统')
    start, end = 2800, 3100
    RiskFreeArbitrage._prepare_draw()
    # # 绘制单独买HO2312-C-2900时的盈亏图
    # RiskFreeArbitrage._draw_dsjctl_profit(
    #     RiskFreeArbitrage._calculate_profit, start, end,
    #     [
    #         {
    #             'option_type': 1,
    #             'executive_price': 2900,
    #             'option_price': 75.0, # 单位为点，规定为100元/点
    #             'share': 1
    #         }
    #     ],
    #     color='blue'
    # )
    # 绘制单独卖出HO2312-C-2950时的盈亏图
    # RiskFreeArbitrage._draw_dsjctl_profit(
    #     RiskFreeArbitrage._calculate_profit, start, end,
    #     [
    #         {
    #             'option_type': 2,
    #             'executive_price': 2950,
    #             'option_price': 61.5,
    #             'share': 2
    #         }
    #     ],
    #     color='red'
    # )
    # # 绘制单独买HO2312-C-3000时的盈亏图
    # RiskFreeArbitrage._draw_dsjctl_profit(
    #     RiskFreeArbitrage._calculate_profit, start, end,
    #     [
    #         {
    #             'option_type': 1,
    #             'executive_price': 3000,
    #             'option_price': 47.0,
    #             'share': 1
    #         }
    #     ],
    #     color='green'
    # )
    # 绘制总体盈亏图
    RiskFreeArbitrage._draw_dsjctl_profit(
        RiskFreeArbitrage._calculate_profit, start, end, 
        [
            {
                'option_type': 1,
                'executive_price': 2900,
                'option_price': 75.0,
                'share': 8
            },
            {
                'option_type': 2,
                'executive_price': 2950,
                'option_price': 61.5,
                'share': 16
            },
            {
                'option_type': 1,
                'executive_price': 3000,
                'option_price': 47.0,
                'share': 8
            }
        ],
        color='blue'
    )
    RiskFreeArbitrage._show_draw()

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    return parser.parse_args()

if '__main__' == __name__:
    args = parse_args()
    main(args=args)