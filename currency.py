from datetime import datetime
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()


def time_is_come(last_cur_update):
    day, time = str(datetime.now()).split(" ")
    hour, minute, sec = time.split(":")

    last_cur_updt_day, last_cur_updt_time = last_cur_update.split(" ")
    last_cur_updt_hour, last_cur_updt_minute, last_cur_updt_sec = last_cur_updt_time.split(":")

    return day >= last_cur_updt_day and int(minute) - int(last_cur_updt_minute) >= 5 and round(float(sec)) >= round(float(last_cur_updt_sec))


class CurrencyBot:
    URLS = {'btc': 'https://exmo.me/ru/trade/BTC_RUB',
            'ltc': 'https://exmo.me/ru/trade/LTC_RUB',
            'bch': 'https://exmo.me/ru/trade/BCH_RUB',
            'eth': 'https://exmo.me/ru/trade/ETH_RUB',
            }

    CURR_MSGS = {'BitCoin': 'BitCoin (BTC)',
                    'LitCoin': 'LitCoin (LTC)',
                    'EXMOCoin': 'EXMO (₽)',
                    'Etherium': 'Etherium (ETH)',
                    'BitCoinCash': 'BitCoinCash (BCH)', }

    def __init__(self):
        self.btc_currency = 0
        self.ltc_currency = 0
        self.bch_currency = 0
        self.eth_currency = 0
        self.exmo_currency = 1
        self.last_cur_update = None
        self.last_cur_update = self.update_all_currencies()

    def update_all_currencies(self):

        if self.last_cur_update is None or time_is_come(str(self.last_cur_update)):
            self.btc_currency = cg.get_price('bitcoin', 'rub')['bitcoin']['rub']
            self.ltc_currency = cg.get_price('litecoin', 'rub')['litecoin']['rub']
            self.bch_currency = cg.get_price('bitcoin-cash', 'rub')['bitcoin-cash']['rub']
            self.eth_currency = cg.get_price('ethereum', 'rub')['ethereum']['rub']

            return datetime.now()

    def get_btc(self):
        return self.btc_currency

    def get_ltc(self):
        return self.ltc_currency

    def get_bch(self):
        return self.bch_currency

    def get_eth(self):
        return self.eth_currency

    def get_curr_by_key(self, key):

        price = 'NaN'
        if key == 'Bitcoin':
            price = self.btc_currency
        if key == 'LiteCoin':
            price = self.ltc_currency
        if key == 'Bitcoin Cash':
            price = self.bch_currency
        if key == 'Ethereum':
            price = self.eth_currency
        if key == 'ExmoRUB':
            price = self.exmo_currency

        return price

    def print(self):
        print(self.btc_currency)
        print(self.ltc_currency)
        print(self.bch_currency)
        print(self.eth_currency)


if __name__ == "__main__":
    curr = CurrencyBot()
    curr.print()











