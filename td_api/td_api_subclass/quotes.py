import httpx

class TdQuotes:
	def __init__(self, parent):
		self._parent = parent

	def get_quote(self, symbol):
		self._parent.login
		endpoint = f"{self._parent._main_url}marketdata/{symbol.upper()}/quotes"
		content = httpx.get(url=endpoint, headers=self._parent.headers)
		decoded_content = content.json()
		return decoded_content

	def get_quotes(self, symbols):
		self._parent.login
		endpoint = f"{self._parent._main_url}marketdata/quotes"
		params = {"symbol": list(map(str.upper, symbols))}
		content = httpx.get(url=endpoint, params=params, headers=self._parent.headers)
		decoded_content = content.json()
		return decoded_content