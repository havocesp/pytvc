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
from argparse import Namespace
from pathlib import Path

from .core import TradingViewChart


def load_indicators():
    """Load indicators from file.

    :return:
    """
    ti = list()
    try:
        ti_file: Path = Path(__file__).with_name('json').joinpath('tv_indicators.json')
        if ti_file.exists() and ti_file.is_file():
            text = ti_file.read_text()
            ti = json.loads(text)
    except (TypeError, ValueError, IOError,) as err:
        print(str(err))
        raise err
    return ti 


def list_indicators() -> int:
    """List all supported indicators.

    :return: 0 if all was fine.
    """
    ti = load_indicators()
    indicators = [f'- {v:<30}' for v in ti]
    indicators.sort()
    for i in indicators:
        print(i)
    return 0


def main(args) -> int:
    """TradingView Chart parserr.
    
    :param Namespace args:
    :return:
    """
    tvc = TradingViewChart()
    tvc.launch(**vars(args))
    return 0


def run():
    """As CLI starting point, this function dispatch argument parsing to be supplied to main function."""
    base_markets = ['BTC', 'TUSD', 'USDT', 'USD', 'EUR', 'PAX', 'USDS']
    exchanges = ['binance', 'hitbtc2', 'poloniex', 'kraken', 'coinbase', 'cexio']
    exchanges = {e: e.strip('_12345 ') for e in exchanges}

    parser = argparse.ArgumentParser()

    parser.add_argument('-l, --list-indicators',
                        action='store_true',
                        dest='list_indicators',
                        help='List all supported technical indicators')                                                                                                  
                                                                                                                                                                         
    parser.add_argument('-e, --exchange',                                                                                                                                
                        default='binance',                                                                                                                               
                        dest='exchange',                                                                                                                                 
                        nargs='?',                                                                                                                                       
                        choices=exchanges,                                                                                                                               
                        help='Exchange used for watch list symbols.')                                                                                                    
                                                                                                                                                                         
    parser.add_argument('-q', '--quote-currency',                                                                                                                        
                        nargs='?',                                                                                                                                       
                        default='BTC',                                                                                                                                   
                        choices=base_markets,                                                                                                                            
                        help='Base market currency (default BTC)')                                                                                                       
                                                                                                                                                                         
    parser.add_argument('-i', '--indicator',                                                                                                                             
                        metavar='TI',                                                                                                                                    
                        nargs='*',                                                                                                                                       
                        choices=list(load_indicators().keys()),                                                                                                          
                        help='Technical analysis indicators to be showed within chart.')                                                                                 
                                                                                                                                                                         
    parser.add_argument('-m', '--min-volume',                                                                                                                            
                        type=float,                                                                                                                                      
                        nargs='?',                                                                                                                                       
                        dest='min_volume',                                                                                                                               
                        default=0.0,                                                                                                                                     
                        help='Min. 24h volume filter.')                                                                                                                  

    args = parser.parse_args()                                                        
    
    if args.list_indicators is True:
        r_code = list_indicators()
    else:
        r_code =  main(args)

    sys.exit(r_code)

if __name__ == '__main__': 
    run()
