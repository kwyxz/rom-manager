#!/usr/bin/env python3

"""
remove clones and bootlegs from fbneo rom folder
"""

import argparse
import os
import shutil
import sys
import xml.etree.ElementTree as ET
import pathlib

def die(message):
    print(f"ERROR: {message}")
    sys.exit(1)

def delete_clones(clones):
    """delete the clone roms"""
    for rom in clones:
        try:
            os.remove(f"{rom}")
        except IsADirectoryError:
            try:
                shutil.rmtree(f"{rom}")
            except FileNotFoundError:
                die(f"unable to delete {rom}, does the file exist?")
        else:
            print(f"SUCCESS: deleted {rom}")

def build_db(root):
    clonedb = {}
    for game in root:
        clonedb[game.attrib.get('name')] = game.attrib.get('cloneof')
    return clonedb

def find_clones(romfolder, clonedb, exclude):
    clonelist = []
    romlist = os.scandir(romfolder)
    for rom in romlist:
        try:
            baserom = rom.name.split('.')[0]
            ext = rom.name.split('.')[1]
            if baserom in exclude:
                clonelist.append(f"{ROMFOLDER}/{clonedb[baserom]}.{ext}")
            else:
                if clonedb[baserom]:
                    clonelist.append(f"{ROMFOLDER}/{rom.name}")
        except KeyError:
            clonelist.append(f"{ROMFOLDER}/{rom.name}")
    return clonelist

def main():
    """main loop"""
    CLONEDB = build_db(ROOT)
    CLONES = find_clones(ROMFOLDER,CLONEDB,EXCLUDE)
    delete_clones(CLONES)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='media_helper',
        description='find missing media and attempt to merge it from duplicates')
    parser.add_argument('-x', '--xml', nargs=1, type=open, action='store', required=True, help='FBNeo XML or DAT data file')
    parser.add_argument('-d', '--directory', nargs=1, type=pathlib.Path, action='store', required=True, help='directory of FBNeo roms')

    ARGS = parser.parse_args()
    DATFILE=ARGS.xml[0]
    ROMFOLDER = ARGS.directory[0]

    EXCLUDE = ['esckidsj', 'punkshot2', 'simpsons2p3', 'ssridersubc', 'tmnt2po', 'tmnt22pu', 'vendetta2pw', 'xmen2pu']
    try:
        TREE = ET.parse(DATFILE)
    except FileNotFoundError:
        die(f"XML file {DATFILE} not found")
    ROOT = TREE.getroot()
    main()
    sys.exit(0)
