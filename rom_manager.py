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
    banned = settings['banned_words']
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
        basename = extract_basename(rom)
        if basename != previous_basename:
            gameset = []
            for rom in romlist:
                if basename in rom:
                    gameset.append(rom)
                    previous_basename = basename
            fullset.append(gameset)
    return fullset

def find_revision(game):
    game.sort()
    revisions = []
    for rom in game:
        # find revisions
        if '(Rev' in rom:
            revisions.append(rom)
    if len(revisions)>0:
        revisions.sort()
        # use the latest revision
        return revisions[-1]
    return game[-1]

def find_country(game,country_index):
    game_country = []
    for rom in game:
        try:
            if settings['country_list'][country_index] in rom:
                game_country.append(rom)
        except IndexError:
            game_country.append(rom)
    if len(game_country)>0:
        return game_country
    else:
        # we test every country before pushing following a specific order
        while country_index < len(settings['country_list']):
            return find_country(game,country_index+1)

def select_unique(folder):
    dumps = []
    """find the most appropriate dump for each game"""
    for game in folder:
        # start with the first country in the list
        best = find_revision(find_country(game,0))
        dumps.append(best)
    return dumps

def sync_consoleroms(folder):
    """sync selected roms to remote folder"""
    # list all roms in folder
    folder_romlist = os.listdir(folder)
    # remove unwanted roms
    folder_romlist = purge(folder_romlist)
    # sort list
    folder_romlist.sort()
    # create sets by game
    folder_romlist = create_sets(folder_romlist)
    msg_debug(folder_romlist)
    # select unique game by country and revision
    folder_romlist = select_unique(folder_romlist)
    msg_ok(folder_romlist)

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
            sync_consoleroms(folder)

if __name__ == "__main__":
    args = cli_arguments.parse()
    settings = load_settings()
    main(args,settings)
