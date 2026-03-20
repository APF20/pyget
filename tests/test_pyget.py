import unittest, asyncio, aiohttp
import pyget
from unittest.mock import AsyncMock, patch, MagicMock, DEFAULT

REST_URL = 'https://api.bitget.com'
REST_CONTRACT_TYPE = 'futures'
WS_PUBLIC_URL = 'wss://ws.bitget.com/mix/v1/stream'
SUBS = ['mc.ticker.BTCUSDT']

class TestSession:

    async def setUpREST(self):
        """Set up the real Exchange and HTTP chain"""
        self.exchange = pyget.Exchange()
        self.rest = self.exchange.rest(
            endpoint=REST_URL,
            contract_type=REST_CONTRACT_TYPE
        )

    async def setUpWebSocket(self):
        """Set up the real Exchange and WebSocket chain"""
        self.exchange = pyget.Exchange()
        self.ws = self.exchange.websocket(
            endpoint=WS_PUBLIC_URL,
            subscriptions=SUBS,
            restart_on_error=False
        )

    async def tearDown(self):
        await self.exchange.exit()

class EndOfTestException(Exception):
    """Raised by mocks to signal test completion"""
    pass

class HTTPTest(unittest.IsolatedAsyncioTestCase):
    """Test the HTTP class from pyget module"""

    session = TestSession()
    api_key = '1234567890'
    api_secret = 'abcdefghijkl'
    passphrase = 'test_phrase'
    timestamp = 1234567890

    @classmethod
    def setUpClass(cls):
        asyncio.run(cls.session.setUpREST())

    @classmethod
    def tearDownClass(cls):
        asyncio.run(cls.session.tearDown())

    def test_set_contract_type(self):
        endpoint = ('get_all_symbols', ('GET', False, '/api/mix/v1/market/contracts'))

        with patch.object(pyget.endpoints.Endpoints, REST_CONTRACT_TYPE, new={endpoint[0]: endpoint[1]}):
            self.session.rest.set_contract_type(REST_CONTRACT_TYPE)
            self.assertEqual(self.session.rest.endpoints[endpoint[0]], endpoint[1])

    async def test_do(self):
        symbol = 'BTCUSDT'
        endpoint = ('get_all_symbols', ('GET', False, '/api/mix/v1/market/contracts'))

        with patch.multiple(self.session.rest, endpoints={endpoint[0]: endpoint[1]}, _submit_request=DEFAULT) as mocks:
            await self.session.rest.do(endpoint[0], symbol=symbol)
            method, auth, path = endpoint[1]
            mocks['_submit_request'].assert_called_once_with(
                method=method,
                path=path,
                query={'symbol': symbol},
                auth=auth
            )

    def test_auth(self):
        mock_args = ('GET', '/api/mix/v1/market/contracts', {'symbol': 'BTCUSDT'}, '')
        expected = {'signature': 'xPdEXLDbJvVX3gmN14rkrmO/VW0VAcjvDfAphn/hjr0=', 'timestamp': 1234567890000}

        with(
            patch.multiple(self.session.rest, api_key=self.api_key, api_secret=self.api_secret, _auth_headers=DEFAULT) as mocks,
            patch.object(pyget.time, 'time', return_value=self.timestamp)
         ):
            self.session.rest._auth(*mock_args) # method, path, params, body = mock_args
            mocks['_auth_headers'].assert_called_once_with(expected['signature'], expected['timestamp'])

    async def test_submit_request(self):
        url = REST_URL
        mock_path = '/api/mix/v1/market/contracts'
        mock_query = {'symbol': 'BTCUSDT'}
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        auth_headers = {'ACCESS-KEY': '1234567890', 'ACCESS-SIGN': 'test-signature'}

        # cases: (name, (method, path, query, auth), expected)
        cases = [
            ('get', ('GET', mock_path, mock_query, False), headers),
            ('post', ('POST', mock_path, mock_query, False), headers),
            ('auth', ('GET', mock_path, mock_query, True), auth_headers)
        ]

        for name, mock_args, expected in cases:

            with self.subTest(name=name):

                patch_kwargs = {'url': url, 'headers': headers}
                if name == 'auth':
                    patch_kwargs['_auth'] = MagicMock(return_value=auth_headers)

                with(
                    patch.multiple(self.session.rest, **patch_kwargs),
                    patch.object(self.session.rest.session, 'request') as mock_request
                ):
                    method, path, query, auth = mock_args
                    await self.session.rest._submit_request(method, path, query=query, auth=auth)

                    mock_request.assert_called_once()
                    args, kwargs = mock_request.call_args
                    self.assertEqual(args, (method, f'{url}{path}'))
                    self.assertIn('headers', kwargs)
                    self.assertEqual(kwargs['headers'], expected)

                    if name == 'post':
                        self.assertEqual(kwargs['data'], pyget.json.dumps(query).encode('utf-8'))
                    else:
                        self.assertEqual(kwargs['params'], query)

    async def test_full_chain_place_order(self):
        symbol = 'BTCUSDT'
        endpoint = 'place_order'
        expected_signature = 'cnfmz9vmo6av64TAyOA6i4viLXMPVCk+L4sxmTbug94='

        # cases: (name, json_data, exception)
        cases = [
            ('success', {'msg': 'success', 'data': {'orderID': '123456789'}}, None),
            ('failed', {'msg': 'Duplicate clientOid', 'code': '40786'}, pyget.exceptions.InvalidRequestError)
        ]

        for name, json_data, exc in cases:

            with self.subTest(name=name):
                response = AsyncMock()
                response.json = AsyncMock(return_value=json_data)

                with(
                    patch.multiple(self.session.rest, api_key=self.api_key, api_secret=self.api_secret, passphrase=self.passphrase),
                    patch.object(pyget.time, 'time', return_value=self.timestamp),
                    patch.object(self.session.rest.session, 'request') as mock_request
                ):
                    mock_request.return_value.__aenter__.return_value = response
                    mock_request.return_value.__aexit__.return_value = None

                    if exc:
                        with self.assertRaises(pyget.exceptions.InvalidRequestError) as e:
                            await self.session.rest.do(endpoint, symbol=symbol)
                        self.assertEqual(e.exception.status_code, json_data['code'])
                    else:
                        result = await self.session.rest.do(endpoint, symbol=symbol)
                        self.assertEqual(result, json_data)

                    _, kwargs = mock_request.call_args
                    self.assertEqual(kwargs['headers']['ACCESS-SIGN'], expected_signature)

    async def test_full_chain_auth_fail(self):
        """
        We can't really test full-chain authenticated endpoints without keys,
        but we can make sure it raises a PermissionError.
        """
        endpoint = 'place_order'
        mock_kwargs = {'symbol': 'BTCUSD', 'order_type': 'Market', 'side': 'Buy', 'qty': 1}

        with patch.object(self.session.rest.session, 'request', PermissionError()) as mock_request:
            with self.assertRaises(PermissionError):
                await self.session.rest.do(endpoint, **mock_kwargs)

