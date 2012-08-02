#!/usr/bin/env python
# File created on 01 Aug 2012
from __future__ import division

__author__ = "Greg Caporaso"
__copyright__ = "Copyright 2011, The QIIME project"
__credits__ = ["Greg Caporaso"]
__license__ = "GPL"
__version__ = "1.5.0-dev"
__maintainer__ = "Greg Caporaso"
__email__ = "gregcaporaso@gmail.com"
__status__ = "Development"

from lib2to3.fixer_base import BaseFix
from lib2to3.pgen2 import token
from lib2to3.fixer_util import Leaf, Node, Subscript, syms, String

class FixOptionsObject(BaseFix):
    
    PATTERN = """
    power< head='opts' trailer< '.' optionname=any > >
    |
    power< head='options' trailer< '.' optionname=any > >
    """
    
    def transform(self, node, results):
        head = results['head']
        optionname = "'" + results['optionname'].value + "'"
        args = [head, Subscript(String(optionname))]
        node.replace(args)
        node.changed()

