# from config.td_config import TdConfig
from td_api.td_api_subclass.td_auth import TD_Authorization
from td_api.td_api_subclass.account_info import TdAccountInfo
from td_api.td_api_subclass.quotes import TdQuotes
from td_api.td_api_subclass.orders import TdOrders
import pickle


class TdApi(TD_Authorization):
    """ base class """
    _main_url = "https://api.tdameritrade.com/v1/"

    def __init__(self):
        super().__init__()
        # self._main_url = "https://api.tdameritrade.com/v1/"
        self.Accounts = TdAccountInfo(self)
        self.Quotes = TdQuotes(self)
        self.Orders = TdOrders(self)

    def __getattr__(self, attr):
        if attr == "access_token":
            return self._retrieve_access_token()
        elif attr == "login":
            return self._td_login()
        elif attr == "headers":
            return self._set_header()
        elif attr == "config_token":
            return self.config.load_config_from_pickle()
        elif attr == "config_token.account_id":
            return self._get_account_id()

    def _set_header(self):
        return {"Authorization": f"Bearer {self.access_token['access_token']}",
                "Content-Type": "application/json",
                }

    def _get_account_id(self):
        accounts = []
        _ = self.Accounts.get_accounts()
        for i in range(len(_)):
            accounts.append(_[i]['securitiesAccount']['accountId'])
        self._update_pickle({'account_id': accounts})
        return accounts

    def _update_pickle(self, dict_item):
        _ = pickle.load(open("config/config.pickle", "rb"))
        _.update(dict_item)
        pickle.dump(_, open(
            "config/config.pickle", "wb"
        ))
