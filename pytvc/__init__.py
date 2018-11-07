# -*- coding: utf-8 -*-
"""
 PyTVC

 Python TradingView Chart

 - Author:      Daniel J. Umpierrez
 - Created:     03-11-2018
 - License:     UNLICENSE
"""
import os
import sys

sys.path.append(os.path.dirname(os.path.basename(__file__)))
sys.path.append(os.path.dirname(__file__))


from pytvc.core import TradingViewChart

__project__ = 'PyTVC'
__package__ = 'pytvc'
__author__ = 'Daniel J. Umpierrez'
__license__ = 'UNLICENSE'
__version__ = '0.1.0'
__description__ = __doc__
__site__ = 'https://github.com/havocesp/{}'.format(__package__)
__email__ = 'umpierrez@pm.me'
__long_description__ = open('../README.me').read()
__keywords__ = ['altcoins', 'altcoin', 'exchange', 'pandas', 'bitcoin', 'trading', 'tradingview', 'chart', 'finance']
__dependencies__ = ['ccxt', 'begins']
__all__ = ['__description__', '__author__', '__license__', '__version__', '__project__', '__site__',
           '__email__', '__keywords__', 'TradingViewChart']
