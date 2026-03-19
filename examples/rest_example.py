"""
To see which endpoints are available, you can read the API docs at
https://bitgetlimited.github.io/apidoc/en/mix/

Some methods will have required parameters, while others may be optional.
The arguments in pyget methods match those provided in the Bitget API
documentation.

The following functions are available:

exit()
set_contract_type()
do()

Public Methods:
------------------------
# Futures
get_all_symbols()
get_depth()
get_single_symbol_ticker()
get_all_symbol_ticker()
vip_fee_rate()
get_recent_fills()
get_fills()
get_candle_data()
get_history_candle_data()
get_history_index_candle_data()
get_history_mark_candle_data()
get_symbol_index_price()
get_symbol_next_funding_time()
get_history_funding_rate()
get_current_funding_rate()
get_open_interest()
get_symbol_mark_price()
get_symbol_leverage()
get_position_tier()
get_risk_position_limit()

# Spot
get_coin_list()
get_symbols()
get_single_symbol()

get_single_ticker()
get_all_tickers()
get_recent_trades()
get_market_trades()
get_candle_data()
get_history_candle_data()
get_depth()
vip_fee_rate()

# Margin
get_cross_interest_rate_and_borrowable()
get_isolated_interest_rate_and_borrowable()
get_cross_tier_data()
get_isolated_tier_data()
get_support_currencies()

# Common
get_server_time()

Private Methods:
(requires authentication)
------------------------
# Futures
get_single_account()
get_account_list()
get_sub_account_contract_assets()
get_open_count()
change_leverage()
change_margin()
change_margin_mode()
change_hold_mode()
get_symbol_position()
get_symbol_position_v2()
get_all_position()
get_all_position_v2()
get_account_bill()
get_business_account_bill()

place_order()
reversal()
batch_order()
cancel_order()
batch_cancel_order()
modify_order()
cancel_order_by_symbol()
cancel_all_order()
close_all_position()
get_open_order()
get_all_open_order()
get_history_order()
get_producttype_history_orders()
get_order_details()
get_order_fill_detail()
get_producttype_order_fill_detail()
place_plan_order()
modify_plan_order()
modify_plan_order_tpsl()
place_stop_order()
place_trailing_stop_order()
place_position_tpsl()
modify_stop_order()
cancel_plan_order_tpsl()
cancel_plan_order_tpsl_by_symbol()
cancel_all_trigger_order_tpsl()
get_plan_order_tpsl_list()
get_history_plan_orders_tpsl()

Spot Methods:
(many of the above methods can also be used with the spot market,
provided the argument contract_type='spot' is passed,
or set_contract_type('spot') method is called.)
------------------------
transfer()
transfer_v2()
sub_transfer()
get_coin_address()
withdraw()
withdraw_v2()
inner_withdraw()
inner_withdraw_v2()
get_withdraw_list()
get_deposit_list()
get_user_fee_ratio()

get_apikey_info()
get_account_assets()
get_account_assets_lite()
get_sub_account_spot_assets()
get_bills()
get_transfer_list()

place_order()
batch_order()
cancel_order()
cancel_order_v2()
cancel_order_by_symbol()
cancel_order_in_batch()
cancel_order_in_batch_v2()
get_order_details()
get_order_list()
get_order_history()
get_transaction_details()
place_plan_order()
modify_plan_order()
cancel_plan_order()
get_current_plan_orders()
get_historic_plan_orders()
batch_cancel_plan_orders()

# Margin
get_cross_assets()
get_isolated_assets()
cross_borrow()
isolated_borrow()
cross_repay()
isolated_repay()
get_cross_risk_rate()
isolated_risk_rate()
cross_max_borrowable_amount()
isolated_max_borrowable()
get_cross_max_transfer_out_amount()
get_isolated_max_transfer_out_amount()

isolated_place_order()
isolated_batch_order()
isolated_cancel_order()
isolated_batch_cancel_orders()
isolated_open_orders()
get_isolated_order_history()
get_isolated_transaction_details()
get_isolated_loan_records()
get_isolated_repay_history()
get_isolated_interest_records()
get_isolated_liquidation_records()
get_isolated_finance_history()

cross_place_order()
cross_batch_order()
cross_cancel_order()
cross_batch_cancel_order()
get_cross_open_orders()
get_cross_order_history()
get_cross_order_fills()
get_cross_loan_records()
get_cross_repay_history()
get_cross_interest_rate_records()
get_cross_liquidation_records()
get_cross_finance_flow_history()

# P2P
p2p_merchant_list()
get_merchant_information()
get_advertisement_list()
merchant_get_p2p_order_list()

# Sub-Account
create_virtual_sub_account()
modify_virtual_account()
batch_create_virtual_account_and_apikey()
get_virtual_account_list()
create_virtual_account_apikey()
modify_virtual_account_apikey()
get_virtual_sub_apikey_list()

# Convert
get_convert_coins()
get_quoted_price()
convert()
convert_history()

# Tax
spot_account_record()
future_account_record()
margin_account_record()
p2p_account_record()

# Common
get_all_notices()

Custom Methods:
(requires authentication)
------------------------
batch_modify_order()

"""

# Import pyget and asyncio, define a coroutine and HTTP object.
import asyncio
from pyget import Exchange

"""
You can create an authenticated or unauthenticated REST HTTP session.
You can skip authentication by not passing any value for api_key
and api_secret.

Exchange class supports both context manager protocol (self closing)
and direct instantiation (manual close required).
"""

# Context manager protocol example

# Lets get market information about BTCUSDT, using context manager
# protocol. Note that `symbol` is a required parameter as per the
# Bitget API documentation. This is a public endpoint so api_key,
# api_secret and passphrase can optionally be omitted.

async def main():
    async with Exchange() as session:
        rest = session.rest(
            endpoint='https://api.bitget.com',
            api_key=...,
            api_secret=...,
            passphrase=...,
            contract_type='futures',
            force_retry=True
        )
        print(await rest.do('get_single_symbol_ticker', symbol='BTCUSDT_UMCBL'))

asyncio.run(main())

# Direct instantiation example

# Lets get our SOL account information using direct instantiation with
# manual session closure. Note that `symbol` and `marginCoin` are required
# parameters as per the Bitget API documentation. This is a private
# endpoint so api_key,api_secret and passphrase are required.

async def main():
    try:
        session = Exchange()
        rest = session.rest(
            endpoint='https://api.bitget.com',
            api_key=...,
            api_secret=...,
            passphrase=...,
            contract_type='futures',
        )
        print(await rest.do('get_single_account', symbol='SOLUSDT_UMCBL', marginCoin='USDT'))
    finally:
        await session.exit()

asyncio.run(main())
