"""
pyget Endpoints
------------------------

Endpoints match Bitget API documentation anchor names.
Formatting is: {name: tuple(method, auth, endpoint), ...}.

Documentation can be found at
https://github.com/APF20/pyget

:copyright: (c) 2023 APF20

:license: MIT License

:updated: Jul 22, 2023
"""

class Endpoints:

    # Refer: https://bitgetlimited.github.io/apidoc/en/mix/#restapi
    futures = {
        # market - public
        'get_all_symbols':              ('GET',  False, '/api/mix/v1/market/contracts'),
        'get_depth':                    ('GET',  False, '/api/mix/v1/market/depth'),
        'get_single_symbol_ticker':     ('GET',  False, '/api/mix/v1/market/ticker'),
        'get_all_symbol_ticker':        ('GET',  False, '/api/mix/v1/market/tickers'),
        'vip_fee_rate':                 ('GET',  False, '/api/mix/v1/market/contract-vip-level'),
        'get_recent_fills':             ('GET',  False, '/api/mix/v1/market/fills'),
        'get_fills':                    ('GET',  False, '/api/mix/v1/market/fills-history'),
        'get_candle_data':              ('GET',  False, '/api/mix/v1/market/candles'),
        'get_history_candle_data':      ('GET',  False, '/api/mix/v1/market/history-candles'),
        'get_history_index_candle_data':    ('GET',  False, '/api/mix/v1/market/history-index-candles'),
        'get_history_mark_candle_data': ('GET',  False, '/api/mix/v1/market/history-mark-candles'),
        'get_symbol_index_price':       ('GET',  False, '/api/mix/v1/market/index'),
        'get_symbol_next_funding_time': ('GET',  False, '/api/mix/v1/market/funding-time'),
        'get_history_funding_rate':     ('GET',  False, '/api/mix/v1/market/history-fundRate'),
        'get_current_funding_rate':     ('GET',  False, '/api/mix/v1/market/current-fundRate'),
        'get_open_interest':            ('GET',  False, '/api/mix/v1/market/open-interest'),
        'get_symbol_mark_price':        ('GET',  False, '/api/mix/v1/market/mark-price'),
        'get_symbol_leverage':          ('GET',  False, '/api/mix/v1/market/symbol-leverage'),
        'get_position_tier':            ('GET',  False, '/api/mix/v1/market/queryPositionLever'),
        'get_risk_position_limit':      ('GET',  False, '/api/mix/v1/market/open-limit'),
        # account - private
        'get_single_account':           ('GET',  True, '/api/mix/v1/account/account'),
        'get_account_list':             ('GET',  True, '/api/mix/v1/account/accounts'),
        'get_sub_account_contract_assets':  ('POST', True, '/api/mix/v1/account/sub-account-contract-assets'),
        'get_open_count':               ('POST', True, '/api/mix/v1/account/open-count'),
        'change_leverage':              ('POST', True, '/api/mix/v1/account/setLeverage'),
        'change_margin':                ('POST', True, '/api/mix/v1/account/setMargin'),
        'change_margin_mode':           ('POST', True, '/api/mix/v1/account/setMarginMode'),
        'change_hold_mode':             ('POST', True, '/api/mix/v1/account/setPositionMode'),
        'get_symbol_position':          ('GET',  True, '/api/mix/v1/position/singlePosition'),
        'get_symbol_position_v2':       ('GET',  True, '/api/mix/v1/position/singlePosition-v2'),
        'get_all_position':             ('GET',  True, '/api/mix/v1/position/allPosition'),
        'get_all_position_v2':          ('GET',  True, '/api/mix/v1/position/allPosition-v2'),
        'get_account_bill':             ('GET',  True, '/api/mix/v1/account/accountBill'),
        'get_business_account_bill':    ('GET',  True, '/api/mix/v1/account/accountBusinessBill'),
        # trade - private
        'place_order':                  ('POST', True, '/api/mix/v1/order/placeOrder'),
        'reversal':                     ('POST', True, '/api/mix/v1/order/placeOrder'),
        'batch_order':                  ('POST', True, '/api/mix/v1/order/batch-orders'),
        'cancel_order':                 ('POST', True, '/api/mix/v1/order/cancel-order'),
        'batch_cancel_order':           ('POST', True, '/api/mix/v1/order/cancel-batch-orders'),
        'modify_order':                 ('POST', True, '/api/mix/v1/order/modifyOrder'),
        'cancel_order_by_symbol':       ('POST', True, '/api/mix/v1/order/cancel-symbol-orders'),
        'cancel_all_order':             ('POST', True, '/api/mix/v1/order/cancel-all-orders'),
        'close_all_position':           ('POST', True, '/api/mix/v1/order/close-all-positions'),
        'get_open_order':               ('GET',  True, '/api/mix/v1/order/current'),
        'get_all_open_order':           ('GET',  True, '/api/mix/v1/order/marginCoinCurrent'),
        'get_history_order':            ('GET',  True, '/api/mix/v1/order/history'),
        'get_producttype_history_orders':   ('GET',  True, '/api/mix/v1/order/historyProductType'),
        'get_order_details':            ('GET',  True, '/api/mix/v1/order/detail'),
        'get_order_fill_detail':        ('GET',  True, '/api/mix/v1/order/fills'),
        'get_producttype_order_fill_detail':('GET',  True, '/api/mix/v1/order/allFills'),
        'place_plan_order':             ('POST', True, '/api/mix/v1/plan/placePlan'),
        'modify_plan_order':            ('POST', True, '/api/mix/v1/plan/modifyPlan'),
        'modify_plan_order_tpsl':       ('POST', True, '/api/mix/v1/plan/modifyPlanPreset'),
        'place_stop_order':             ('POST', True, '/api/mix/v1/plan/placeTPSL'),
        'place_trailing_stop_order':    ('POST', True, '/api/mix/v1/plan/placeTrailStop'),
        'place_position_tpsl':          ('POST', True, '/api/mix/v1/plan/placePositionsTPSL'),
        'modify_stop_order':            ('POST', True, '/api/mix/v1/plan/modifyTPSLPlan'),
        'cancel_plan_order_tpsl':       ('POST', True, '/api/mix/v1/plan/cancelPlan'),
        'cancel_plan_order_tpsl_by_symbol': ('POST', True, '/api/mix/v1/plan/cancelSymbolPlan'),
        'cancel_all_trigger_order_tpsl':('POST', True, '/api/mix/v1/plan/cancelAllPlan'),
        'get_plan_order_tpsl_list':     ('GET',  True, '/api/mix/v1/plan/currentPlan'),
        'get_history_plan_orders_tpsl': ('GET',  True, '/api/mix/v1/plan/historyPlan')
    }

    # Refer: https://bitgetlimited.github.io/apidoc/en/spot/#restapi
    spot = {
        # public
        'get_coin_list':                ('GET',  False, '/api/spot/v1/public/currencies'),
        'get_symbols':                  ('GET',  False, '/api/spot/v1/public/products'),
        'get_single_symbol':            ('GET',  False, '/api/spot/v1/public/product'),
        # market - public
        'get_single_ticker':            ('GET',  False, '/api/spot/v1/market/ticker'),
        'get_all_tickers':              ('GET',  False, '/api/spot/v1/market/tickers'),
        'get_recent_trades':            ('GET',  False, '/api/spot/v1/market/fills'),
        'get_market_trades':            ('GET',  False, '/api/spot/v1/market/fills-history'),
        'get_candle_data':              ('GET',  False, '/api/spot/v1/market/candles'),
        'get_history_candle_data':      ('GET',  False, '/api/spot/v1/market/history-candles'),
        'get_depth':                    ('GET',  False, '/api/spot/v1/market/depth'),
        'vip_fee_rate':                 ('GET',  False, '/api/spot/v1/market/spot-vip-level'),
        # wallet - private
        'transfer':                     ('POST', True, '/api/spot/v1/wallet/transfer'),
        'transfer_v2':                  ('POST', True, '/api/spot/v1/wallet/transfer-v2'),
        'sub_transfer':                 ('POST', True, '/api/spot/v1/wallet/subTransfer'),
        'get_coin_address':             ('GET',  True, '/api/spot/v1/wallet/deposit-address'),
        'withdraw':                     ('POST', True, '/api/spot/v1/wallet/withdrawal'),
        'withdraw_v2':                  ('POST', True, '/api/spot/v1/wallet/withdrawal-v2'),
        'inner_withdraw':               ('POST', True, '/api/spot/v1/wallet/withdrawal-inner'),
        'inner_withdraw_v2':            ('POST', True, '/api/spot/v1/wallet/withdrawal-inner-v2'),
        'get_withdraw_list':            ('GET',  True, '/api/spot/v1/wallet/withdrawal-list'),
        'get_deposit_list':             ('GET',  True, '/api/spot/v1/wallet/deposit-list'),
        'get_user_fee_ratio':           ('GET',  True, '/api/user/v1/fee/query'),
        # account - private
        'get_apikey_info':              ('GET',  True, '/api/spot/v1/account/getInfo'),
        'get_account_assets':           ('GET',  True, '/api/spot/v1/account/assets'),
        'get_account_assets_lite':      ('GET',  True, '/api/spot/v1/account/assets-lite'),
        'get_sub_account_spot_assets':  ('POST', True, '/api/spot/v1/account/sub-account-spot-assets'),
        'get_bills':                    ('POST', True, '/api/spot/v1/account/bills'),
        'get_transfer_list':            ('GET',  True, '/api/spot/v1/account/transferRecords'),
        # trade - private
        'place_order':                  ('POST', True, '/api/spot/v1/trade/orders'),
        'batch_order':                  ('POST', True, '/api/spot/v1/trade/batch-orders'),
        'cancel_order':                 ('POST', True, '/api/spot/v1/trade/cancel-order'),
        'cancel_order_v2':              ('POST', True, '/api/spot/v1/trade/cancel-order-v2'),
        'cancel_order_by_symbol':       ('POST', True, '/api/spot/v1/trade/cancel-symbol-order'),
        'cancel_order_in_batch':        ('POST', True, '/api/spot/v1/trade/cancel-batch-orders'),
        'cancel_order_in_batch_v2':     ('POST', True, '/api/spot/v1/trade/cancel-batch-orders-v2'),
        'get_order_details':            ('POST', True, '/api/spot/v1/trade/orderInfo'),
        'get_order_list':               ('POST', True, '/api/spot/v1/trade/open-orders'),
        'get_order_history':            ('POST', True, '/api/spot/v1/trade/history'),
        'get_transaction_details':      ('POST', True, '/api/spot/v1/trade/fills'),
        'place_plan_order':             ('POST', True, '/api/spot/v1/plan/placePlan'),
        'modify_plan_order':            ('POST', True, '/api/spot/v1/plan/modifyPlan'),
        'cancel_plan_order':            ('POST', True, '/api/spot/v1/plan/cancelPlan'),
        'get_current_plan_orders':      ('POST', True, '/api/spot/v1/plan/currentPlan'),
        'get_historic_plan_orders':     ('POST', True, '/api/spot/v1/plan/historyPlan'),
        'batch_cancel_plan_orders':     ('POST', True, '/api/spot/v1/plan/batchCancelPlan')
    }

    # Refer: https://bitgetlimited.github.io/apidoc/en/margin/#restapi
    margin = {
        # public
        'get_cross_interest_rate_and_borrowable':   ('GET',  False, '/api/margin/v1/cross/public/interestRateAndLimit'),
        'get_isolated_interest_rate_and_borrowable':('GET',  False, '/api/margin/v1/isolated/public/interestRateAndLimit'),
        'get_cross_tier_data':          ('GET',  False, '/api/margin/v1/cross/public/tierData'),
        'get_isolated_tier_data':       ('GET',  False, '/api/margin/v1/isolated/public/tierData'),
        'get_support_currencies':       ('GET',  False, '/api/margin/v1/public/currencies'),
        # account - private
        'get_cross_assets':             ('GET',  True, '/api/margin/v1/cross/account/assets'),
        'get_isolated_assets':          ('GET',  True, '/api/margin/v1/isolated/account/assets'),
        'cross_borrow':                 ('POST', True, '/api/margin/v1/cross/account/borrow'),
        'isolated_borrow':              ('POST', True, '/api/margin/v1/isolated/account/borrow'),
        'cross_repay':                  ('POST', True, '/api/margin/v1/cross/account/repay'),
        'isolated_repay':               ('POST', True, '/api/margin/v1/isolated/account/repay'),
        'get_cross_risk_rate':          ('GET',  True, '/api/margin/v1/cross/account/riskRate'),
        'isolated_risk_rate':           ('POST', True, '/api/margin/v1/isolated/account/riskRate'),
        'cross_max_borrowable_amount':  ('POST', True, '/api/margin/v1/cross/account/maxBorrowableAmount'),
        'isolated_max_borrowable':      ('POST', True, '/api/margin/v1/isolated/account/maxBorrowableAmount'),
        'get_cross_max_transfer_out_amount':    ('GET',  True, '/api/margin/v1/cross/account/maxTransferOutAmount'),
        'get_isolated_max_transfer_out_amount': ('GET',  True, '/api/margin/v1/cross/account/maxTransferOutAmount'), #doctypo??  
        # isolated - private
        'isolated_place_order':         ('POST', True, '/api/margin/v1/isolated/order/placeOrder'),
        'isolated_batch_order':         ('POST', True, '/api/margin/v1/isolated/order/batchPlaceOrder'),
        'isolated_cancel_order':        ('POST', True, '/api/margin/v1/isolated/order/cancelOrder'),
        'isolated_batch_cancel_orders': ('POST', True, '/api/margin/v1/isolated/order/batchCancelOrder'),
        'isolated_open_orders':         ('GET',  True, '/api/margin/v1/isolated/order/openOrders'),
        'get_isolated_order_history':   ('GET',  True, '/api/margin/v1/isolated/order/history'),
        'get_isolated_transaction_details': ('GET',  True, '/api/margin/v1/isolated/order/fills'),
        'get_isolated_loan_records':    ('GET',  True, '/api/margin/v1/isolated/loan/list'),
        'get_isolated_repay_history':   ('GET',  True, '/api/margin/v1/isolated/repay/list'),
        'get_isolated_interest_records':('GET',  True, '/api/margin/v1/isolated/interest/list'),
        'get_isolated_liquidation_records': ('GET',  True, '/api/margin/v1/isolated/liquidation/list'),
        'get_isolated_finance_history': ('GET',  True, '/api/margin/v1/isolated/fin/list'),
        # cross - private
        'cross_place_order':            ('POST', True, '/api/margin/v1/cross/order/placeOrder'),
        'cross_batch_order':            ('POST', True, '/api/margin/v1/cross/order/batchPlaceOrder'),
        'cross_cancel_order':           ('POST', True, '/api/margin/v1/cross/order/cancelOrder'),
        'cross_batch_cancel_order':     ('POST', True, '/api/margin/v1/cross/order/batchCancelOrder'),
        'get_cross_open_orders':        ('GET',  True, '/api/margin/v1/cross/order/openOrders'),
        'get_cross_order_history':      ('GET',  True, '/api/margin/v1/cross/order/history'),
        'get_cross_order_fills':        ('GET',  True, '/api/margin/v1/cross/order/fills'),
        'get_cross_loan_records':       ('GET',  True, '/api/margin/v1/cross/loan/list'),
        'get_cross_repay_history':      ('GET',  True, '/api/margin/v1/cross/repay/list'),
        'get_cross_interest_rate_records':  ('GET',  True, '/api/margin/v1/cross/interest/list'),
        'get_cross_liquidation_records':('GET',  True, '/api/margin/v1/cross/liquidation/list'),
        'get_cross_finance_flow_history':   ('GET',  True, '/api/margin/v1/cross/fin/list')
    }

    # Refer: https://bitgetlimited.github.io/apidoc/en/spot/#p2p-endpoint
    p2p = {
        # p2p - private
        'p2p_merchant_list':            ('GET',  True, '/api/p2p/v1/merchant/merchantList'),
        'get_merchant_information':     ('GET',  True, '/api/p2p/v1/merchant/merchantInfo'),
        'get_advertisement_list':       ('GET',  True, '/api/p2p/v1/merchant/advList'),
        'merchant_get_p2p_order_list':  ('GET',  True, '/api/p2p/v1/merchant/orderList')
    }

    # Refer: https://bitgetlimited.github.io/apidoc/en/spot/#sub-account-endpoints
    sub_account = {
        # sub-account - private
        'create_virtual_sub_account':   ('POST', True, '/api/user/v1/sub/virtual-create'),
        'modify_virtual_account':       ('POST', True, '/api/user/v1/sub/virtual-modify'),
        'batch_create_virtual_account_and_apikey':  ('POST', True, '/api/user/v1/sub/virtual-api-batch-create'),
        'get_virtual_account_list':     ('GET',  True, '/api/user/v1/sub/virtual-list'),
        'create_virtual_account_apikey':('POST', True, '/api/user/v1/sub/virtual-api-create'),
        'modify_virtual_account_apikey':('POST', True, '/api/user/v1/sub/virtual-api-modify'),
        'get_virtual_sub_apikey_list':  ('GET',  True, '/api/user/v1/sub/virtual-api-list')
    }

    # Refer: https://bitgetlimited.github.io/apidoc/en/spot/#convert
    convert = {
        # convert - private
        'get_convert_coins':            ('GET',  True, '/api/spot/v1/convert/currencies'),
        'get_quoted_price':             ('POST',  True, '/api/spot/v1/convert/quoted-price'),
        'convert':                      ('POST',  True, '/api/spot/v1/convert/trade'),
        'convert_history':              ('GET',  True, '/api/spot/v1/convert/convert-record')
    }

    # Refer: https://bitgetlimited.github.io/apidoc/en/spot/#tax
    tax = {
        # tax - private
        'spot_account_record':          ('GET',  True, '/api/user/v1/tax/spot-record'),
        'future_account_record':        ('GET',  True, '/api/user/v1/tax/future-record'),
        'margin_account_record':        ('GET',  True, '/api/user/v1/tax/margin-record'),
        'p2p_account_record':           ('GET',  True, '/api/user/v1/tax/p2p-record')
    }

    # common endpoints accessible from all endpoint types
    common = {
        # notice - private
        'get_all_notices':              ('GET',  True, '/api/spot/v1/notice/queryAllNotices'),
        # public
        'get_server_time':              ('GET',  False, '/api/spot/v1/public/time')
    }
