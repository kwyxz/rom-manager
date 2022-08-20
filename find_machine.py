#!/usr/bin/env python3

import xml.dom.minidom

MAMEXML='./shortmame.xml'

class MachineParse(object):

  def __init__(self,is_clone,source):
    self.name = name
    self.description = description
    self.is_clone = is_clone
    self.source = source
