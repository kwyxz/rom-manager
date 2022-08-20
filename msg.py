# output

"""
display messages to user in CLI mode
"""

import sys

# error messages
def error(text):
    """print an error message"""
    print(f"\033[31mERROR\033[m: {text}")
    return False

# info messages
def info(text):
    """print an info message"""
    print(f"\033[33mINFO\033[m: {text}")
    return True

# debug messages
def debug(text,debug):
    """print only in verbose mode"""
    if debug:
        print(f"\033[33mDEBUG\033[m: {text}")
        return True
    else:
        return False

# OK messages
def ok(text):
    """print an OK message"""
    print(f"\033[32mOK\033[m: {text}")
    return True

# die messages
def die(text):
    """print an error message then die"""
    error(text)
    sys.exit(1)

# hardware output
def hw(settings):
    """display the list of remote destinations configured in settings"""
    for key,value in enumerate(settings['remote_hw']):
        print(f"\n\033[1mremote\033[m: {value}")
        # remote hardware will always be useful
        x = settings['remote_hw'][value]
        print(f"\t({x['name']})")
        print(f"\t{x['protocol']}@{x['ip_addr']}:{x['port']}")
        print(f"\t{x['rom_path']}")
    sys.exit(0)