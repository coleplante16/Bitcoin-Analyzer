# price conversions using CoinGecko api
import requests


# check if given id is accepted by api
def acceptedcoin(coinid):
    URL = 'https://api.coingecko.com/api/v3/coins/list'
    r = requests.get(URL).json()
    check = False
    for i in r:
        if i.get('id') == coinid:
            check = True
    return check


def symboltoid(coin):
    URL = 'https://api.coingecko.com/api/v3/coins/list'
    r = requests.get(URL).json()
    for i in r:
        if i.get('id') == coin:
            return coin
    for i in r:
        if i.get('symbol') == coin:
            return i.get('id')
    return coin


# check if given currency is accepted by api
def acceptedcurrency(currency):
    URL = 'https://api.coingecko.com/api/v3/simple/supported_vs_currencies'
    currencylist = requests.get(URL).json()
    check = False
    for i in currencylist:
        if i == currency:
            check = True

    return check


# price conversion
# accepts
#   amount of cryptocurrency
#   id of cryptocurrency
#   currency to convert to
# returns
#   up-to-date value of given cryptocurrency in given currency
def price(coin, currency):
    coin = symboltoid(coin)
    if currency == 'usd':
        pass
    elif not acceptedcurrency(currency):
        print('ERROR: Not an accepted currency')
        return -1

    URL = ("https://api.coingecko.com/api/v3/simple/price?ids=" + coin + "&vs_currencies=" + currency)
    base = requests.get(URL).json()
    index = base.get(coin)
    conversion = index.get(currency)
    return conversion


# Convert amount of bitcoin to USD
def btctousd(amount):
    coin = "bitcoin"
    currency = "usd"
    return price(amount, coin, currency)


# test function
def test():
    value = .314
    coin = "bitcoin"
    currency = "usd"

    print('\nCoin')
    accepted = acceptedcoin(coin)
    print(accepted)

    print('\nCurrency')
    accepted = acceptedcurrency(currency)
    print(accepted)

    print('\nConversion')
    converted = price(value, coin, currency)
    print(value, " ", coin, " = ", converted, " ", currency)

