import sys
import os
import argparse

from individuleOptimizer import individuleOptimizer
from positionDefiner import getPosData
from eggFlasher import eggFlasher

os.chdir(os.path.split(os.path.realpath(__file__))[0])
sys.path.append(os.path.abspath("."))

parser = argparse.ArgumentParser(description="Pokemon automatic tool",
                                 epilog="This program is not easy to use, please be patient.")
parser.add_argument('--mode', default='posDefiner', type=str,
                    help='At present, "individule value optimizer"[indiValue], "critical position definer"[posDefiner], "pokemon egg flash observer"[eggFlasher] are supported \
                                       the former is default while the latter mode should be done first')
parser.add_argument('--how_many_v', default=6, type=int,
                    help='[indiValue]you can choose to incubate 5v or less at first',
                    dest='v')
parser.add_argument('--egg_pos', default=1, type=int,
                    help='[indiValue]the position of egg at right column of pokemon bag')
parser.add_argument('--pos_file', default='criPosition_pc.json', type=str,
                    help='location of critical position file')
parser.add_argument('--platform', default='mobile', type=str,
                    help='game operation platform:mobile or pc')


def main():
    """Operation hub
    """
    args = parser.parse_args()

    mode = args.mode
    if mode == 'indiValue':
        individuleOptimizer(getPosData(
            args.pos_file, addon='Indivalue'), how_many_v=args.v, egg_pos=args.egg_pos, platform=args.platform).run()
    elif mode == 'posDefiner':
        getPosData(args.pos_file, rewrite=True, addon='Indivalue')
    elif mode == 'eggFlasher':
        eggFlasher(getPosData(args.pos_file, addon='Flash'),
                   platform=args.platform).run()


if __name__ == "__main__":
    main()
