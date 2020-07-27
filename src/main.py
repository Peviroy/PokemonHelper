import sys
import os
import argparse

from individuleOptimizer import individuleOptimizer
from positionDefiner import getPosData

os.chdir(os.path.split(os.path.realpath(__file__))[0])
sys.path.append(os.path.abspath("."))

parser = argparse.ArgumentParser(description="Pokemon automatic tool")
parser.add_argument('--mode', default='indiValue', type=str,
                    help='At present, "individule value optimizer"[indiValue] and "critical position definer"[posDefiner] are supported \
                                       the former is default while the latter mode should be done first')
parser.add_argument('--how_many_v', default=6, type=int,
                    help='[indiValue]you can choose to incubate 5v or less at first',
                    dest='v')
parser.add_argument('--pos_file', default='criPosition.json', type=str,
                    help='location of critical position file')


def main():
    """Operation hub
    """
    args = parser.parse_args()

    mode = args.mode
    if mode == 'indiValue':
        individuleOptimizer(getPosData(args.pos_file), how_many_v=args.v).run()
    elif mode == 'posDefiner':
        getPosData(args.pos_file, rewrite=True)


if __name__ == "__main__":
    main()
