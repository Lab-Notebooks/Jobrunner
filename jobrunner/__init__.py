"""Initialization method for PyJobrunner"""

from . import options

if options.INSTRUMENTS == 1:
    from . import instruments

from . import lib
from . import api
from . import cli
