#!/usr/bin/env python3

"""
manage roms on specific devices
"""

import os
import sys
import yaml
import cli_arguments

### output

# error messages
def msg_error(msg):
    """print an error message"""
    print(f"\033[31mERROR\033[m: {msg}")

# info messages
def msg_info(msg):
    """print an info message"""
    print(f"\033[33mINFO\033[m: {msg}")

# debug messages
def msg_debug(msg):
    """print only in verbose mode"""
    if args.verbose:
        print(f"\033[33mDEBUG\033[m: {msg}")
    else:
        pass

# OK messages
def msg_ok(msg):
    """print an OK message"""
    print(f"\033[32mOK\033[m: {msg}")

### settings management ###

def load_settings():
    """load settings from global conf file or local conf file"""
    user_settings = "$HOME/.config/rom-manager/settings.yaml"
    if os.path.exists(user_settings):
        settings_file = user_settings
    else:
        # ideally use a local file because this is weak
        settings_file = 'settings.yaml'
    with open(settings_file) as file:
        msg_debug(f"loading settings file {settings_file}")
        return yaml.safe_load(file)

### rom management functions

# expunge roms by keyword
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

# extract base name to create sets of similar game
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

# select rom by revision
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

# select rom by country
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

# select rom by country and revision
def select_unique(folder):
    dumps = []
    """find the most appropriate dump for each game"""
    for game in folder:
        # start with the first country in the list
        best = find_revision(find_country(game,0))
        dumps.append(best)
    return dumps

# push roms to remote
def push_ssh(folder,remote):
    msg_debug(f"SSH push to {remote['user']}@{remote['ip_addr']}:{remote['port']}/{remote['rom_path']}")

def push_ftp(folder,remote):
    msg_debug(f"FTP push to {remote['user']}@{remote['ip_addr']}:{remote['port']}/{remote['rom_path']}")

def push_to_remote(folder):
    # remote is exclusive in options
    remote_host = settings['remote_hw'][args.remote]
    if remote_host['protocol'] == 'ssh':
        push_ssh(folder,remote_host)
    elif remote_host['protocol'] == 'ftp':
        push_ftp(folder,remote_host)
    else:
        msg_error("something went very wrong")
        sys.exit(1)

# main sync functions
def sync_consoleroms(folders):
    """sync selected console roms to remote folder"""
    for folder in folders:
        # list all roms in folder and remove some based on keywords
        folder_romlist = purge(os.listdir(folder))
        # sort list
        folder_romlist.sort()
        # create sets by game and select unique one
        folder_romlist = select_unique(create_sets(folder_romlist))
        return push_to_remote(folder_romlist)

def sync_arcaderoms(folders):
    """sync selected arcade roms to remote folder"""
    # generate list of clones using MAME
    msg_debug('arcade')

### main loop ###
def main(args,settings):
    """main function"""
    if args.listhw:
        for key,value in enumerate(settings['remote_hw']):
            print(f"\n\033[1mremote\033[m: {value}")
            # remote hardware will always be useful
            x = settings['remote_hw'][value]
            print(f"\t({x['name']})")
            print(f"\t{x['protocol']}@{x['ip_addr']}:{x['port']}")
            print(f"\t{x['rom_path']}")
        sys.exit(0)
    else:
        try:
            if args.console:
                for folder in args.console:
                    sync_consoleroms(folder)
            elif args.arcade:
                for folder in args.arcade:
                    sync_arcaderoms(folder)
            else:
                msg_error(f"argument error")
                sys.exit(1)
        except KeyError:
            msg_error(f"{args.remote} is not a valid remote identifier")

if __name__ == "__main__":
    args = cli_arguments.parse()
    settings = load_settings()
    main(args,settings)
