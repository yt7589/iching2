#
import argparse
import websocket

class LmaxApp(object):
    def __init__(self):
        self.name = 'apps.lmax.lmax_app.LmaxApp'

    def startup(self, args:argparse.Namespace = {}) -> None:
        print(f'外汇交易平台LMAX 1.0.0')
        url = "wss://public-data-api.london-demo.lmax.com/v1/web-socket"
        ws = websocket.WebSocket()
        ws.connect(url)
        req = '{"type": "SUBSCRIBE","channels": [{"name": "ORDER_BOOK","instruments": ["eur-usd"]},{"name": "TICKER","instruments":["usd-jpy"]}]}'
        ws.send(req)
        while True:
            print(ws.recv())
            print('************************')

def main(args:argparse.Namespace = {}) -> None:
    app = LmaxApp()
    app.startup(args=args)

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--run_mode', action='store', type=int, default=1, dest='run_mode', help='run mode')
    return parser.parse_args()

if '__main__' == __name__:
    args = parse_args()
    main(args=args)

'''
from datetime import datetime
ts_str1 = '2022-07-29T11:10:54.755Z'
ts1 = datetime.strptime(ts_str1, '%Y-%m-%dT%H:%M:%S.%fZ')
'''