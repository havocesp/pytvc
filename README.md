# PyTVC: Python TradingView Chart

- **Author**: Daniel J. Umpierrez
- **License**: UNLICENSE

## Description

Just a simple browser launcher TradingView Chart launcher  with  widget 

## Installation

### From GitHub repo using `git`

```sh
$ git clone https://github.com/havocesp/pytvc
$ cd pytvc
$ pip install -r requirements.txt
$ pip install -r https://raw.githubusercontent.com/havocesp/pytvc/master/requirements.txt
$ pip install .
```

### From GitHub repo using `pip`

```
pip install git+https://github.com/havocesp/pytvc
```

## Usage

### From CLI `pytvc` command

The following command will retrieve and display the last hour "gainers" currencies listed on supplied exchanges every 60 seconds. 

```sh
pytvc binance cryptopia hitbtc --loop
```

## TODO

- [ ] Sorting any column supplied as argument. 
- [ ] More accurate diff by storing requested in loop mode historic data.
- [ ] Get exchanges where a currency is listed.
- [ ] Get currencies supported by a given exchange.
- [ ] Get FIAT and crypto-currency rate conversions.

## ChangeLog

### 0.1.1
- Removed duplicate "pytvc" dir
- Writed some project details at README.md
- Minor errors fixed

### 0.1.0

- Initial version
