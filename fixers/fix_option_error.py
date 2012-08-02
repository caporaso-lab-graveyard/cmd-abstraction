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

class FixOptionError(BaseFix):
    
    #_accept_type = token.TRAILER
    PATTERN = """
    power< 'option_parser' trailer< '.' 'error' > trailer< '(' term< '"Can\'t open parameters file (%s). Does it exist? Do you have read access?"' '%' power< 'opts' trailer< '.' 'parameter_fp' > > > ')' > >
    """

    def match(self, node):
        print node
        # if node.value == '.error':
        #         return True
        #     return False
        # 
    def transform(self, node, results):
        print node
        node.value = 'QiimeCommandError'
        node.changed()
