# curate arcade roms

"""
curate arcade roms by machine
"""

import os
import xml.etree.ElementTree as ET
import msg
import remote_host

def find_machine(game,root,debug):
    """looking for hardware a game runs on"""
    msg.debug(f"CHECK:\thardware for {game}",debug)
    try:
        return root.findall(f".//machine[@name='{game}']")[0].attrib['sourcefile']
    except IndexError:
        msg.die(f"game {game} not found in MAME database")

def replace_game(game,replist,debug):
    try:
        if replist[game]:
            msg.debug(f"REPLACED:\tgame {game} => {replist[game]}",debug)
            return replist[game]
    except KeyError:
        return game

def find_by_machine(machine,root,banned,rompath,merged,replace,debug):
    """list all games running on a hardware"""
    games = []
    for game in root.findall(f".//*[@sourcefile='{machine}']"):
        msg.debug(f"TESTING:\tgame {game.attrib['name']}",debug)
        try:
            if game.attrib['cloneof']:
                msg.debug(f"SKIPPED:\tclone {game.attrib['name']}",debug)
        except KeyError:
            gamename = game.attrib['name']
            if gamename in banned:
                msg.debug(f"SKIPPED:\tbanned {gamename}",debug)
            else:
                msg.debug(f"FOUND:\tgame {game.attrib['name']}",debug)
                if not merged:
                    # look if a replacement exists for 4-player games
                    gamename = replace_game(gamename,replace,debug)
                if os.path.exists(rompath + '/' + gamename):
                    msg.info(f"FOUND:\tCHD for {gamename}")
                    chd_files = os.listdir(rompath + '/' + gamename)
                    for chd_file in chd_files:
                        games.append(gamename + '/' + chd_file)
                games.append(gamename + '.zip')
    return games

def curate(gamelist,remote,banned,mamerompath,mamexml,merged,replace,debug): # pylint: disable=too-many-arguments
    """sync selected arcade roms to remote folder"""
    # open the XML file
    msg.debug(f"CHECK:\tMAME data source {mamexml}",debug)
    with open(mamexml, encoding="utf-8") as xmlfile:
        xmlstring = xmlfile.read()
    root = ET.fromstring(xmlstring)
    machines = []
    romset = []
    # parse through the list of games and find the hardwares that will be pushed
    for game in gamelist:
        msg.debug(f"CHECK:\tgame {game}",debug)
        machine = find_machine(game,root,debug)
        msg.debug(f"FOUND:\thardware {machine}",debug)
        machines.append(machine)
    # get rid of duplicates
    sorted_set = sorted(set(machines))
    # create a new loop over all the hardwares to optimize search
    for machine in sorted_set:
        msg.debug(f"CHECK:\tgames by hardware {machine}",debug)
        machine_games = find_by_machine(machine,root,banned,mamerompath,merged,replace,debug)
        romset = romset + machine_games
    # there should not be any duplicates yet but just to play it safe
    sorted_set = sorted(set(romset))
    print(sorted_set)
    remote_host.pushromset(sorted_set,mamerompath,remote['rom_path'] + '/' + 'arcade/',remote,debug)
