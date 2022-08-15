#!/usr/bin/env python3

"""
manage roms on specific devices
"""

import os
import yaml
import cli_arguments

def check_folder(folder):
    if os.path.exists(folder):
        extract_romname(folder)
    else:
        die("Error: folder {} does not exist, skipping".format(folder))

def load_settings():
    user_settings = "$HOME/.config/rom-manager/settings.yaml"
    if os.path.exists(user_settings):
        settings_file = user_settings
    else:
        settings_file = 'settings.yaml'
    with open(settings_file) as file:
        return yaml.safe_load(file)

def main():
    settings = load_settings()
    args = cli_arguments.parse()
    print(args)

if __name__ == "__main__":
    main()