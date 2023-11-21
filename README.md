# iching2
Iching for quantitative trading version 2

# 1. 基于事件的交易系统
## 1.1. 程序启动
<details><summary>1. 程序的入口点为apps\forex\forex_app.py::main方法</summary>
会调用backtesting方法
</details>
<details><summary>1.1. 在apps\forex\forex_app.py::backtesting方法中</summary>
    <details><summary>1.1.1. 启动独立线程apps\forex\exchs\lmax_bar_repo.py::LmaxBarRepo.connect</summary>
    <ol>
    <li>从文件中读入Bar数据，将当前条写入ForexRepository.bars_queue，提供行情数据；</li>
<li>将下一条写入ForexRepository.next_bars_queue中，订单执行时用于估计订单的执行价；</li>
</ol>
在apps\forex\forex_repository.py::ForexRepository中维护三个事件：
<ol>
  <li>Bar事件：接收到Bar数据时执行，激活Trade事件，然后处于等待状态，直到本条Bar行情经过策略和订单（如果有）执行后，重新激活，取下一条Bar数据；</li>
  <li>Trade事件：接收到Bar数据后触发，调用策略模块产生订单，激活Order事件，置于等待状态；</li>
  <li>Order事件：执行订单逻辑，然后激活Bar事件，自己进入等待状态；</li>
</ol>
    </details>
    <details><summary>1.1.2. 启动独立线程apps\forex\trade_engine.py::TradeEngine.execute</summary>
    从apps\forex\forex_repository.py::ForexRepository.bars_queue中读取Bar行情，调用策略模块执行。产生市价买入或卖出的订单。
    清空Trade事件，激活Order事件，使Trade事件处于等待状态。
    </details>
    <details><summary>1.1.3. 启动独立线程apps\forex\order_engine.py::OrderEngine.processOrdersBackTesting</summary>
    从apps\forex\forex_repository.py::ForexRepository.next_bars_queue读出下一条bar数据，将其中的Close价格，加上一个指定值作为买入价，减去一个指定值作为卖出价。<br />
    根据Bar数据构造买n或卖n的Tick数据。<br />
    调用broker执行订单，并对用户的仓位和现金进行相应的修改。
    </details>
</details>

## 1.2. 趋势跟踪策略开发
### 1.2.1. 概述
我们认为市场可以分为：上升、下降、震荡，判断标准：
* 上升：收盘价在短期移动平均线之上，并且短期移动平均线在长期移动平均线之上；
* 下降：收盘价在短期移动平均线之下，并且短期移动平均线在长期移动平均线之下；
* 震荡：不在上述两种情形之下的情况；

趋势跟踪策略的要点：
1. 市场是否处于趋势中；
2. 趋势方向；
3. 进入时机；
4. 退出时机；

### 1.2.2. 品种选择
每种策略都有适合的市场和币值对，以趋势跟踪策略为例，就比较适合到澳大利亚元与日元AUDJPY、澳大利元与美元AUDUSD（美元利率低的时候）。因为澳大利亚元受金价和矿产品出口影响很明显，而这些产品具有明确的周期性。
对于趋势跟踪策略，日内如分钟级交易数据，由于人们交易习惯的原因，有很多假的趋势，会对识别真正的趋势造成影响，因此选择日K数据比较合适。
综上所述，我们选择AUDUSD，以日K数据为准，以USD为计价单位。
生成市场数据：
```bash
python -m apps.forex.strategies.trend_following_strategy
```
生成的数据集文件为：apps\forex\datasets\eurusd_1_tick.csv 。这里需要注意，00:00属于前一天，因为其表示23:59至00:00中间发生的行情数据。

### 1.2.3. 回测结果
采用AUDUSD货币对，2020-01-01至2022-12-13的日K行情数据进行回测，初始资金为50000美元和50000澳元，回测结果为：
```bash
Total trades: 289
Average trade: 65.89423169550165
Backtest complete in 3.0 second(s).
profit: 19043.432959999976
roi of year: 0.07465114704487268;
```
既最终的年化收益率为7%左右，共进行289次交易，平均每次交易盈利65美元，最终的利润为19043美金，实测效果还可以。

# Releases
* 2023.11.18 v0.0.1 Initial Import: Forex trading system for live trading and back testing
* 2023.11.21 v0.0.2 Add trend following strategy
