import json
import requests
from config import keys


class APIException(Exception):
    pass


class MoneyConverter:
    @staticmethod
    def get_price(quote, base, amount):
        if quote == base:
            raise APIException(f"Невозможно конвертировать одиннаковые валюты {quote}.")

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту {quote}.")

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту {base}.")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Не удалось обработать {amount}.")

        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}")

        price = round(json.loads(r.content)[base_ticker] * float(amount), 2)

        return price
