from datetime import datetime


from pycoingecko import CoinGeckoAPI
from modules.functions import time_is_come


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
        import coinaddr
        self.cg = CoinGeckoAPI()
        self.btc_currency = 0
        self.ltc_currency = 0
        self.bch_currency = 0
        self.eth_currency = 0
        self.exmo_currency = 1
        self.last_cur_update = None
        self.last_cur_update = self.update_all_currencies()
        self.coinaddr = coinaddr

    def adress_is_valid(self, address):
        print(address, 'ADDRESS CHECKOUT ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        try:
            address = bytes(address, 'ascii')
            if self.coinaddr.validate('btc', address):
                return True
        except Exception:
            try:
                if self.coinaddr.validate('ltc', address):
                    return True
            except Exception:
                try:
                    if self.coinaddr.validate('bch', address):
                        return True
                except Exception:
                    try:
                        if self.coinaddr.validate('eth', address):
                            return True
                    except Exception:
                        return False

    def update_all_currencies(self):

        if self.last_cur_update is None or time_is_come(str(self.last_cur_update)):
            self.btc_currency = self.cg.get_price('bitcoin', 'rub')['bitcoin']['rub']
            self.ltc_currency = self.cg.get_price('litecoin', 'rub')['litecoin']['rub']
            self.bch_currency = self.cg.get_price('bitcoin-cash', 'rub')['bitcoin-cash']['rub']
            self.eth_currency = self.cg.get_price('ethereum', 'rub')['ethereum']['rub']

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











