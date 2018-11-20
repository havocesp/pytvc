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

from pytvc import TradingViewChart


def main(exchange, indicators, quote_currency=None):
    """TradingView Chart launcher."""
    TradingViewChart().launch(exchange, indicators, quote_currency or 'BTC')
    return 0


def run():
    base_markets = ['BTC', 'USDT', 'USD', 'EUR']
    exchanges = ['binance', 'cryptopia', 'hitbtc', 'poloniex', 'kraken', 'coinbase', 'cexio']

    ti_file = pathlib.Path(__file__).parent.joinpath('json', 'tv_indicators.json')
    indicators = list()

    if ti_file.exists() and ti_file.is_file():
        indicators = json.loads(ti_file.read_text())

    parser = argparse.ArgumentParser()

    parser.add_argument('exchange',
                      choices=exchanges,
                      default='binance', nargs='?',
                      help='Exchange for smart watch list symbols loading.')

    parser.add_argument('-q', '--quote-currency',
                        default='BTC',
                        choices=base_markets,
                        help='Base market currency (default BTC)')

    parser.add_argument('-i', '--indicator',
                        metavar='TI',
                        nargs='*',
                        choices=list(indicators.keys()),
                        help='Technical analysis indicators to be showed within chart.')

    parser.add_argument('-t', '--ti-list',
                        action="store_true",
                        help='List all supported technical indicators.')
    args = parser.parse_args()  # type: argparse.Namespace

    if args.ti_list:
        for v in indicators:
            print('- {:<30}'.format(v))
            return 0
    else:
        return (main(args.exchange.upper(), args.indicator, args.quote_currency))


if __name__ == '__main__':
    sys.exit(run())
