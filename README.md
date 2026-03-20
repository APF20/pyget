# pyget
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-2-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

[![Python versions](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11-blue)](https://www.python.org/downloads/)
[![Build Status](https://img.shields.io/github/v/tag/APF20/pyget)](https://github.com/APF20/pyget/releases)
[![Build Status](https://img.shields.io/github/v/release/APF20/pyget)](https://github.com/APF20/pyget/releases)
[![CI](https://github.com/APF20/pyget/actions/workflows/ci.yml/badge.svg)](https://github.com/APF20/pyget/actions/workflows/ci.yml)
![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)

Asyncronous Python3 API connector for Bitget's HTTP and Websockets APIs.

## Table of Contents

- [About](#about)
- [Development](#development)
- [Installation](#installation)
- [Usage](#usage)
- [Contact](#contact)
- [Contributors](#contributors)
- [Donations](#donations)

## About
Put simply, `pyget` (Python + Bitget) is a lightweight, fast, asyncronous one-stop-shop
module for the Bitget REST HTTP and WebSocket APIs. It is built using built in `asyncio`
library and the `aiohttp` library.

I was never a fan of connectors that used a mosh-pit of various modules that you didn't
want, used up valuable resources and slowed down the connector, particularly with
syncronous code. So I decided to build my own Python3-dedicated connector with very
little external resources (`pyget` uses only `aiohttp` package). The goal of the
connector is to provide traders and developers with an easy-to-use, lightning fast
asyncronous API connector module.

## Development
`pyget` was a private module as part of proprietary trading strategies, it was being
actively developed, especially since Bitget was making changes and improvements to
their API on a regular basis. It is compatible up to V1 of the Bitget APIs. It has
now been open-sourced and is offered as a public, true `community` project. 

`pyget` uses aiohttp for its methods, alongside other built-in modules, such as asyncio,
for high performance asyncronous operations.

Feel free to fork this repository, issue reports for any bugs and add pull requests for any
improvements and updates to Bitget API changes.

## Installation
`pyget` requires Python 3.9 or higher. The module can be installed manually. Pypi
installation support will be considered.
```
# Production installation
pip install .

# Developer/Editable installation
pip install -e .
```

## Usage
You can retrieve the HTTP and WebSocket classes like so:
```python
import asyncio
from pyget import Exchange
```
Create an HTTP session and connect via WebSocket using context manager protocol:
```python
async def main():
    async with Exchange() as session:
        rest = session.rest(
            endpoint='https://api.bitget.com',
            api_key='...',
            api_secret='...',
            passphrase=...,
            contract_type='futures',
            force_retry=True
        )
        ws = session.websocket(
            endpoint='wss://ws.bitget.com/mix/v1/stream',
            subscriptions=['mc.candle1m.ETHUSDT']
        )
asyncio.run(main())
```
Information can be sent to, or retrieved from, the Bitget APIs:
```python
async def main():
    async with Exchange() as session:
        rest = session.rest(...)

        # Get symbol ticker.
        await rest.do('get_single_symbol_ticker', symbol='BTCUSDT_UMCBL')

        # Create five long orders.
        orders = [{
            'size': '0.1',
            'price': i,
            'side': 'open_long', 
            'orderType': 'limit'
        } for i in ['5000', '5500', '6000', '6500', '7000']]

        # Submit the orders in bulk, asyncronously.
        await self.rest.do('batch_order',
            symbol = 'BTCUSDT_UMCBL',
            marginCoin = 'USDT',
            orderDataList = orders
        )

asyncio.run(main())
```
Check out the example python files, in the examples directory, for
more information, documentation and examples on available endpoints
and methods for the `HTTP` and `WebSocket` classes.

## Contact
I'm pretty responsive here on [Github](https://github.com).

## Contributors

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
      <td align="center"><a href="https://github.com/APF20"><img src="https://avatars0.githubusercontent.com/u/74583612?v=4" width="100px;" alt=""/><br /><sub><b>APF20</b></sub></a><br /><a href="https://github.com/APF20/pyget/commits?author=APF20" title="Code">💻</a>  <a href="https://github.com/APF20/pyget/commits?author=APF20" title="Documentation">📖</a></td>
  </tr>
</table>

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) 
specification. Contributions of any kind welcome!

## Donations

I work on `pyget` in my spare time. If you like the project and want to donate, 
you can do so to the following addresses:

```
SOL: HoUMsBKUESB9fsVTNtT4jYGnAzTAH9LNpZHjXvPiZ5Tb
BTC: bc1q4y230tg3rrhty9zxwpm63g5sgaqxw83xuwahjk
ETH: 0x06fd9aad799c5f094ce8c941fae9b81967cd8323
```
