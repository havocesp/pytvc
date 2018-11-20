# -*- coding: utf-8 -*-
"""
 PyTVC
 - Author:      Daniel J. Umpierrez
 - Created:     04-11-2018
 - License:     UNLICENSE
"""
import argparse
import json
import pathlib
import sys
from argparse import Namespace

from pytvc import TradingViewChart


def main(exchange, indicators, quote_currency=None):
    """TradingView Chart launcher."""
    TradingViewChart().launch(exchange, indicators, quote_currency or 'BTC')


def run():
    base_markets = ['BTC', 'USDT', 'USD', 'EUR']
    exchanges = ['binance', 'cryptopia', 'hitbtc', 'poloniex', 'kraken', 'coinbase', 'cexio']

    ti_file = pathlib.Path(__file__).parent.joinpath('json', 'tv_indicators.json')
    indicators = list()
    if ti_file.is_file():
        indicators = json.loads(ti_file.read_text())

    args = argparse.ArgumentParser()
    args.add_argument('exchange',
                      choices=exchanges,
                      default='binance', nargs='?',
                      help='Exchange for smart watch list symbols loading.')

    args.add_argument('-q', '--quote-currency',
                      default='BTC',
                      choices=base_markets,
                      help='Base market currency (default BTC)')

    args.add_argument('-i', '--indicator',
                      metavar='TI',
                      nargs='*',
                      choices=list(indicators.keys()),
                      help='Technical analysis indicators to be showed within chart.')

    args.add_argument('-t', '--ti-list',
                      action="store_true",
                      help='List all supported technical indicators.')
    args = args.parse_args()  # type: Namespace

    if args.ti_list:
        for v in indicators:
            print('- {:<30}'.format(v))
    else:
        main(args.exchange.upper(), args.indicator, args.quote_currency)


if __name__ == '__main__':
    run()

    generated_html = pathlib.Path(__file__).parent / 'html' / 'generated.html'  # type: pathlib.Path
    if generated_html.exists():
        generated_html.unlink()
