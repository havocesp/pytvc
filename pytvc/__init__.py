# -*- coding: utf-8 -*-
"""
 PyTVC

 Python TradingView Chart

 - Author:      Daniel J. Umpierrez
 - Created:     03-11-2018
 - License:     UNLICENSE
"""
import pathlib

from pytvc.core import TradingViewChart

_ROOT = pathlib.Path(__file__).parent.parent  # type: pathlib.Path

__project__ = 'PyTVC'
__package__ = 'pytvc'
__author__ = 'Daniel J. Umpierrez'
__license__ = 'UNLICENSE'
__version__ = '0.1.1'
__description__ = __doc__
__site__ = 'https://github.com/havocesp/{}'.format(__package__)
__email__ = 'umpierrez@pm.me'
__long_description__ = _ROOT.joinpath('README.md').read_text()
__keywords__ = ['altcoins', 'altcoin', 'exchange', 'pandas', 'bitcoin', 'trading', 'tradingview', 'chart', 'finance']
__dependencies__ = ['ccxt', 'begins']

__all__ = ['__description__', '__author__', '__license__', '__version__', '__project__', '__site__', '__email__',
           '__keywords__', 'TradingViewChart']
