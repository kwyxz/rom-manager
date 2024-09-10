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
def debug(text,flag):
    """print only in verbose mode"""
    if flag:
        try:
            print(f"\033[33mDEBUG\033[m: {text}")
        except UnicodeEncodeError:
            print(f"\033[31mERROR\033[m: encoding error with file name (skipping debug)")
        return True
    return False

# OK messages
def ok(text): # pylint: disable=invalid-name
    """print an OK message"""
    print(f"\033[32mOK\033[m: {text}")
    return True

# die messages
def die(text):
    """print an error message then die"""
    error(text)
    sys.exit(1)

# hardware output
def hw(settings): # pylint: disable=invalid-name
    """display the list of remote destinations configured in settings"""
    for _,value in enumerate(settings['remote_hw']):
        # remote hardware will always be useful
        remote = settings['remote_hw'][value]
        print(f"\n\033[1mremote\033[m: {value} ({remote['name']})")
        print(f"\t{remote['protocol']}@{remote['ip_addr']}:{remote['port']}")
        print(f"\t{remote['rom_path']}")
    sys.exit(0)
