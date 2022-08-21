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
                for local_folder in args.console:
                    console.sync(local_folder,remote_hw,conf['banned_words'],conf['country_list'],DEBUG)
            elif args.arcade:
                for gamelist in args.arcade:
                    curate_arcaderoms(gamelist)
            else:
                msg.die(f"argument error")
        except KeyError:
            msg.die(f"{args.remote} is not a valid remote identifier")

if __name__ == "__main__":
    ARGS = cli_args.parse()
    CONF = settings.load(ARGS.verbose)
    main(ARGS,CONF)
