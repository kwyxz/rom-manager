#!/usr/bin/env python3

import xml.etree.ElementTree as ET

MAMEXML='/usr/local/games/mame/mame.xml'
#MAMEXML='./shortmame.xml'

with open(MAMEXML) as xmlfile:
  xmlstring = xmlfile.read()

root = ET.fromstring(xmlstring)

#root.findall(".//*[@name='ffight'/")

print(root.findall(".//*[@name='ffight']")[0].attrib['sourcefile'])

for node in root.findall(".//*[@sourcefile='capcom/cps1.cpp']"):
  try:
    if node.attrib['cloneof']:
      print(f"CLONE: {node.attrib['name']}")
  except KeyError:
    print(f"NAME: {node.attrib['name']}")
