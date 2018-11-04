# -*- coding: utf-8 -*-
"""
 PyTVC
 - Author:      Daniel J. Umpierrez
 - Created:     04-11-2018
 - License:     UNLICENSE
"""
import begin

from pytvc import TradingViewChart


@begin.start
def main(exchange, quote_currency=None):
    """TradingView Chart launcher."""
    TradingViewChart().launch(exchange, quote_currency)
