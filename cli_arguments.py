# command-line arguments parsing

"""
manage command-line arguments
"""

import argparse
import os


def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"{path} is not a valid path")

def parse():
    """the parsing mechanism"""
    parser = argparse.ArgumentParser(description="Manage romsets on handheld devices")
    parser.add_argument('-d','--debug', action='store_true', help='print out debug messages')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-c', '--console', nargs='*', type=dir_path, action='store', help='directory with console games')

    args = parser.parse_args()

    return args