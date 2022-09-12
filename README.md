# rom-manager
If you have ever spent hours just scrolling down a list of MAME games desperately looking for the one you wanted to play, then this tool is for you.
It's a fact : nobody needs 15000 roms. Especially when 90% of these are either regional variants, bootlegs, clones, or just crap that should never have been released in the first place.
This is especially true on handhelds (GCW Zero, JXD, Vita, Switch, Steamdeck) where storage space is limited but also true on Raspberry Pi devices for example.
This tool is an attempt to curate games in order to only keep the ones that really matter.
It takes two different approaches depending on whether we are dealing with console games or arcade games.

With console games, it will:
 - browse a folder full of games
 - look for a unique name amongst various regional variants
 - trim out versions based off a configurable banned keyword list (like Demo, Beta, etc)
 - pick up the most interesting region following a configurable order
 - in my case, this means first USA (60Hz and english language) > France (I am french) > Europe > World > Japan (last resort when no other exist) ; again this is of course configurable
 - it will then attempt to get the latest revision (bugfixes baby)
 - push the winner to the remote device

With arcade games, it will:
 - look for the hardware a given game is running on
 - select all games running on the same hardware ; the rationale is if I enjoyed a game by developer X on hardware Y, there is a chance I might enjoy another game (often by the same developer) on hardware Y
 - trim out clones / bootlegs that nobody needs
 - trim out games from a banned list (configurable)
 - push the resulting list of games the remote device

# requirements
- python3
- paramiko module
- yaml module

# data file
A MAME xml file is necessary. Either download one, or create it using the MAME binary with option `-listxml` copied into a file. Then set the path to it in the settings file.

# configuration
Some default settings are set in settings.yaml. To customize them, copy the file to your $HOME/.config/ and update it.

# usage
Run `rom_manager.py -h` for a list of options.

# examples
Send all SNES roms from a folder to a Steamdeck:
```
$ rom_manager.py -r deck -c ~/Games/snes
```
Find all arcade games running on the same hardware as Final Fight and send them to a Raspberry Pi:
```
$ rom_manager.py -r pi -a ffight
```

# todo
Implement FTP push (for Vita and other devices that do not run SSH)