class WebSocketTest(unittest.IsolatedAsyncioTestCase):
    """Test the WebSocket class from pyget module"""

    session = TestSession()

    @classmethod
    def setUpClass(cls):
        asyncio.run(cls.session.setUpWebSocket())
        cls.session.ws.bind(SUBS[0], cls.ws_callback)

    @classmethod
    def tearDownClass(cls):
        asyncio.run(cls.session.tearDown())

    async def ws_callback(msg):
        print(f'wsCB: {msg}')
        pass

    async def test_websocket(self):
        mock_arg = '{"instType": "mc", "channel": "candle1m", "instId": "SBTCSUSDT"}'
        mock_ws = AsyncMock()
        mock_ws.receive.side_effect = [
            MagicMock(type=aiohttp.WSMsgType.TEXT, data=f'{{"action": "update", "arg": {mock_arg}, "data": "test1"}}'),
            MagicMock(type=aiohttp.WSMsgType.TEXT, data=f'{{"action": "update", "arg": {mock_arg}, "data": "test2"}}'),
            EndOfTestException('End of test')
        ]

        with patch.object(self.session.ws.session, 'ws_connect', new=AsyncMock(return_value=mock_ws)):
            with patch.object(self.session.ws, '_emit') as mock_emit:
                with self.assertRaises(EndOfTestException):
                    await self.session.ws.run_forever()

                self.assertEqual(mock_emit.call_count, 2)
                call_args = mock_emit.call_args_list
                self.assertEqual(call_args[0][0][1]['data'], 'test1')
                self.assertEqual(call_args[1][0][1]['data'], 'test2')
              
