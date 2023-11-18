#
import argparse
from apps.ake.ake_app import AkeApp
import apps.lmax.forex_data as forex_data

def main(args:argparse.Namespace = {}) -> None:
    print(f'Iching2 v0.0.1')
    # app = AkeApp()
    # app.startup(args=args)
    forex_data.main(args=args)

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--run_mode', action='store', type=int, default=1, dest='run_mode', help='run mode')
    return parser.parse_args()

if '__main__' == __name__:
    args = parse_args()
    main(args=args)