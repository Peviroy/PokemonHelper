import sys
import os
import argparse
import textwrap

from individuleOptimizer import individuleOptimizer
from positionDefiner import getPosData
from eggFlasher import eggFlasher

os.chdir(os.path.split(os.path.realpath(__file__))[0])
sys.path.append(os.path.abspath("."))

parser = argparse.ArgumentParser(description="Pokemon automatic tool",
                                 formatter_class=argparse.RawTextHelpFormatter,
                                 epilog="This program is not easy to use, please be patient.")
subparser_mode = parser.add_subparsers(dest='mode', required=True,
                                       help=textwrap.dedent('''\
                                            Now three modes are supported:
                                                [indiValue]"individule value optimizer",
                                                [posDefiner]"critical position definer",
                                                [eggFlasher]"pokemon egg flash observer"\
                                        '''))
parser.add_argument('-F', type=str,
                    help='location of critical position file; if not given, use "criPosition_pc.json" or "criPosition.json" for default',
                    metavar='--pos_file',
                    dest='pos_file')
parser.add_argument('-P', default='mobile', type=str,
                    choices=['mobile', 'pc'],
                    help='game operation platform: mobile or pc',
                    metavar='--platform',
                    dest='platform')


subparser_mode.add_parser(
    'posDefiner', help="helper for define critical position and keyboard")
subparser_mode.add_parser(
    'eggFlasher', help="helper for get flash pokemon")
subparser_indiValue = subparser_mode.add_parser(
    'indiValue', help="For next, define 'egg position'[-E] and the 'exact v count'[-V] you want")

subparser_indiValue.add_argument('-V', default=6, type=int, required=True,
                                 help='[indiValue]you can choose to incubate 5v or less at first',
                                 metavar='--how_many_v',
                                 dest='v')
subparser_indiValue.add_argument('-E', default=1, type=int,
                                 help='[indiValue]the position of egg at right column of pokemon bag',
                                 metavar='--egg_pos',
                                 dest='egg_pos')


def main():
    """Operation hub
    """
    args = parser.parse_args()

    # deal with positionFile according to platform
    if args.platform == 'mobile':
        args.pos_file = 'criPosition.json'
    else:
        args.pos_file = 'criPosition_pc.json'

    mode = args.mode
    if mode == 'indiValue':
        individuleOptimizer(getPosData(
            args.pos_file, addon='Indivalue'), how_many_v=args.v, egg_pos=args.egg_pos, platform=args.platform).run()
    elif mode == 'posDefiner':
        getPosData(args.pos_file, rewrite=True, addon='Flash')
    elif mode == 'eggFlasher':
        eggFlasher(getPosData(args.pos_file, addon='Flash'),
                   platform=args.platform).run()


if __name__ == "__main__":
    main()
