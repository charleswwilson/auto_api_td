import httpx


class TdAccountInfo:
    def __init__(self, parent: object):
        self._parent = parent

    def get_account(self, account_id=None, param=None):
        """ Retrieves one account associated with login primary by default or 
            optionally a sub account by setting account_id.  Also output can be 
            modified with the param field 
            Usage::  
            class_instance.Accounts.get_account()
            class_instance.Accounts.get_account(account_id=123456789, param="all")
            """
        self._parent.login
        if account_id:
            assert isinstance(account_id, int)
        if param:
            assert param in {"orders", "positions", "all"}
        if account_id == None:
            account_id = self._parent.config_token.account_id[0]
        endpoint = f"{self._parent._main_url}accounts/{account_id}"
        if param == "orders":
            payload = {
                "fields": ['orders'],
            }
        elif param == "positions":
            payload = {
                "fields": ['positions'],
            }
        elif param == "all":
            payload = {
                "fields": ["orders,positions"],
            }
        else:
            payload = {}

        content = httpx.get(
            url=endpoint, headers=self._parent.headers, params=payload
        )
        decoded_content = content.json()
        return decoded_content

    def get_accounts(self):
        """
        Retrieves all accounts associated with login
        """
        self._parent.login
        endpoint = f"{self._parent._main_url}accounts"
        content = httpx.get(url=endpoint, headers=self._parent.headers)
        decoded_content = content.json()
        return decoded_content

    def get_account_preferences(self, account_id=None):
        """
        Retrieves account preferences with primary account.  Can retrieve a sub account
        by specifying account_id as an integer
        """
        self._parent.login
        if account_id == None:
            account_id = self._parent.config_token.account_id[0]
        endpoint = f"{self._parent._main_url}accounts/{account_id}"
        content = httpx.get(url=endpoint, headers=self._parent.headers)
        decoded_content = content.json()
        return decoded_content

    def get_user_principals(self):
        self._parent.login
        endpoint = f"{self._parent._main_url}userprincipals"
        # headers_dec = {'Authorization': "Bearer {}".format(self.access_token['access_token']),
        #                "Content-Type": "application/json"}
        payload = {'fields': 'streamerSubscriptionKeys,streamerConnectionInfo'}

        content = httpx.get(url=endpoint, params=payload,
                            headers=self._parent.headers)
        data = content.json()
        return data

    def get_streamer_subscription_keys(self, account_id=None):
        self._parent.login
        if account_id == None:
            account_id = self._parent.config_token.account_id[0]
        endpoint = f"{self._parent._main_url}userprincipals/streamersubscriptionkeys"
        # headers_dec = {'Authorization': "Bearer {}".format(self.access_token['access_token']),
        #                "Content-Type": "application/json"}
        payload = {'accountIds': f"{account_id}"}

        content = httpx.get(url=endpoint, params=payload,
                            headers=self._parent.headers)
        data = content.json()
        return data

    # not returning data return to later
    # def get_transaction(self, transaction_id=None, account_id = None):
    #     self._parent.login
    #     if not account_id:
    #         account_id = self._parent.config.account_id
    #     endpoint = f"{self._parent._main_url}accounts/{account_id}/transactions/{transaction_id}"
    #     content = httpx.get(url=endpoint, headers=self._parent.headers)
    #     decoded_content = content.json()
    #     return decoded_content

    def get_transactions(self, type=None, symbol=None, start_date=None, end_date=None, account_id=None):
        self._parent.login
        if not account_id:
            account_id = self._parent.config_token.account_id[0]
        endpoint = f"{self._parent._main_url}accounts/{account_id}/transactions"
        params = {
            "type": type,
            "symbol": symbol,
            "startDate": start_date,
            "endDate": end_date,
        }
        content = httpx.get(
            url=endpoint, params=params, headers=self._parent.headers
        )
        decoded_content = content.json()
        return decoded_content
