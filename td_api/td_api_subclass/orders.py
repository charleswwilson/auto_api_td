import httpx


class TdOrders:
    def __init__(self, parent):
        self._parent = parent

    def _get_order_id_from_http_response(self, http_response):
        if (http_response.status_code == httpx.codes.CREATED and http_response.is_error == False):
            return http_response.headers["location"].split("/orders/")[1]
        else:
            return http_response.text

    def get_orders_by_path(self, max_results=None, from_entered_datetime=None, to_entered_datetime=None, status=None, statuses=None):
        self._parent.login
        endpoint = f"{self._parent._main_url}accounts/{self._parent.config_token.account_number}/orders"
        params = {
            "maxResults": max_results,
            "fromEnteredTime": from_entered_datetime,
            "toEnteredTime": to_entered_datetime,
            "status": status,
        }
        content = httpx.get(
            url=endpoint, params=params, headers=self._parent.headers
        )
        decoded_content = content.json()
        return decoded_content

    def get_order(self, order_id):
        self._parent.login
        endpoint = f"{self._parent._main_url}accounts/{self._parent.config_token.account_id[0]}/orders/{order_id}"
        content = httpx.get(url=endpoint, headers=self._parent.headers)
        decoded_content = content.json()
        return decoded_content

    def cancel_order(self, order_id):
        self._parent.login
        endpoint = f"{self._parent._main_url}accounts/{self._parent.config_token.account_number}/orders/{order_id}"
        content = httpx.delete(url=endpoint, headers=self._parent.headers)
        if content.status_code == 200:
            print(f"order {order_id} cancelled")
            return (content, 200)
        else:
            print("an error has occured")
            return (content, content.status_code)

    def buy_market(self, symbol, quantity, session="NORMAL", duration="DAY"):
        self._parent.login
        endpoint = f"{self._parent._main_url}accounts/{self._parent.config_token.account_number}/orders"
        payload = {
            "orderType": "MARKET",
            "session": session,
            "duration": duration,
            "orderStrategyType": "SINGLE",
            "orderLegCollection": [
                {
                    "instruction": "BUY",
                    "quantity": int(quantity),
                    "instrument": {
                        "symbol": str(symbol).upper(),
                        "assetType": "EQUITY",
                    },
                }
            ],
        }
        content = httpx.post(
            url=endpoint, json=payload, headers=self._parent.headers
        )
        print(content.status_code, content.text)
        return self._get_order_id_from_http_response(content)

    def buy_limit(self, symbol, quantity, price, session="NORMAL", duration="DAY"):
        self._parent.login
        endpoint = f"{self._parent._main_url}accounts/{self._parent.config_token.account_number}/orders"
        payload = {
            "orderType": "LIMIT",
            "session": session,
            "duration": duration,
            "price": float(price),
            "orderStrategyType": "SINGLE",
            "orderLegCollection": [
                {
                    "instruction": "BUY",
                    "quantity": int(quantity),
                    "instrument": {
                        "symbol": str(symbol).upper(),
                        "assetType": "EQUITY",
                    },
                }
            ],
        }
        content = httpx.post(
            url=endpoint, json=payload, headers=self._parent.headers
        )
        print(content.status_code, content.text)
        return self._get_order_id_from_http_response(content)

    def sell_market(self, symbol, quantity, session="NORMAL", duration="DAY"):
        self._parent.login
        endpoint = f"{self._parent._main_url}accounts/{self._parent.config_token.account_id[0]}/orders"
        payload = {
            "orderType": "MARKET",
            "session": session,
            "duration": duration,
            "orderStrategyType": "SINGLE",
            "orderLegCollection": [
                {
                    "instruction": "SELL",
                    "quantity": int(quantity),
                    "instrument": {
                        "symbol": str(symbol).upper(),
                        "assetType": "EQUITY",
                    },
                }
            ],
        }
        content = httpx.post(
            url=endpoint, json=payload, headers=self._parent.headers
        )
        print(content.status_code, content.text)
        return self._get_order_id_from_http_response(content)

    def sell_limit(self, symbol, quantity, price, session="NORMAL", duration="DAY"):
        self._parent.login
        endpoint = f"{self._parent._main_url}accounts/{self._parent.config_token.account_id[0]}/orders"
        payload = {
            "orderType": "LIMIT",
            "session": session,
            "duration": duration,
            "price": float(price),
            "orderStrategyType": "SINGLE",
            "orderLegCollection": [
                {
                    "instruction": "SELL",
                    "quantity": int(quantity),
                    "instrument": {
                        "symbol": str(symbol).upper(),
                        "assetType": "EQUITY",
                    },
                }
            ],
        }
        content = httpx.post(
            url=endpoint, json=payload, headers=self._parent.headers
        )
        print(content.status_code, content.text)
        return self._get_order_id_from_http_response(content)
