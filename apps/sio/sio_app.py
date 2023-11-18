#
import argparse
from apps.sio.monte_carlo import MonteCarlo

def main(args:argparse.Namespace = {}) -> None:
    print(f'股指期权平台 v0.0.1')
    MonteCarlo.init_app()
    MonteCarlo.startup()

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--run_mode', action='store', type=int, default=1, dest='run_mode', help='run mode')
    return parser.parse_args()

if '__main__' == __name__:
    args = parse_args()
    main(args=args)