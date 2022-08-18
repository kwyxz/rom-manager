#!/usr/bin/env python3

from lxml import etree

MAMEXML='/usr/local/games/mame/mame.xml'

# retrieve the metadata from the XML file
def game_meta(name,xmlroot,node,meta):
    """retrieve game metadata"""
    try:
        xpath = "./" + node + "[@name='" + name + "']/{}"
        return xmlroot.findall(xpath.format(meta))[0].text
    except IndexError:
        print("Either the game %s, its year or manufacturer, were not found in this database" % name)
        return None

def game_meta_misc(name,xmlroot,node,meta,tag):
    """retrieve misc game metadata"""
    try:
        xpath = "./" + node + "[@name='" + name + "']//" + meta
        value = xmlroot.findall(xpath)[0].attrib[tag]
        return value
    except (IndexError,KeyError):
        return ''

tree_mame = etree.parse(MAMEXML)
tree_root = tree_mame.getroot()

print(game_meta('ffight',tree_root,'machine','description'))
print(game_meta_misc('ffight',tree_root,'machine','input','players'))
