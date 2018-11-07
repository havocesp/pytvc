# -*- coding: utf-8 -*-
"""
Core module.
"""
import json
import webbrowser
from pathlib import Path

import begin
import ccxt


def watchlist_formatter(exchange, symbols):
    """
    Returns symbols formatted using tradingview specs.

    :param str exchange: exchange name used as prefix.
    :param list symbols: symbols str list.
    :return list: symbols list after formatting process.
    """
    exchange = exchange.upper()
    template = '{}:{}{}'
    result = [template.format(exchange, *s.split('/')) for s in symbols]
    return result


class TradingViewChart:
    """
    TradingView settings handler.
    """

    class Indicators:
        """
        Supported indicators references.
        """
        ACCD = "ACCD@tv-basicstudies"
        studyADR = "studyADR@tv-basicstudies"
        AROON = "AROON@tv-basicstudies"
        ATR = "ATR@tv-basicstudies"
        AwesomeOscillator = "AwesomeOscillator@tv-basicstudies"
        BB = "BB@tv-basicstudies"
        BollingerBandsR = "BollingerBandsR@tv-basicstudies"
        BollingerBandsWidth = "BollingerBandsWidth@tv-basicstudies"
        CMF = "CMF@tv-basicstudies"
        ChaikinOscillator = "ChaikinOscillator@tv-basicstudies"
        chandeMO = "chandeMO@tv-basicstudies"
        ChoppinessIndex = "ChoppinessIndex@tv-basicstudies"
        CCI = "CCI@tv-basicstudies"
        CRSI = "CRSI@tv-basicstudies"
        CorrelationCoefficient = "CorrelationCoefficient@tv-basicstudies"
        DetrendedPriceOscillator = "DetrendedPriceOscillator@tv-basicstudies"
        DM = "DM@tv-basicstudies"
        DONCH = "DONCH@tv-basicstudies"
        DoubleEMA = "DoubleEMA@tv-basicstudies"
        EaseOfMovement = "EaseOfMovement@tv-basicstudies"
        EFI = "EFI@tv-basicstudies"
        ENV = "ENV@tv-basicstudies"
        FisherTransform = "FisherTransform@tv-basicstudies"
        HV = "HV@tv-basicstudies"
        hullMA = "hullMA@tv-basicstudies"
        IchimokuCloud = "IchimokuCloud@tv-basicstudies"
        KLTNR = "KLTNR@tv-basicstudies"
        KST = "KST@tv-basicstudies"
        LinearRegression = "LinearRegression@tv-basicstudies"
        MACD = "MACD@tv-basicstudies"
        MOM = "MOM@tv-basicstudies"
        MF = "MF@tv-basicstudies"
        MoonPhases = "MoonPhases@tv-basicstudies"
        MASimple = "MASimple@tv-basicstudies"
        MAExp = "MAExp@tv-basicstudies"
        MAWeighted = "MAWeighted@tv-basicstudies"
        OBV = "OBV@tv-basicstudies"
        PSAR = "PSAR@tv-basicstudies"
        PivotPointsHighLow = "PivotPointsHighLow@tv-basicstudies"
        PivotPointsStandard = "PivotPointsStandard@tv-basicstudies"
        PriceOsc = "PriceOsc@tv-basicstudies"
        PriceVolumeTrend = "PriceVolumeTrend@tv-basicstudies"
        ROC = "ROC@tv-basicstudies"
        RSI = "RSI@tv-basicstudies"
        VigorIndex = "VigorIndex@tv-basicstudies"
        VolatilityIndex = "VolatilityIndex@tv-basicstudies"
        SMIErgodicIndicator = "SMIErgodicIndicator@tv-basicstudies"
        SMIErgodicOscillator = "SMIErgodicOscillator@tv-basicstudies"
        Stochastic = "Stochastic@tv-basicstudies"
        StochasticRSI = "StochasticRSI@tv-basicstudies"
        TripleEMA = "TripleEMA@tv-basicstudies"
        Trix = "Trix@tv-basicstudies"
        UltimateOsc = "UltimateOsc@tv-basicstudies"
        VSTOP = "VSTOP@tv-basicstudies"
        Volume = "Volume@tv-basicstudies"
        VWAP = "VWAP@tv-basicstudies"
        MAVolumeWeighted = "MAVolumeWeighted@tv-basicstudies"
        WilliamR = "WilliamR@tv-basicstudies"
        WilliamsAlligator = "WilliamsAlligator@tv-basicstudies"
        WilliamsFractal = "WilliamsFractal@tv-basicstudies"
        ZigZag = "ZigZag@tv-basicstudies"

        @classmethod
        def as_dict(cls):
            """
            Returns a dict with indicator data.
            :return dict: generate dict generated from indicators short names as keys and long names as values.
            """
            return dict(cls.__dict__['__annotations__'])

        @classmethod
        def keys(cls):
            """
            Returns indicators short names as list .

            :return list: dict with indicator data.
            """
            return list(sorted(cls.as_dict().keys()))

        @classmethod
        def values(cls):
            """
            Returns indicators long names as list.

            :return list:
            """
            return list(sorted(cls.as_dict().values()))

        @classmethod
        def to_json(cls):
            """
            Returns a JSON indicators serialized with short names as keys and long names values.

            :return str: a JSON indicators serialized with short names as keys and long names values.
            """
            return json.dumps(cls.as_dict(), indent=2)

    def get_watchlist(self, exchange, market=None):
        """
        Returns a formatted symbols list belonging to "market" will be returned after apply a format process based
        on tradingview specs

        :param str exchange: a valid exchange name (example: BINANCE)
        :param str market: if set, only symbols on specific market will be return, this is, if market is set as USDT,
                           only symbols ending in USDT (like BTC/USDT) will be return.
        :return list: a formatted symbols list belonging to "market" will be returned after apply a format process based
                      on tradingview specs.
        """
        exchange = str(exchange).lower()

        if exchange in ccxt.exchanges:
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

    def launch(self, exchange, quote_currency=None, *indicators, **options):
        """
        Launch an embedded "tradingview.com" widget in "app" mode (if available) with default web browser.

        :param str exchange: a valid exchange name (example: BINANCE)
        :param indicators: list of indicators short names to show.
        :param options: [interval, theme, details, hotlist, calendar, news, hide_side_toolbar, locale, withdateranges]
        """
        html_dir = Path(__file__).parent.joinpath('html')  # type: Path

        params_file = str(html_dir.joinpath('params.json'))

        default_params = json.load(params_file)
        default_params.update(options)

        quote_currency = quote_currency if quote_currency else 'BTC'

        if len(indicators):
            indicators = [i for i in self.Indicators.keys() if i.upper() in map(str.upper, indicators)]
        else:
            indicators = [self.Indicators.ChaikinOscillator, self.Indicators.ROC, self.Indicators.WilliamR,
                          self.Indicators.MAExp, self.Indicators.MAExp, self.Indicators.LinearRegression]

        watchlist = self.get_watchlist(exchange, quote_currency)
        symbol = options.get('symbol') or 'BINANCE:BTCUSDT'

        default_params.update(symbol=symbol, watchlist=watchlist, studies=indicators)

        html_template_code = html_dir.joinpath('template.html').read_text()
        html_template_code = html_template_code.replace('@PARAMETERS', json.dumps(default_params, indent=2))

        html_generated_file = html_dir.joinpath('generated.html')
        html_generated_file.touch(exist_ok=True)
        html_generated_file.write_text(html_template_code)

        generated_file_url = 'file://{}'.format(html_generated_file)
        print(webbrowser.Chromium.args)

        webbrowser.get(using='chromium-browser --app %s --new-window').open(generated_file_url, 1)


@begin
def main(exchange, quote_currency=None):
    """TradingView Charts launcher"""
    TradingViewChart().launch(exchange, quote_currency)
