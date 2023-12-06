# command-line arguments parsing

"""
manage command-line arguments
"""

import argparse
import os


def dir_path(path):
    """test if path is valid"""
    if os.path.isdir(path):
        return path
    raise argparse.ArgumentTypeError(f"{path} is not a valid path")

def parse():
    """the parsing mechanism"""
    parser = argparse.ArgumentParser(description="Manage romsets on handheld devices")
    parser.add_argument(
        '-n',
        '--noop',
        action='store_true',
        help='do not actually upload anything, only display projected upload'
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='print out debug messages'
    )
    hardware = parser.add_mutually_exclusive_group(required=True)
    hardware.add_argument(
        '-l',
        '--listhw',
        action='store_true',
        help='list remote hardwares'
    )
    hardware.add_argument(
        '-r',
        '--remote',
        type=str,
        action='store',
        help='name of remote hardware'
    )
    parser.add_argument(
        '-c',
        '--console',
        nargs='+',
        type=dir_path,
        action='append',
        metavar='<console roms directory>',
        help='directory with console games'
    )
    parser.add_argument(
        '-a',
        '--arcade',
        nargs='+',
        action='append',
        metavar='<arcade game name>',
        help='name of an arcade game'
    )
    args = parser.parse_args()
    return args
