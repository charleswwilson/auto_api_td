from td_api.td_main import TdApi
p1 = TdApi()


# td_auth parent class

def test_attr_access_token():
    assert isinstance(p1.access_token, dict) == True


def test_o_auth():
    p1.o_auth()


def test_o_auth_refresh():
    p1.o_auth_refresh()


def test_td_login():
    p1.td_login()

# account subclass


def test_account():
    test_account = p1.Accounts.get_account()
    assert isinstance(p1.Accounts.get_account(), dict) == True


def test_accounts():
    assert isinstance(p1.Accounts.get_accounts(), list) == True


def test_get_account_preferences():
    assert isinstance(p1.Accounts.get_account_preferences(), dict) == True


def test_get_user_principals():
    assert isinstance(p1.Accounts.get_user_principals(), dict) == True


def test_get_streamer_subscription_keys():
    assert isinstance(
        p1.Accounts.get_streamer_subscription_keys(), dict) == True


def test_get_transactions():
    assert isinstance(p1.Accounts.get_transactions(), list) == True

# quote subclass


def test_Quotes_get_quote():
    test_quote = p1.Quotes.get_quote('am')
    assert isinstance(test_quote, dict) == True


def test_Quotes_get_quotes():
    test_quotes = p1.Quotes.get_quotes(['am', 'TSLA', 'IBm', 'TSLA'])
    assert isinstance(test_quotes, dict) == True

# orders subclass


def test_get_order_by_path():
    _ = p1.Orders.get_orders_by_path()
    assert isinstance(_, list) == True
    assert not _ == False


def test_buy_limit_and_cancel():
    test_order = p1.Orders.buy_limit('am', 1, 1.00)
    p1.Orders.cancel_order(test_order)


def test_but_market_and_cancel():
    test_order = p1.Orders.buy_market('am', 1)
    p1.Orders.cancel_order(test_order)
