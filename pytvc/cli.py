#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PyTVC

 - Author:      Daniel J. Umpierrez
 - Created:     04-11-2018
 - License:     UNLICENSE
"""
import argparse
import json
import sys
from pathlib import Path

from .core import TradingViewChart

_indicators = None


def load_indicators():
    """Load indicators from file.

    :return:
    """
    ti = dict()
    try:
        ti_file: Path = Path(__file__).with_name('json').joinpath('tv_indicators.json')
        if ti_file.exists() and ti_file.is_file():
            text = ti_file.read_text()
            ti = json.loads(text)
    except (TypeError, ValueError, IOError,) as err:
        print(str(err))
    return ti 


def list_indicators() -> int:
    """List all supported indicators.

    :return: 0 if all was fine.
    """
    ti = load_indicators()
    indicators = [f'- {v:<30}\n' for v in ti]
    indicators.sort()
    for i in indicators:
        print(i)
    return 0


def main(args):
    """TradingView Chart launcher."""
    tvc = TradingViewChart()
    tvc.launch(**vars(args))
    return 0


def run() -> int:
    """ As CLI starting point, this function dispatch argument parsing to be supplied to main function.

    :return: a 0 value for execution success or a non zero value containing the clue about where to find the error :-).
    :rtype: int
    """
    # system return code
    r_code = 0

    base_markets = ['BTC', 'TUSD', 'USDT', 'USD', 'EUR', 'PAX', 'USDS']
    exchanges = ['binance', 'cryptopia', 'hitbtc2', 'poloniex', 'kraken', 'coinbase', 'cexio']
    exchanges = {e: e.strip('_12345 ') for e in exchanges}

    load_indicators()

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(description='Commands')

    launch = subparsers.add_parser('launch', help='a help')

    launch.add_argument('-e, --exchange',
                        default='binance',
                        dest='exchange',
                        nargs='?',
                        choices=exchanges,
                        help='Exchange used for watch list symbols.')

    launch.add_argument('-q', '--quote-currency',
                        nargs='?',
                        default='BTC',
                        choices=base_markets,
                        help='Base market currency (default BTC)')

    launch.add_argument('-i', '--indicator',
                        metavar='TI',
                        nargs='*',
                        choices=list(_indicators.keys()),
                        help='Technical analysis indicators to be showed within chart.')

    launch.add_argument('-m', '--min-volume',
                        type=float,
                        nargs='?',
                        dest='min_volume',
                        default=0.0,
                        help='Min. 24h volume filter.')

    launch.set_defaults(func=main)

    indicators = subparsers.add_parser('list-indicators',
                                       help='List all supported technical indicators.')

    indicators.set_defaults(func=list_indicators)

    args = parser.parse_args()

    if hasattr(args, 'func'):
        r_code = args.func(args)
    else:
        parser.print_help()

    return r_code


if __name__ == '__main__':
    sys.exit(run())
