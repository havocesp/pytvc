# -*- coding: utf-8 -*-
"""
Core module.
"""
import inspect as insp
import json
import webbrowser
from pathlib import Path

import ccxt

_EX_SYMBOL_FMT = '{}:{}{}'


def checker(func):
    """

    :param function func:
    :return:
    """

    def wrapper(*args, **kwargs):
        args = list(args)
        kwargs = dict(kwargs)
        func_sign = insp.signature(func)
        params = func_sign.parameters
        params_list = list(params.keys())

        if len(args) and len(params_list):
            for pos, param in enumerate(params):
                if param in 'exchange':
                    if str(args[pos]).lower() in ccxt.exchanges:
                        args[pos] = str(args[pos]).upper()
                        params_list.remove('exchange')
                    else:
                        raise ValueError('Exchange {} is not supported'.format(str(args[pos].upper())))
                if param in 'currency' or param in 'symbol' and args[pos] is not None and isinstance(args[pos], str):
                    args[pos] = str(args[pos]).upper()
                if param in 'symbols' or param in 'currencies' and isinstance(args[pos], (set, list, tuple)):
                    args[pos] = list(map(str.upper, args[pos]))
        elif len(kwargs) and len(params_list):
            for p in list(params_list):
                if p in kwargs:
                    args.append(kwargs.get(p))
        return func(*args)

    return wrapper
    # return decorator


@checker
def watchlist_formatter(exchange, symbols):
    """
    Returns symbols formatted using tradingview specs.

    :param str exchange: exchange name used as prefix.
    :param list symbols: symbols str list.
    :return list: symbols list after formatting process.
    """
    exchange = str(exchange).upper()
    result = [_EX_SYMBOL_FMT.format(exchange, *s.split('/')) for s in symbols]
    return result


class TradingViewChart:
    """
    TradingView settings handler.
    """

    @checker
    def get_watchlist(self, exchange, market=None):
        """Returns a formatted symbols list belonging to "market" will be returned after apply a format process based
        on tradingview specs

        :param str exchange: a valid exchange name (example: BINANCE)
        :param str market: if set, only symbols on specific market will be return, this is, if market is set as USDT,
                           only symbols ending in USDT (like BTC/USDT) will be return.
        :return list: a formatted symbols list belonging to "market" will be returned after apply a format process based
                      on tradingview specs.
        """
        exchange = str(exchange).lower()

        for api_version in range(2, 5):
            api_version2check = '{}{:d}'.format(exchange, api_version)
            if api_version2check in ccxt.exchanges:
                exchange = api_version2check

            api = getattr(ccxt, exchange)({'timeout': 15000})  # type: ccxt.Exchange
            api.substituteCommonCurrencyCodes = False
            symbols = api.load_markets().keys()

            base_markets = {s.split('/')[1] for s in symbols}

            market = str(market).upper() if market and market in base_markets else 'BTC'
            ccc = api.common_currency_code
            filtered_symbols = ['{}/{}'.format(ccc(s.split('/')[0]), market) for s in symbols if
                                s.split('/')[1] in market]

            ticker = api.fetch_tickers(filtered_symbols)

            all_volumes = [v['quoteVolume'] for v in ticker.values()]
            volume_average = sum(all_volumes) / len(all_volumes)

            symbols_selection = {k: v for k, v in ticker.items() if v['quoteVolume'] > volume_average}
            sort_criteria = lambda k: symbols_selection[k]['quoteVolume']
            symbols_selection = sorted(symbols_selection, key=sort_criteria, reverse=True)

            return watchlist_formatter(exchange, symbols_selection)

    def launch(self, exchange, indicators=None, quote_currency=None, **options):
        """Launch an embedded "tradingview.com" widget in "app" mode (if available) with default web browser.

        :param str exchange: a valid exchange name (example: BINANCE)
        :param str quote_currency: a valid quote currency.
        :param indicators: list of indicators short names to show.
        :param options: [interval, theme, details, hotlist, calendar, news, hide_side_toolbar, locale, withdateranges]
        """
        quote_currency = quote_currency if quote_currency else 'BTC'

        json_dir = Path(__file__).parent.joinpath('json')  # type: Path
        html_dir = Path(__file__).parent.joinpath('html')  # type: Path

        params = json_dir.joinpath('params.json')
        params = json.loads(params.read_text())
        params.update(options)

        tv_indicators = json_dir.joinpath('tv_indicators.json')
        tv_indicators = json.loads(tv_indicators.read_text())

        if len(indicators or []):
            indicators = [ind.upper() for ind in indicators]
            indicators = [tv_indicators[i] for i in tv_indicators if i.upper() in indicators]
        else:
            indicators = [
                tv_indicators['ChaikinOscillator'],
                tv_indicators['ROC'],
                tv_indicators['WilliamR'],
                tv_indicators['MAExp'],
                tv_indicators['MAExp'],
                tv_indicators['LinearRegression']
            ]

        watchlist = self.get_watchlist(exchange, quote_currency)
        symbol = options.get('symbol') or 'BINANCE:BTCUSDT'

        params.update(symbol=symbol, watchlist=watchlist, studies=indicators)

        html_template_code = html_dir.joinpath('template.html').read_text()
        html_template_code = html_template_code.replace('@PARAMETERS', json.dumps(params, indent=2))

        html_generated_file = html_dir.joinpath('generated.html')
        html_generated_file.touch(exist_ok=True)
        html_generated_file.write_text(html_template_code)

        generated_file_url = 'file://{}'.format(html_generated_file)

        wb = webbrowser.get(using='chromium-browser --app="%s" --new-window')
        wb.open(generated_file_url, 1)
