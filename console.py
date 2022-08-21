# console rom management functions

"""
functions used to:
 - find unique game name
 - sort out by country
 - sort out by revision
"""

import os
import msg
import remote_host

# expunge roms by keyword
def purge(romlist,banned,debug):
    """remove roms using word from banned list in their filename"""
    clean = []
    for rom in romlist:
        found = False
        for key in banned:
            if key in rom:
                found = True
                break
        if found:
            msg.debug(f"SKIPPED:\tgame {rom}, keyword {key}",debug)
        else:
            clean.append(rom)
    return clean

# extract base name to create sets of similar game
def extract_basename(rom,debug):
    """extract base rom name from file name"""
    base_name = rom.split('(')[0] + '('
    msg.debug(f"FOUND:\tbase name is {base_name}",debug)
    return base_name

def create_sets(romlist,debug):
    """create sets per unique names"""
    fullset = []
    previous_basename = ''
    for rom in romlist:
        basename = extract_basename(rom,debug)
        if basename != previous_basename:
            gameset = []
            for rom in romlist:
                if basename in rom:
                    msg.debug(f"FOUND:\tadding rom {rom}",debug)
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
def find_country(game,country_list,country_index):
    game_country = []
    for rom in game:
        try:
            if country_list[country_index] in rom:
                game_country.append(rom)
        except IndexError:
            game_country.append(rom)
    if len(game_country)>0:
        return game_country
    else:
        # we test every country before pushing following a specific order
        while country_index < len(country_list):
            return find_country(game,country_list,country_index+1)

# select rom by country and revision
def select_unique(gamelist,country_list):
    dumps = []
    """find the most appropriate dump for each game"""
    for game in gamelist:
        # start with the first country in the list
        best = find_revision(find_country(game,country_list,0))
        dumps.append(best)
    return dumps

def trim_path(folder):
    if folder[-1] == '/':
        folder = folder.rstrip(folder[-1])
    return folder.split('/')[-1]

# main sync functions
def sync(folder,remote,banned_words,country_list,debug):
    local_folder = os.path.abspath(folder)
    """sync selected console roms to remote folder"""
    # list all roms in folder and remove some based on keywords
    romlist = purge(os.listdir(local_folder),banned_words,debug)
    # sort list
    romlist.sort()
    # create sets by game and select unique one
    romset = select_unique(create_sets(romlist,debug),country_list)
    # push romsets once they have been curated
    remote_host.pushromset(romset,local_folder,remote['rom_path'] + '/' + trim_path(local_folder),remote,debug)