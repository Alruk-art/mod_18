import requests
import json
from config18 import carrency

class ConvertionException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException('Валюты одинаковые, курс 1:1')

        try:
            quote_ticker = carrency[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработвать валюту  {quote}')
        try:
            base_ticker = carrency[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработвать валюту  {base}')
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество  {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[carrency[base]]

        return total_base