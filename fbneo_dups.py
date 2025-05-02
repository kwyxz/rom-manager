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
import zipfile

def die(message):
    print(f"ERROR: {message}")
    sys.exit(1)

def is_konami2p(rom,exclude):
    """verify if game is konami game"""
    for k,v in enumerate(exclude):
        if exclude[v] + '.zip' == os.path.basename(rom):
            return True
    return False

def delete_clones(clones,exclude):
    """delete the clone roms"""
    for rom in clones:
        try:
            os.remove(f"{rom}")
        except IsADirectoryError:
            try:
                shutil.rmtree(f"{rom}")
            except FileNotFoundError:
                die(f"could not delete {rom}")
        except FileNotFoundError:
            if is_konami2p(rom,exclude):
                pass
            else:
                die(f"could not delete {rom}")
        else:
            if VERBOSE:
                print(f"Deleted clone: {rom}")
            pass

def delete_bootlegs(romfolder,bootlegdb):
    """delete bootlegs, hacks, etc"""
    romlist = os.scandir(romfolder)
    for rom in romlist:
        baserom = rom.name.split('.')[0]
        ext = rom.name.split('.')[1]
        if baserom in bootlegdb:
            try:
                os.remove(f"{romfolder}/{rom.name}")
                if VERBOSE:
                    print(f"Deleted bootleg: {rom.name}")
            except FileNotFoundError:
                die(f"could not delete {romfolder}/{rom.name}")

def build_clonedb(root):
    """create database of clones"""
    clonedb = {}
    for game in root:
        clonedb[game.attrib.get('name')] = game.attrib.get('cloneof')
    return clonedb

def build_bootlegdb(root):
    """create database of bootlegs, hacks, etc"""
    bootlegs = []
    for game in root:
        if game.findtext('comment'):
            bootlegs.append(game.attrib.get('name'))
    return bootlegs

def find_clones(romfolder, clonedb, exclude):
    """find list of clones in folder"""
    clonelist = []
    romlist = os.scandir(romfolder)
    for rom in romlist:
        try:
            baserom = rom.name.split('.')[0]
            ext = rom.name.split('.')[1]
            if baserom in exclude:
                if os.path.exists(f"{ROMFOLDER}/{clonedb[baserom]}.{ext}"):
                    clonelist.append(f"{ROMFOLDER}/{clonedb[baserom]}.{ext}")
            else:
                if clonedb[baserom]:
                    clonelist.append(f"{ROMFOLDER}/{rom.name}")
        except KeyError:
            clonelist.append(f"{ROMFOLDER}/{rom.name}")
    return clonelist

def build_konami(romfolder,konami2p):
    """rebuild zipfiles for 2p versions of Konami games"""
    # looking at list of 2p konami roms
    for childrom in konami2p.keys():
        # if the parent still exists create a temp folder
        if os.path.exists(f"{romfolder}/{konami2p[childrom]}.zip"):
            if os.path.isdir(f"{romfolder}/{childrom}"):
                shutil.rmtree(f"{romfolder}/{childrom}")
            os.mkdir(f"{romfolder}/{childrom}")
            # unzip the 2p child
            with zipfile.ZipFile(f"{romfolder}/{childrom}.zip", 'r') as childzip:
                childzip.extractall(path=f"{romfolder}/{childrom}")
            # unzip the 3p/4p parent
            with zipfile.ZipFile(f"{romfolder}/{konami2p[childrom]}.zip", 'r') as parentzip:
                parentzip.extractall(path=f"{romfolder}/{childrom}")
            # zip everything back under the child name
            shutil.make_archive(f"{romfolder}/{childrom}", 'zip', root_dir=f"{romfolder}/{childrom}", base_dir='.')
            # delete the temp folder
            shutil.rmtree(f"{romfolder}/{childrom}")

def main():
    """main loop"""
    build_konami(ROMFOLDER,KONAMI2P)
    CLONEDB = build_clonedb(ROOT)
    CLONES = find_clones(ROMFOLDER,CLONEDB,KONAMI2P)
    BOOTLEGDB = build_bootlegdb(ROOT)
    delete_clones(CLONES,KONAMI2P)
    delete_bootlegs(ROMFOLDER,BOOTLEGDB)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='media_helper',
        description='find missing media and attempt to merge it from duplicates')
    parser.add_argument('-x', '--xml', nargs=1, type=open, action='store', required=True, help='FBNeo XML or DAT data file')
    parser.add_argument('-d', '--directory', nargs=1, type=pathlib.Path, action='store', required=True, help='directory of FBNeo roms')
    parser.add_argument('-v', '--verbose',action='store_true', help='increase verbosity')

    ARGS = parser.parse_args()
    DATFILE=ARGS.xml[0]
    ROMFOLDER = ARGS.directory[0]
    VERBOSE = ARGS.verbose

    KONAMI2P = {
        'esckidsj': 'esckids',
        'punkshot2': 'punkshot',
        'simpsons2p3': 'simpsons',
        'ssridersubc': 'ssriders',
        'tmnt2po': 'tmnt',
        'tmnt22pu': 'tmnt2',
        'vendetta2pw': 'vendetta',
        'xmen2pu': 'xmen'
    }
    try:
        TREE = ET.parse(DATFILE)
    except FileNotFoundError:
        die(f"XML file {DATFILE} not found")
    ROOT = TREE.getroot()
    main()
    sys.exit(0)
