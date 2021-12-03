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
        content = httpx.get(url=endpoint, params=params,
                            headers=self._parent.headers)
        decoded_content = content.json()
        return decoded_content

    def get_price_history(self, symbol, period_type="day", period=10, frequency_type="minute", frequency=1, end_date="", start_date="", need_extended_hours_data="true"):
        period_type_list = ["day", "month", "year", "ytd"]
        frequency_list = [1]
        if period_type.lower() not in period_type_list:
            print(
                f"Please enter one of the following values for period_type {period_type_list}")
            return
        if period_type.lower() == "day":
            period_list = [1, 2, 3, 4, 5, 10]
            frequency_type_list = ['minute']
            frequency_list = [1, 5, 10, 15, 30]
        elif period_type.lower() == "month":
            period_list = [1, 2, 3, 6]
            frequency_type_list = ['daily', 'weekly']
        elif period_type.lower() == "year":
            period_list = [1, 2, 3, 5, 10, 15, 20]
            frequency_type_list = ['daily', 'weekly', 'monthly']
        elif period_type.lower() == "ytd":
            period_list = [1]
            frequency_type_list = ['daily', 'weekly']
        else:
            print("Something went wrong with the period type")
            return
        if period not in period_list:
            print(
                f"Please enter one of the following values for period {period_list}")
            return
        if frequency_type not in frequency_type_list:
            print(f"Please enter one of the following values for frequency_type {frequency_type_list}"
                  )
            return
        if frequency not in frequency_list:
            print(
                f"Please enter one of the following values for frequency {frequency_list}")
        self._parent.login
        endpoint = f"{self._parent._main_url}marketdata/{symbol.upper()}/pricehistory"

        params = {
            "periodType": period_type,
            "period": period,
            "frequencyType": frequency_type,
            "frequency": frequency,
            "endDate": end_date,
            "startDate": start_date,
            "needExtendedHoursData": need_extended_hours_data
        }

        if params["endDate"] or params["startDate"] != "":
            params.pop("period", None)
        else:
            params.pop("endDate", None)
            params.pop("startDate", None)

        content = httpx.get(
            url=endpoint, params=params, headers=self._parent.headers
        )
        decoded_content = content.json()
        return decoded_content
