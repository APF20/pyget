"""
To see which endpoints and topics are available, check the Bitget API
documentation at:
    https://bitgetlimited.github.io/apidoc/en/mix/#websocketapi

We can also create a REST Exchange object at the same time using:
async with Exchange() as session:
    rest = session.rest(...)
    ws = session.websocket(...)

For Bitget Testnet API WebSocket, modify the instType and/or symbol
strings as per Bitget documentation:
- add S (simulated) in front of instType (`SUMCBL`) for demo private subs.
- add S in front of base and coin (`SBTCSUSDT`) for demo public subs.

Subscriptions use `instType`, `channel` and `instId`, based on Bitget
documentation `Request Parameters`. See `WebSocket.args_to_topic()` for info
on required `pyget` formating. Example:
    ['instType.channel.instId', ...]
"""

# Import pyget and asyncio.
import asyncio
from pyget import Exchange

# Define our endpoint URL and subscriptions.
endpoint = 'wss://ws.bitget.com/mix/v1/stream'
subs = [
    'mc.ticker.SBTCSUSDT',      # testnet symbol
    'mc.candle1m.ETHUSDT',
    'sumcbl.positions.default',
    'sumcbl.orders.default'
]

# Define a coroutine and WebSocket object.
async def main():
    # Create callback functions for events.
    async def ticker(msg):
        print(f'Ticker event: {msg}')

    async def candle(msg):
        print(f'Candle event: {msg}')

    async def positions(msg):
        print(f'Positions event: {msg}')

    async def orders(msg):
        print(f'Orders event: {msg}')

    async def onError(err):
        print(err)

    async with Exchange() as session:
        # Connect without authentication!
        ws = session.websocket(endpoint, subscriptions=subs)

        # Let's bind ticker events to the ticker function
        ws.bind('mc.ticker.SBTCSUSDT', ticker)

        # Let's bind kline/candle events to the klines function
        ws.bind('mc.candle1m.ETHUSDT', candle)

        # Connect with authentication!
        ws_auth = session.websocket(
            endpoint,
            subscriptions=subs,
            api_key='...',
            api_secret='...',
            passphrase='...'
            error_cb_func=onError
        )

        # Bind position events stream to the position function.
        # Note that no position data is received until a change
        # in your position occurs (initially, there will be no data).
        ws_auth.bind('sumcbl.positions.default', positions)
        ws_auth.bind('sumcbl.orders.default', orders)

        # Start the streaming events
        await asyncio.gather(
            ws.run_forever(),
            ws_auth.run_forever(),
        )

asyncio.run(main())
