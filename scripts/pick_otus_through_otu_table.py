#!/usr/bin/env python
# File created on 30 Jul 2012
from __future__ import division

__author__ = "Greg Caporaso"
__copyright__ = "Copyright 2011, The QIIME project"
__credits__ = ["Greg Caporaso"]
__license__ = "GPL"
__version__ = "1.5.0-dev"
__maintainer__ = "Greg Caporaso"
__email__ = "gregcaporaso@gmail.com"
__status__ = "Development"

from cmd_abstraction.util import cmd_main
from cmd_abstraction.interfaces import PickOtusThroughOtuTable
from sys import argv

if __name__ == "__main__":
    cmd_main(PickOtusThroughOtuTable,argv)