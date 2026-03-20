"""
pyget
------------------------

pyget is a lightweight, high-performance and asyncronous API
connector for the RESTful and WebSocket APIs of the Bitget exchange.

Documentation can be found at
https://github.com/APF20/pyget

:copyright: (c) 2023 APF20

:license: MIT License

"""

import time
import hmac
import asyncio
import aiohttp
import json
import base64

from .exceptions import FailedRequestError, InvalidRequestError, WebSocketException
from .endpoints import Endpoints
from .log import Logger


# VERSION = '3.3.2'

#
# Helpers
#
#LOGGER = log.setup_custom_logger('root', streamLevel='INFO')


class Exchange:
    """
    Exchange Interface for pyget REST and WebSocket API
    """

    def __init__(self, logger=None):
        self.session = aiohttp.ClientSession()
        self.logger = logger if logger else Logger().setup_custom_logger('root', streamLevel='INFO')

    async def __aenter__(self):
        return self

    async def __aexit__(self, *err):
        await self.exit()

    async def exit(self):
        """Closes the aiohttp session."""
        await self.session.close()
        self.logger.info('Exchange session closed.')

    def rest(self, **kwargs):
        """
        Create REST Object.

        :param kwargs: See REST Class.
        :returns: REST Object.
        """
        return REST(self.session, self.logger, **kwargs)

    def websocket(self, endpoint, **kwargs):
        """
        Create WebSocket Object.

        :param str endpoint: Required parameter. The endpoint of the remote
            websocket.
        :param kwargs: See WebSocket Class.
        :returns: REST WebSocket Object.
        """
        return WebSocket(self.session, self.logger, endpoint, **kwargs)

    @property
    def clientSession(self):
        return self.session

    @property
    def exchangeLogger(self):
        return self.logger


