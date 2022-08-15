#!/usr/bin/env python3

"""
manage roms on specific devices
"""

import os
import yaml
import cli_arguments

### Error messages
def msg_error(msg):
    """print an error message"""
    print(f"\033[31mERROR\033[m: {msg}")

### Info messages
def msg_info(msg):
    """print an info message"""
    print(f"\033[33mINFO\033[m: {msg}")

def msg_debug(msg):
    """print only in verbose mode"""
    if args.debug:
        print(f"\033[33mDEBUG\033[m: {msg}")
    else:
        pass

### OK messages
def msg_ok(msg):
    """print an OK message"""
    print(f"\033[32mOK\033[m: {msg}")

### romlist management functions
def purge(romlist):
    """remove roms using word from banned list in their filename"""
    banned = [
        'BIOS',
        'Enhancement Chip',
        '(Unl',
        '(Demo',
        '(Hack',
        '(Program',
        '(Beta',
        '(NP',
        '(Alt',
        'Virtual Console',
        'Switch Online',
        'Channel)',
        'Collection)'
    ]
    clean = []
    for rom in romlist:
        found = False
        for key in banned:
            if key in rom:
                found = True
                break
        if found:
            msg_debug(f"banned rom {rom} due to keyword {key}")
        else:
            clean.append(rom)
    return clean

def extract_basename(rom):
    """extract base rom name from file name"""
    return rom.split('(')[0] + '('

def create_sets(romlist):
    """create sets per unique names"""
    fullset = []
    previous_basename = ''
    for rom in romlist:
        msg_debug(f"extracting game name from {rom}")
        basename = extract_basename(rom)
        msg_debug(f"base name {basename}")
        if basename == previous_basename:
            msg_debug(f"set for {basename} already taken care of")
        else:
            gameset = []
            for rom in romlist:
                if basename in rom:
                    gameset.append(rom)
                    previous_basename = basename
            fullset.append(gameset)
    msg_ok(fullset)
    return fullset

def sync_roms(folder):
    """list roms in folder"""
    folder_romlist = os.listdir(folder)
    folder_romlist = purge(folder_romlist)
    msg_error(folder_romlist)
    folder_romlist.sort()
    romlist_sets = create_sets(folder_romlist)

### settings management ###
def load_settings():
    """load settings from global conf file or local conf file"""
    user_settings = "$HOME/.config/rom-manager/settings.yaml"
    if os.path.exists(user_settings):
        settings_file = user_settings
    else:
        settings_file = 'settings.yaml'
    with open(settings_file) as file:
        msg_debug(f"loading settings file {settings_file}")
        return yaml.safe_load(file)

### main loop ###
def main(args,settings):
    """main function"""
    if args.console:
        for folder in args.console:
            msg_debug(f"checking folder {folder}")
            sync_roms(folder)

if __name__ == "__main__":
    args = cli_arguments.parse()
    settings = load_settings()
    main(args,settings)