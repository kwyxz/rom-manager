#!/usr/bin/env python3

"""
manage roms on specific devices
"""

import settings
import cli_args
import msg
import arcade
import console

### main loop ###
def main(args,conf):
    """main function"""
    if args.verbose:
        DEBUG = True
    else:
        DEBUG = False
    # read the other arguments
    if args.listhw:
        msg.hw(conf)
    else:
        remote_hw = conf['remote_hw'][args.remote]
        try:
            if args.console:
                for local_folder in args.console[0]:
                    console.sync(local_folder,remote_hw,conf['banned_words'],conf['country_list'],DEBUG)
            elif args.arcade:
                    arcade.curate(args.arcade[0],remote_hw,conf['mame_rom_path'],conf['mame_data_file'],DEBUG)
            else:
                msg.die(f"argument error")
        except KeyError:
            msg.die(f"{args.remote} is not a valid remote identifier")

if __name__ == "__main__":
    ARGS = cli_args.parse()
    CONF = settings.load(ARGS.verbose)
    main(ARGS,CONF)
