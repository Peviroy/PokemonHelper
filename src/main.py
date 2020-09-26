import sys
import os
import argparse
import textwrap

from modes.individuleOptimizer import individuleOptimizer
from modes.positionDefiner import PostionDefiner
from modes.eggFlasher import eggFlasher

os.chdir(os.path.split(os.path.realpath(__file__))[0])
sys.path.append(os.path.abspath("."))

parser = argparse.ArgumentParser(description="Pokemon automatic tool",
                                 formatter_class=argparse.RawTextHelpFormatter)
subparser_mode = parser.add_subparsers(dest='mode', required=True,
                                       help=textwrap.dedent('''\
                                            Now three modes are supported:
                                                [indiValue]"individule value optimizer",
                                                [posDefiner]"critical position definer--foundation of this script",
                                                [eggFlasher]"pokemon egg flash observer"\
                                        '''))
parser.add_argument('-F', default='criPosition.json', type=str,
                    help='location of critical position file; use "criPosition.json" for default',
                    metavar='--pos_file',
                    dest='pos_file')
parser.add_argument('-P', default='mobile', type=str,
                    choices=['mobile', 'desktop'],
                    help='game operation platform: mobile or pc',
                    metavar='--platform',
                    dest='platform')


subparser_posDefiner = subparser_mode.add_parser(
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
subparser_posDefiner.add_argument('-A', default='', type=str,
                                  help='[posDefiner]define what. default is for pos, "Flash" for flash point, "Indivalue" for indivalue area',
                                  metavar='--addon',
                                  dest='addon')
subparser_posDefiner.add_argument('-R', default=False, type=bool,
                                  help='[posDefiner]Wheter to rewrite json file',
                                  metavar='--rewrite',
                                  dest='rewrite')


def main():
    """Operation hub
    """
    args = parser.parse_args()

    mode = args.mode
    posDefiner = PostionDefiner(args.pos_file)
    if mode == 'posDefiner':
        posDefiner.run(args.platform, addon=args.addon, rewrite=args.rewrite)
    elif mode == 'indiValue':
        posData = posDefiner.run(args.platform)
        individuleOptimizer(posData,
                            how_many_v=args.v,
                            egg_pos=args.egg_pos,
                            platform=args.platform).run()
    elif mode == 'eggFlasher':
        posData = posDefiner.run(args.platform)
        eggFlasher(posData,
                   platform=args.platform).run()


if __name__ == "__main__":
    main()
