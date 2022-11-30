from config import keys, headers
import requests
import json

class APIException(Exception):
    pass

class Convertor:
    @staticmethod
    def get_price(quote, base, amount):
        if quote not in keys.keys() or base not in keys.keys():
            raise APIException('нет такой валюты в списке')
        if quote == base:
            raise APIException('Нет смысла перевести одни и те же валюты')
        try:
            amount = float(amount)
        except:
            raise APIException(f'Не удалость обработать количество {amount}')
        req = requests.get(
            f'https://api.apilayer.com/exchangerates_data/convert?to={keys[quote]}&from={keys[base]}&amount={amount}',
            headers=headers)
        result = json.loads(req.content)
        return f"Цена {amount} {keys[base]} - {round(result['result'], 2)} {keys[quote]}"
