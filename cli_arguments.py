# command-line arguments parsing

"""
manage command-line arguments
"""

import argparse

def parse():
    """the parsing mechanism"""
    parser = argparse.ArgumentParser(description="Manage romsets on handheld devices")
    parser.add_argument('-d','--debug', help='print out debug messages', action='store_true')
    parser.add_argument('directory', nargs='+', help='list of directories to sync with remote devices')

    args = parser.parse_args()

    return args