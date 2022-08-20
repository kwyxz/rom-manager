# settings management

"""
manage settings, load and maybe in the future save
"""

import os
import msg
import yaml
from pathlib import Path

def load(debug):
    """load settings from global conf file or local conf file"""
    user_conf = str(Path.home()) + "/.config/rom-manager/settings.yaml"
    if os.path.exists(user_conf):
        conf_file = user_conf
    else:
        conf_file = os.path.abspath(os.path.dirname(__file__)) + '/settings.yaml'
    with open(conf_file) as file:
        msg.debug(f"loading settings file {conf_file}",debug)
        return yaml.safe_load(file)