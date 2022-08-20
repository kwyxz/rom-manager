# curate arcade roms

"""
curate arcade roms by machine
"""

def find_machine(game):
    return True

def curate_arcaderoms(gamelist):
    """sync selected arcade roms to remote folder"""
    for game in gamelist:
        machine = find_machine(game)