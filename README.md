# rom-manager
A unified tool to manage roms on all my devices

# requirements
- python3
- paramiko module
- yaml module

# data file
A MAME xml file is necessary. Either download one, or create it using the MAME binary with option `-listxml` copied into a file.

# configuration
Some default settings are set in settings.yaml. To customize them, copy the file to your $HOME/.config/ and update it.

# usage
Run `rom_manager.py -h` for a list of options