class REST:
    """
    Connector for Bitget's REST API.

    :param obj session: Required parameter. An aiohttp ClientSession constructed
        session instance.
    :param obj logger: Required parameter. An initialised logging object.
    :param str endpoint: The base endpoint URL of the REST API, e.g.
        'https://api.bitget.com'.
    :param str api_key: Your API key. Required for authenticated endpoints. Defaults
        to None.
    :param str api_secret: Your API secret key. Required for authenticated
        endpoints. Defaults to None.
    :param str passphrase: Your API key password. Required for authenticated
        endpoints. Defaults to None.
    :param logging_level: The logging level of the built-in logger. Defaults to
        logging.INFO. Options are CRITICAL (50), ERROR (40), WARNING (30),
        INFO (20), DEBUG (10), or NOTSET (0).
    :type logging_level: Union[int, logging.level]
    :param bool log_requests: Whether or not pyget should log each REST request.
    :param int request_timeout: The timeout of each REST request in seconds. Defaults
        to 10 seconds.
    :param bool force_retry: Whether or not pyget should retry a timed-out request.
    :param set retry_codes: A list of non-fatal status codes to retry on.
    :param set ignore_codes: A list of non-fatal status codes to ignore.
    :param int max_retries: The number of times to re-attempt a request.
    :param int retry_delay: Seconds between retries for returned error or timed-out
        requests. Default is 2 seconds.
    :param str contract_type: The contract type endpoints to use for requests. e.g.
        'futures', 'spot', 'margin', 'p2p', 'sub_account', 'tax'. Can be dynamically
        changed by using set_contract_type().

    :returns: pyget.REST session.

    """
  
    def __init__(self, session, logger, *, endpoint=None, api_key=None, api_secret=None,
                 passphrase=None, logging_level='INFO', log_requests=False,
                 request_timeout=10, force_retry=False, retry_codes=None,
                 ignore_codes=None, max_retries=3, retry_delay=2,
                 contract_type=None):

        """Initializes the REST class."""

        # Set the base endpoint url.
        self.url = 'https://api.bitget.com' if not endpoint else endpoint

        # Setup logger.
        self.logger = logger
        self.logger.info('Initializing pyget REST session.')
        self.log_requests = log_requests

        # Validate API keys.
        if api_key and (api_secret is None or passphrase is None):
            raise PermissionError(
                'You must be authorized to use private interface!'
            )

        # Set API keys.
        self.api_key = api_key
        self.api_secret = api_secret
        self.passphrase = passphrase

        # Set timeout to ClientTimeout sentinel.
        self.timeout = aiohttp.ClientTimeout(sock_read=request_timeout)
        self.force_retry = force_retry
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        # Set whitelist of non-fatal Bitget status codes to retry on.
        self.retry_codes = {
            '429',    # request too frequent
            '40008',  # request timestamp expired
            '40010',  # request timed out
            '40015',  # system error
            '43025',  # limit order does not exist
            '40725',  # service returned an error
            '45001'   # unknown error
        } if not retry_codes else retry_codes

        # Set whitelist of non-fatal Bitget status codes to ignore.
        self.ignore_codes = {} if not ignore_codes else ignore_codes

        # Set aiohttp client session.
        self.session = session

        # Set default aiohttp headers.
        self.headers = {
            'User-Agent': 'pyget',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        # Set contract type
        self.set_contract_type(contract_type)

    async def __aenter__(self):
        return self

    async def __aexit__(self, *err):
        await self.exit()

    async def exit(self):
        """Closes the aiohttp session."""
        await self.session.close()
        self.logger.info('REST session closed.')

    async def _sem_gather(self, n: int, *aws):
        """Semaphore async gather with concurrent rate limit"""

        sem = asyncio.BoundedSemaphore(n)

        async def sem_task(task):
            async with sem:
                return await task

        return await asyncio.gather(*(sem_task(task) for task in aws))

    def set_contract_type(self, type: str):
        """
        Set contract_type var and endpoints dict based on contract type.

        :param str type: Contract type e.g. futures, spot, margin, p2p,
            sub_account, tax.
        """

        if type:
            self.logger.info(f'Using {type} contract type endpoints.')
            self.endpoints = {**getattr(Endpoints, type)}

        else:
            self.endpoints = {}
            self.logger.warning(
                'Contract type is not set. Only account asset endpoints are available. '
                'Use contract_type init param or set_contract_type() to set/change.'
            )

        # add common endpoints for account asset
        self.endpoints.update(Endpoints.common)

    async def do(self, endpoint, **kwargs):
        """
        Perform REST API endpoint operations.

        :param kwargs: See
            https://bitgetlimited.github.io/apidoc/en
        :returns: Request results as dictionary.
        """

        method, auth, path = self.endpoints[endpoint]

        return await self._submit_request(
            method=method,
            path=path,
            query=kwargs,
            auth=auth
        )


    '''
    Additional Methods
    These methods use requests to perform a specific
    function and are exclusive to pyget.
    '''

    async def batch_modify_order(self, orders: list, max_in_parallel=10):
        """
        Replaces multiple active orders in bulk using async concurrency. For more
        information on modify_order, see
        https://bitgetlimited.github.io/apidoc/en/mix/#modify-order

        :param list orders: A list of orders and their parameters.
        :param max_in_parallel: The number of requests to be sent in parallel.
            Note that you are limited to 50 requests per second.
        :returns: Future request result dictionaries as a list.
        """

        res = await self._sem_gather(
            max_in_parallel,
            *[self.do('modify_order', **order) for order in orders]
        )
        return [r for r in res]


    '''
    Internal methods; signature and request submission.
    For more information about the request signature, see
    https://bitgetlimited.github.io/apidoc/en/mix/#api-verification.
    '''

    def _auth(self, method, path, params, body):
        """
        Generates authentication headers per Bitget API specifications.
        """

        api_key = self.api_key
        api_secret = self.api_secret

        if api_key is None:
            raise PermissionError('Authenticated endpoints require keys.')

        # Generate querystring for GET requests.
        if params and not body:
            qs = '&'.join(
                [f'{str(k)}={str(v)}' for k, v in params.items() if
                 v is not None]
            )

            # Append querystring to path.
            path = f'{path}?{qs}'

        # Generate timestamp in milliseconds.
        timestamp = int((time.time() * 10 ** 3))

        # Generate message value to sign.
        _val = f'{timestamp}{method}{path}{body}'

        # Generate signature.
        signature = str(
            base64.b64encode(
                hmac.new(
                    bytes(api_secret, 'utf-8'),
                    bytes(_val, 'utf-8'),
                    digestmod='sha256'
                ).digest()
            ), 'utf-8'
        )

        # Return headers
        return self._auth_headers(signature, timestamp)

    def _auth_headers(self, signature, timestamp):
        """
        Generates authentication headers dictionary.
        """

        headers = self.headers
        headers['ACCESS-KEY'] = self.api_key
        headers['ACCESS-SIGN'] = signature
        headers['ACCESS-TIMESTAMP'] = str(timestamp)
        headers['ACCESS-PASSPHRASE'] = self.passphrase
      
        return headers

    async def _submit_request(self, method, path, *, query=None, auth=False):
        """
        Submits the request to the API.

        Notes
        -------------------
        We use the params argument for the GET method, and data (bytes) argument
        for the POST method. Dicts passed to the json argument are automatically
        JSONified, byte encoded and set to data argument, by ClientSession handler
        prior to submitting request.
        """

        # Define query parameters.
        if query:
            req_params = {k: v for k, v in query.items() if
                          v is not None}
        else:
            req_params = {}

        # Form absolute url.
        url = self.url + path

        # Send request and return headers with body. Retry if failed.
        retries_attempted = self.max_retries

        while True:

            retries_attempted -= 1
            if retries_attempted < 0:
                raise FailedRequestError(
                    request=f'{method} {url}: {req_params}',
                    message='Bad Request. Retries exceeded maximum.',
                    status_code=400,
                    time = time.strftime("%H:%M:%S", time.gmtime())
                )

            retries_remaining = f'{retries_attempted} retries remain.'

            # Set default request headers and body.
            r = {'headers': self.headers}
            body = ''

            # Prepare request; use 'params' for GET and b'data' for POST.
            if method == 'GET':
                r['params'] = req_params

            elif req_params:

                # JSONify body for POST request signature.
                body = json.dumps(req_params)

                # Encode to bytes, per JsonPayload method of session.
                r['data'] = body.encode('utf-8')

            # Authenticate if we are using a private endpoint.
            if auth:
                # Prepare and append auth headers to the dictionary.
                r['headers'] = self._auth(method, path, req_params, body)

            # Log the request.
            if self.log_requests:
                self.logger.info(f'Request -> {method} {url}: {req_params}')

            # Attempt the request.
            try:
                async with self.session.request(
                    method, url, **r, timeout=self.timeout
                ) as s:

                    # Convert response to dictionary, or raise if requests error.
                    try:
                        s_json = await s.json()

                    # If we have trouble converting, handle the error and retry.
                    except aiohttp.client_exceptions.ContentTypeError as e:
                        if self.force_retry:
                            self.logger.error(f'REST {e}. {retries_remaining}')
                            await asyncio.sleep(self.retry_delay)
                            continue
                        else:
                            raise FailedRequestError(
                                request=f'{method} {url}: {req_params}',
                                message='Conflict. Could not decode JSON.',
                                status_code=409,
                                time = time.strftime("%H:%M:%S", time.gmtime())
                            )

            # If requests fires an error, retry.
            except (
                aiohttp.client_exceptions.ClientConnectorError,
                aiohttp.client_exceptions.ServerConnectionError
            ) as e:
                if self.force_retry:
                    self.logger.error(f'REST {e}. {retries_remaining}')
                    await asyncio.sleep(self.retry_delay)
                    continue
                else:
                    raise e

            # Return response if no error. Handle malformed responses that only return a
            # list, eg. get_candle_data endpoint, by checking for 'code' existence first.
            if not 'code' in s_json or s_json['code'] == '00000':
                return s_json

            # Bitget returned an error, so handle and/or raise.

            # Generate error message.
            error_msg = (f'REST {s_json["msg"]} (HTTPStatus: {s.status}) (ErrCode: {s_json["code"]})')

            # Set default retry delay.
            err_delay = self.retry_delay

            # Retry non-fatal whitelisted error requests.
            if s_json['code'] in self.retry_codes:

                # 429, request too frequent; wait err_delay seconds and retry.
                if s_json['code'] == '429':

                    self.logger.error(f'429 ERROR MSG: {s_json}')
                    self.logger.error(
                        f'{error_msg}. Ratelimited on current request. '
                        f'Sleeping, then trying again. Request: {url}'
                    )

                    # Calculate how long we need to wait.
                    error_msg =(
                        f'Sleeping for {err_delay} seconds'
                    )

                # Log the error.
                self.logger.error(f'{error_msg}. {retries_remaining}')
                await asyncio.sleep(err_delay)
                continue

            # Ignore whitelisted error requests.
            elif s_json['code'] in self.ignore_codes:
                pass

            # Raise for invalid authorization errors.
            elif s_json['code'] in {'40005', '40006', '40009', '40012', '40014'}:
                raise PermissionError(
                    f'Authorization failed. Please check your API keys and restart. '
                    f'Error: {error_msg}).'
                )

            else:
                raise InvalidRequestError(
                    request=f'{method} {url}: {req_params}',
                    message=s_json["msg"],
                    status_code=s_json["code"],
                    time=time.strftime("%H:%M:%S", time.gmtime())
                )



class WebSocket:
    """
    Connector for Bitget's WebSocket API.

    :param obj session: Required parameter. An aiohttp ClientSession constructed
        session instance.
    :param obj logger: Required parameter. An initialised logging object.
    :param str endpoint: Required parameter. The endpoint of the remote
        websocket.
    :param str api_key: Your API key. Required for authenticated endpoints.
        Defaults to None.
    :param str api_secret: Your API secret key. Required for authenticated
        endpoints. Defaults to None.
    :param str passphrase: Your API key password. Required for authenticated
        endpoints. Defaults to None.
    :param list subscriptions: A list of desired topics to subscribe to. See
        args_to_topic() method and Bitget API documentation for more information.
        Defaults to None.
    :param str logging_level: The logging level of the built-in logger. Defaults
        to logging.INFO. Options are CRITICAL (50), ERROR (40), WARNING (30),
        INFO (20), DEBUG (10), or NOTSET (0).
    :param int ping_interval: The number of seconds between each automated ping.
        Pong timeout is based on ping_interval/2.
    :param bool restart_on_error: Whether or not the connection should restart
        on error.
    :param func error_cb_func: Callback function to bind to exception error
        handling.

    :returns: WebSocket session.
    """

    def __init__(self, session, logger, endpoint, *, api_key=None, api_secret=None,
                 passphrase=None, subscriptions=None, logging_level='INFO',
                 ping_interval=20, restart_on_error=True, error_cb_func=None):

        """
        Initializes the websocket session.
        """

        # Set websocket name for logging purposes
        self.wsName = 'Authenticated' if api_key else 'Non-Authenticated'

        # Setup logger.
        self.logger = logger
        self.logger.info(f'Initializing pyget {self.wsName} WebSocket.')

        # Set aiohttp client session.
        self.session = session

        # Set endpoint.
        self.endpoint = endpoint

        # Set API keys.
        self.api_key = api_key
        self.api_secret = api_secret
        self.passphrase = passphrase

        # Initialize subscriptions set.
        self.subscriptions = set()

        # Validate/set topic subscriptions for WebSocket.
        if subscriptions:
            self._validate_subs(subscriptions)
            self.subscriptions.update(subscriptions)

        # Set ping settings.
        self.ping_interval = ping_interval

        # Other optional data handling settings.
        self.handle_error = restart_on_error

        # Initialize handlers dictionary
        self.handlers = {}

        # Bind error handler callback function
        if error_cb_func:
            self.bind('error_cb', error_cb_func)

        # Set initial state and initialize dictionary.
        self._reset()

    def _reset(self):
        """
        Set state booleans and initialize dictionary.
        """

        self.exited = False
        self.ws = None
        self.logged_in = False
        self.connected = False
        self._subscribed = set()

    def _validate_subs(self, subscriptions):
        """
        Validate subscriptions and permissions.
        """

        if not subscriptions:
            raise Exception('Subscription list cannot be empty!')

        # Ensure subscriptions is a list.
        elif isinstance(subscriptions, str):
            subscriptions = [subscriptions]

        # Ensure authentication for private topics.
        if any(c in s for s in subscriptions for c in [
            'account',
            'positions',
            'orders',
            'ordersAlgo'
        ]) and None in (self.api_key, self.api_secret, self.passphrase):
            raise PermissionError('You must be authorized to use '
                                  'private topics!')

    async def subscribe(self, subscriptions):
        """
        Subscribe to websocket topics. See args_to_topic() for info.

        :param list subscriptions: Subscriptions in required
            format: ['instType.channel.instId', ...]
        """

        # Validate subscriptions and update set.
        self._validate_subs(subscriptions)
        self.subscriptions.update(subscriptions)

        # Wait for connection to be opened/auth before subscribing.
        if not self.connected:
            self.logger.info(f'Waiting for WebSocket {self.wsName} to connect.')
            return

        # Generate list of current, non subscribed topics.
        topics = list(self.subscriptions - self._subscribed)

        if not topics:
            self.logger.info(f'Subscribe {subscriptions}, nothing to do!')
            return

        # Generate subscription args as list of dicts.
        args = self.topics_to_args(topics)
        self.logger.info(f"Subscribing to {args}.")

        # Subscribe to the requested topics.
        await self.ws.send_json({
            'op': 'subscribe',
            'args': args
        })

    async def unsubscribe(self, subscriptions):
        """
        Unsubscribe from websocket topics.

        :param list subscriptions: Subscriptions in required
            format: ['instType.channel.instId', ...]
        """

        # Validate and discard subscriptions from set
        self._validate_subs(subscriptions)
        self.subscriptions -= set(subscriptions)

        # Generate intersection list from current, subscribed topics.
        topics = [s for s in subscriptions if s in self._subscribed]

        if not topics:
            self.logger.info(f'Unsubscribe {subscriptions}, nothing to do!')
            return

        # Generate Unsubscribe args as list of dicts.
        args = self.topics_to_args(topics)
        self.logger.info(f"Unsubscribing from {args}.")

        # Unsubscribe from the requested topics.
        await self.ws.send_json({
            'op': 'unsubscribe',
            'args': args
        })

    async def ping(self):
        """
        Pings the remote server to test the connection. The status of the
        connection can be monitored using self.ws.ping().
        Bitget uses str type ping/pong.
        """

        await self.ws.send_str('ping')

    async def _heartbeat(self):
        while 1:
            await asyncio.sleep(self.ping_interval)
            await self.ping()

    async def _connect(self):
        """
        Open websocket in a thread.
        """

        # Attempt to connect for X seconds.
        retries = 10
        while retries > 0:

            # Connect to WebSocket.
            try:
                self.ws = await self.session.ws_connect(
                    self.endpoint,
                )

            # Handle errors during connection phase.
            except(
                aiohttp.client_exceptions.WSServerHandshakeError,
                aiohttp.client_exceptions.ClientConnectorError
            ) as e:
                self.logger.error(f'WebSocket connection {e!r}')
                retries -= 1

                # If connection was not successful, raise error.
                if retries <= 0:
                    raise WebSocketException(e)

            else:
                break

            await asyncio.sleep(1)

    async def _auth(self):
        """
        Authorize websocket connection.
        """

        # Generate timestamp in seconds.
        timestamp = int((time.time() + 1))

        # Generate signature.
        _val = f'{timestamp}GET/user/verify'
        signature = str(
            base64.b64encode(
                hmac.new(
                    bytes(self.api_secret, 'utf-8'),
                    bytes(_val, 'utf-8'), digestmod='sha256'
                ).digest()
            ), 'utf-8'
        )

        # Authenticate with API.
        await self.ws.send_json({
            'op': 'login',
            'args': [{
                'apiKey': self.api_key,
                'passphrase': self.passphrase,
                'timestamp': timestamp,
                'sign': signature
            }]
        })

    async def _dispatch(self):

        while True:
            msg = await self.ws.receive()

            if msg.type == aiohttp.WSMsgType.TEXT:

                # Convert message to json and consume.
                try:
                    await self._consume(json.loads(msg.data))

                except json.decoder.JSONDecodeError as e:

                    # pong packet is sent as str
                    if msg.data == 'pong':
                        continue

                    raise e

            elif msg.type == aiohttp.WSMsgType.ERROR:
                raise WebSocketException(f'WebSocket connection error. Code: {self.ws.close_code}; {msg}')

            # Handle EofStream (type 257, etc)
            elif msg.type in (
                aiohttp.WSMsgType.CLOSE,
                aiohttp.WSMsgType.CLOSING,
                aiohttp.WSMsgType.CLOSED
            ):
                raise WebSocketException(f'WebSocket connection closed. Code: {self.ws.close_code}; {msg}')

    async def _consume(self, msg: dict):
        """
        Consumer to parse and emit incoming messages.
        """

        if 'action' in msg:
            await self._emit(self.args_to_topic(msg['arg']), msg)

        elif 'event' in msg:

            if msg['event'] == 'login':
                if msg['code'] == 0:
                    self._on_login()

            elif msg['event'] == 'subscribe':
                self._on_subscribe(self.args_to_topic(msg['arg']))

            elif msg['event'] == 'unsubscribe':
                self._on_unsubscribe(self.args_to_topic(msg['arg']))

            elif msg['event'] == 'error':

                # channel does not exist; invalid op
                if msg['code'] in {30001, 30003}:
                    raise WebSocketException(
                        f'Couldn\'t subscribe to topic. Error: {msg["msg"]} (ErrCode: {msg["code"]}).'
                    )

                # login failed; invalid access key; invalid passphrase; user needs to log in
                elif msg['code'] in {30004, 30005, 30011, 30012}:
                    raise PermissionError(
                        f'Authorization failed. Please check your API keys and restart. '
                        f'Error: {msg["msg"]} (ErrCode: {msg["code"]}).'
                    )

                else:
                    raise WebSocketException(f'Error: {msg["msg"]} (ErrCode: {msg["code"]}).')

    @staticmethod
    def args_to_topic(args: dict):
        """
        Generate topics to match common format: [instType].[channel].[instId]
        eg. mc.ticker.BTCUSDT, UMCBL.account.default

        :param dict args: with parsed json, in received message format. eg.:
                 {"instType":"mc","channel":"ticker","instId":"btcusdt"}
        :returns: Formatted topic as str, eg. 'mc.ticker.btcusdt'.
        """

        return f'{args["instType"]}.{args["channel"]}.{args["instId"]}'

    @staticmethod
    def topics_to_args(topics: list):
        """
        Generate subscription args as list of dicts, from common topic format list:
        ["[instType].[channel].[instId]",..]

        :param list topics: eg. ["mc.ticker.BTCUSDT", "UMCBL.account.default"]
        :returns: Formatted args as list of dicts, eg.
            [{"instType":"mc","channel":"ticker","instId":"btcusdt"},..]
        """

        return [
            {
                'instType': x[0],
                'channel': x[1],
                'instId': x[2]
            } for x in (s.split('.') for s in topics)
        ]

    async def _emit(self, topic: str, msg):
        """
        Send message data events to binded callback functions.

        :param topic: Required. Subscription topic.
        :param msg: Required. Message event json data.
        """

        await self.handlers[topic](msg)

    def bind(self, topic, func):
        """
        Bind functions by topic to local object to handle websocket message events.

        :param topic: Required. Subscription topic.
        :param func: Required. Callback Function to handle processing of events.
        """

        if not asyncio.iscoroutinefunction(func):
            raise ValueError(f'Binded handler {func} must be coroutine function!')

        # Bind function handler to topic events.
        self.handlers[topic] = func

    def unbind(self, topic):
        """
        UnBind functions from local websocket message events.

        :param topic: Required. Subscription topic.
        """

        del self.handlers[topic]

    async def _on_open(self):
        """
        Perform tasks on WS open.
        """

        self.logger.info(f'WebSocket {self.wsName} opened.')

        # If given an api_key, authenticate.
        if self.api_key:
            await self._auth()

            # Wait for authentication success before subscribing.
            self.logger.info('Waiting for login authentication.')
            while not self.logged_in:
                await asyncio.sleep(0.01)

        # Connection is open.
        self.connected = True

        # Subscribe to websocket topics.
        if self.subscriptions:
            await self.subscribe(self.subscriptions)

    def _on_login(self):
        self.logged_in = True
        self.logger.info('Authorization successful.')

    def _on_subscribe(self, topic):
        """
        Log and store WS subscription successes.
        """

        self.logger.info(f'Subscription to {topic} successful.')
        self._subscribed.add(topic)

    def _on_unsubscribe(self, topic):
        """
        Log and store WS subscription successes.
        """

        self.logger.info(f'Subscription to {topic} successful.')
        self._subscribed.add(topic)

    def _on_unsubscribe(self, topic):
        """
        Log and remove WS unsubscribe successes.
        """

        self.logger.info(f'Unsubscribe to {topic} successful.')
        self._subscribed.discard(topic)

    @property
    def subscribed(self):
        return self._subscribed

    async def _on_close(self):
        """
        Perform tasks on WS close.
        """

        self.logger.info(f'WebSocket {self.wsName} closed.')
        await self.exit()

    async def _on_error(self, error):
        """
        Exit on errors and raise exception, or attempt reconnect.
        """

        t = time.strftime("%H:%M:%S", time.gmtime())
        self.logger.error(
            f'WebSocket {self.wsName} encountered a {error!r} (ErrTime: {t} UTC).'
        )
        await self.exit()

        if 'error_cb' in self.handlers:
            await self._emit('error_cb', error)

        # Reconnect.
        if self.handle_error:
            self.logger.info(f'WebSocket {self.wsName} reconnecting.')
            self._reset()

    async def exit(self):
        """
        Closes the websocket connection.
        """

        if self.ws:
            await self.ws.close()
        self.exited = True
        self.ws = None
        self.connected = False

    async def run_forever(self):

        self.logger.debug(f'WebSocket {self.wsName} starting stream.')

        while not self.exited:

            try:
                if not self.ws:
                    await self._connect()

                # Launch dispatch as background task to process packets.
                task = asyncio.create_task(self._dispatch())

                # Open topics and Force ping loop to keep connection alive.
                await asyncio.gather(task, self._on_open(), self._heartbeat())

            except asyncio.CancelledError as e:
                self.logger.warning(f'Asyncio interrupt received.')
                self.exited = True
                break

            except WebSocketException as e:
                await self._on_error(e)

            except PermissionError as e:
                self.handle_error = False
                await self._on_error(e)

            finally:
                if self.exited:
                    await self._on_close()
                    break

            # Give event loop a foothold to juggle between coroutines
            await asyncio.sleep(0.01)
