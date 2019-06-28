# PyTVC: Python TradingView Chart

- **Author**: Daniel J. Umpierrez
- **License**: UNLICENSE

## Description

TradingView chart launcher from CLI using the Chrome (or similar) "desktop like" app launch feature

Some features:
- Set as many technical indicators as you need.
- Watchlist 24h volume filtering.
- Watchlist base market filtering.

## Installation

### From GitHub repo using `git`

```sh
git clone https://github.com/havocesp/pytvc
cd pytvc
pip install -r requirements.txt
pip install -r https://raw.githubusercontent.com/havocesp/pytvc/master/requirements.txt
pip install .
```

### From GitHub repo using `pip`

```sh
pip install git+https://github.com/havocesp/pytvc
```

## Usage

### From CLI `pytvc` command

The following command will retrieve and display the last hour "gainers" currencies listed on supplied exchanges every 60 seconds. 

```sh
pytvc binance cryptopia hitbtc --loop
```

## TODO

- [ ] Add watchlist symbols as arguments.
- [ ] Add arg to set initial initial symbol (default BTC/USDT)

## ChangeLog

### 0.1.4
- CLI params simplified
- Added Brave browser
- Many errors fixed

### 0.1.3

- Added min volume filtering

### 0.1.2

- Removed duplicate "pytvc" dir
- Added some lines to README.md
- Minor errors fixed

### 0.1.1

- Removed duplicate "pytvc" dir
- Added some lines to README.md
- Minor errors fixed

### 0.1.0

- Initial version
