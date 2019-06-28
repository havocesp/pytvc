# -*- coding: utf-8 -*-
"""Core module."""
import json
import shutil
import subprocess
from pathlib import Path

import ccxt

_CHROME_LIKE_BROWSERS = ['brave-browser', 'chromium', 'chromium-browser', 'google-chrome', 'chrome']
_BROWSERS = _CHROME_LIKE_BROWSERS + ['firefox', 'mozilla', 'epiphany', 'konqueror', 'safari', 'opera', 'edge']


class Symbol:
    """Symbol class."""

    def __init__(self, ref):
        if '/' in str(ref):
            self.base, self.quote = ref.split('/')
        else:
            self.base = None
            self.quote = None

    def __str__(self):
        return f'{self.base or ""}/{self.quote or ""}'

    def __repr__(self):
        return f'{self.base or ""}/{self.quote or ""}'


def watchlist_formatter(exchange, symbols):
    """Returns symbols formatted using TradingView specs.

    :param str exchange: exchange name used as prefix.
    :param list symbols: symbols str list.
    :return list: symbols list after formatting process.
    """
    exchange = str(exchange).upper()
    result = [f'{exchange}:{s.base}{s.quote}'
              for s in map(Symbol, symbols)
              if s.base not in ['PAX']]
    return result


def open_browser(url):
    """Open url using a "chrome like" found (or any when chrome like not found)"""
    global _BROWSERS, _CHROME_LIKE_BROWSERS
    for browser in _BROWSERS:
        if shutil.which(browser):
            if browser in _CHROME_LIKE_BROWSERS:
                return subprocess.call([browser, f'--app={url}', '--new-window'])
            else:
                return subprocess.call([browser, f'{url}'])
    return 1


def get_volume_average(tickers) -> float:
    """Get volume average from tickers data.

    :param dict tickers:
    :return: calculated volume average from tickers data.
    """
    all_volumes = [v['quoteVolume'] for v in tickers.values()]
    avg = sum(all_volumes) / len(all_volumes)
    return avg


class TradingViewChart:
    """TradingView settings handler."""

    def get_watchlist(self, exchange, market=None, min_volume=None):
        """Returns a formatted symbols list belonging to "market" will be returned after apply a format process based
        on TradingView specs

        :param str exchange: a valid exchange name (example: BINANCE)
        :param str market: if set, only symbols on specific market will be return, this is, if market is set as USDT,
                           only symbols ending in USDT (like BTC/USDT) will be return.
        :param float min_volume: min volume filter (default 0.0)
        :return list: a formatted symbols list belonging to "market" will be returned after apply a format process based
                      on tradingview specs.
        """
        exchange = str(exchange).lower()

        for api_version in range(2, 5):
            api_version2check = f'{exchange}{api_version:d}'

            if api_version2check in ccxt.exchanges:
                exchange = api_version2check

            api = getattr(ccxt, exchange)({
                'timeout':                       15000,
                'substituteCommonCurrencyCodes': True
            })

            api.load_markets()

            base_markets = {Symbol(s).quote for s in api.symbols}
            market = str(market or '').upper()
            market = market if market in base_markets else 'BTC'

            filtered_symbols = [f'{api.common_currency_code(s.base)}/{market}'
                                for s in map(Symbol, api.symbols)
                                if s.quote in market and s.base != s.quote]

            tickers = api.fetch_tickers(filtered_symbols)

            if min_volume is None:
                min_volume = get_volume_average(tickers)
            elif isinstance(min_volume or 0, str):
                try:
                    min_volume = float(min_volume)
                except ValueError:
                    pass
            elif isinstance(min_volume, (float, int)):
                min_volume = get_volume_average(tickers)
            else:
                raise ValueError(f'{min_volume} invalid min. volume value.')

            symbols_selection = {k: v for k, v in tickers.items() if v['quoteVolume'] > min_volume}
            sort_criteria = lambda k: symbols_selection[k]['quoteVolume']
            symbols_selection = sorted(symbols_selection, key=sort_criteria, reverse=True)

            return watchlist_formatter(exchange, symbols_selection)

    def launch(self, exchange, indicators=None, quote_currency=None, min_volume=0.0, **options):
        """Launch an embedded "tradingview.com" widget in "app" mode (if available) with default web browser.

        :param str exchange: a valid exchange name (example: BINANCE)
        :param indicators: list of indicators short names to show.
        :param str quote_currency: a valid quote currency.
        :param float min_volume: min volume filter (default 0.0)
        :param options: [interval, theme, details, hotlist, calendar, news, hide_side_toolbar, locale, withdateranges]
        """
        quote_currency = quote_currency if quote_currency else 'BTC'

        json_dir = Path(__file__).with_name('json')  # type: Path
        html_dir = Path(__file__).with_name('html')  # type: Path

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
                tv_indicators['MAExp'],
                tv_indicators['MAExp'],
                tv_indicators['MASimple'],
                tv_indicators['StochasticRSI'],
                tv_indicators['LinearRegression']
            ]

        watchlist = self.get_watchlist(exchange, quote_currency, min_volume=min_volume)
        symbol = options.get('symbol') or 'BINANCE:BTCUSDT'

        params.update(symbol=symbol, watchlist=watchlist, studies=indicators)

        html_template_code = html_dir.joinpath('template.html').read_text()

        params_json = json.dumps(params)
        html_template_code = html_template_code.replace('@PARAMETERS', params_json)

        html_generated_file = html_dir.joinpath('generated.html')
        html_generated_file.touch(exist_ok=True)
        html_generated_file.write_text(html_template_code)

        generated_file_url = f'file://{html_generated_file}'

        open_browser(generated_file_url)
