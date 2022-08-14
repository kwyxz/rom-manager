#!/usr/bin/env python3

import os
import yaml

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
    print(settings)

if __name__ == "__main__":
    main()