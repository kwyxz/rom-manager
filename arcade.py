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

def find_by_machine(machine,root,rompath):
    games = []
    for game in root.findall(f".//*[@sourcefile='{machine}']"):
        try:
            if game.attrib['cloneof']:
                pass
        except KeyError:
            chd_folder = game.attrib['name']
            if os.path.exists(rompath + '/' + chd_folder):
                msg.info(f"CHD FOUND: {chd_folder}")
                chd_files = os.listdir(rompath + '/' + chd_folder)
                for chd_file in chd_files:
                    games.append(chd_folder + '/' + chd_file)
            games.append(game.attrib['name'] + '.zip')
    return games

def curate(gamelist,remote,mamerompath,mamexml,debug):
    """sync selected arcade roms to remote folder"""
    # open the XML file
    with open(mamexml) as xmlfile:
        xmlstring = xmlfile.read()
    root = ET.fromstring(xmlstring)
    romset = []
    for game in gamelist:
        machine = find_machine(game,root)
        machine_games = find_by_machine(machine,root,mamerompath)
        romset = romset + machine_games
    remote_host.pushromset(romset,mamerompath,remote['rom_path'] + '/' + 'arcade/',remote,debug)