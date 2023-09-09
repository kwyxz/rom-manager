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
        for banword in banned:
            if banword in rom:
                found = True
                break
        if found:
            msg.debug(f"SKIPPED:\tgame {rom}, keyword {banword}",debug) # pylint: disable=undefined-loop-variable
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
        if basename.lower() != previous_basename.lower():
            gameset = []
            for game in romlist:
                if basename in game:
                    msg.debug(f"FOUND:\tadding rom {game}",debug)
                    gameset.append(game)
                    previous_basename = basename
            fullset.append(gameset)
    return fullset

# select rom by revision
def find_revision(game,allow_translations,debug):
    """find most recent revision of game"""
    msg.debug(f"Looking at {game}",debug)
    game.sort()
    revisions = []
    if allow_translations:
        translations = []
        adds = []
    for rom in game:
        # find revisions or versions
        if '(Rev' or '(v.' in rom:
            revisions.append(rom)
        if allow_translations:
            # find translations of Japanese games
            if ('Japan' and '[T-En') in rom:
                translations.append(rom)
            # find addendums to translations
            if ('Japan' and '[T-En' and '[Add') in rom:
                adds.append(rom)
    if allow_translations:
        if len(adds)>0:
            adds.sort()
            # use the latest add to translation
            return adds[-1]
        if len(translations)>0:
            translations.sort()
            # use the latest translation
            return translations[-1]
    if len(revisions)>0:
        revisions.sort()
        # use the latest revision
        return revisions[-1]
    return game[-1]

# select rom by country
def find_country(game,country_list,country_index):
    """find most appropriate country based off list in settings"""
    game_country = []
    for rom in game:
        try:
            if country_list[country_index] in rom:
                game_country.append(rom)
        except IndexError:
            game_country.append(rom)
    if len(game_country)>0:
        return game_country
    # we test every country before pushing following a specific order
    while country_index < len(country_list):
        return find_country(game,country_list,country_index+1)

# select rom by country and revision
def select_unique(gamelist,country_list,allow_translations,debug):
    """find the most appropriate dump for each game"""
    dumps = []
    for game in gamelist:
        # start with the first country in the list
        best = find_revision(find_country(game,country_list,0),allow_translations,debug)
        dumps.append(best)
    return dumps

def trim_path(folder):
    """trim folder path and keep last"""
    if folder[-1] == '/':
        folder = folder.rstrip(folder[-1])
    return folder.split('/')[-1]

# main sync functions
def sync(folder,remote,banned_words,country_list,allow_translations,debug):
    """sync selected console roms to remote folder"""
    local_folder = os.path.abspath(folder)
    # list all roms in folder and remove some based on keywords
    romlist = purge(os.listdir(local_folder),banned_words,debug)
    # sort list
    romlist.sort()
    # create sets by game and select unique one
    romset = select_unique(create_sets(romlist,debug),country_list,allow_translations,debug)
    # push romsets once they have been curated
    remote_host.pushromset(
        romset,
        local_folder,
        remote['rom_path'] + '/' + trim_path(local_folder),
        remote,debug
    )
