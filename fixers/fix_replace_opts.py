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

class FixReplaceOpts(BaseFix):
    
    _accept_type = token.NAME

    def match(self, node):
        if node.value == 'opts':
            return True
        return False
    
    def transform(self, node, results):
        node.value = 'options'
        node.changed()

