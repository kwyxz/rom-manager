# curate arcade roms

"""
curate arcade roms by machine
"""

import os
import msg
import remote_host
import xml.etree.ElementTree as ET

def find_machine(game,root):
    return root.findall(f".//*[@name='{game}']")[0].attrib['sourcefile']

def find_by_machine(machine,root,rompath,debug):
    games = []
    for game in root.findall(f".//*[@sourcefile='{machine}']"):
        try:
            if game.attrib['cloneof']:
                msg.debug(f"{game.attrib['name']} is a clone, skipping",debug)
                pass
        except KeyError:
            msg.debug(f"found game: {game.attrib['name']}",debug)
            chd_folder = game.attrib['name']
            if os.path.exists(rompath + '/' + chd_folder):
                msg.info(f"found CHD folder: {chd_folder}")
                chd_files = os.listdir(rompath + '/' + chd_folder)
                for chd_file in chd_files:
                    games.append(chd_folder + '/' + chd_file)
            games.append(game.attrib['name'] + '.zip')
    return games

def curate(gamelist,remote,mamerompath,mamexml,debug):
    """sync selected arcade roms to remote folder"""
    # open the XML file
    msg.debug(f"using {mamexml} as MAME data source",debug)
    with open(mamexml) as xmlfile:
        xmlstring = xmlfile.read()
    root = ET.fromstring(xmlstring)
    romset = []
    for game in gamelist:
        msg.debug(f"looking for game {game}",debug)
        machine = find_machine(game,root)
        machine_games = find_by_machine(machine,root,mamerompath,debug)
        romset = romset + machine_games
    sorted_set = sorted(set(romset))
    remote_host.pushromset(sorted_set,mamerompath,remote['rom_path'] + '/' + 'arcade/',remote,debug)
