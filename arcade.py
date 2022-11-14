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

def find_by_machine(machine,root,banned,rompath,debug):
    """list all games running on a hardware"""
    games = []
    for game in root.findall(f".//*[@sourcefile='{machine}']"):
        try:
            if game.attrib['cloneof']:
                msg.debug(f"SKIPPED:\tclone {game.attrib['name']}",debug)
        except KeyError:
            msg.debug(f"FOUND:\tgame {game.attrib['name']}",debug)
            gamename = game.attrib['name']
            if gamename in banned:
                msg.debug(f"SKIPPED:\tbanned {gamename}",debug)
            else:
                if os.path.exists(rompath + '/' + gamename):
                    msg.info(f"FOUND:\tCHD for {gamename}")
                    chd_files = os.listdir(rompath + '/' + gamename)
                    for chd_file in chd_files:
                        games.append(gamename + '/' + chd_file)
                games.append(game.attrib['name'] + '.zip')
    return games

def curate(gamelist,remote,banned,mamerompath,mamexml,debug): # pylint: disable=too-many-arguments
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
        machine_games = find_by_machine(machine,root,banned,mamerompath,debug)
        romset = romset + machine_games
    # there should not be any duplicates yet but just to play it safe
    sorted_set = sorted(set(romset))
    remote_host.pushromset(sorted_set,mamerompath,remote['rom_path'] + '/' + 'arcade/',remote,debug)
