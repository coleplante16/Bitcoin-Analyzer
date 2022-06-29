from termcolor import colored
import blockcypher as bc
key = '398307359db341d5a7f9f31ce32030ef'


def overview(addr, coin, currency):
    r = bc.get_address_overview(addr, coin_symbol=coin.lower(), api_key=key)
    # record basic info on address
    received = (r.get('total_received')) / 100000000    # this conversion value will have to change based on currency
    sent = (r.get('total_sent')) / 100000000            # currently works for BTC, LTC, DASH
    balance = (r.get('final_balance')) / 100000000
    totaltransactions = r.get('n_tx')

    # check for sanctions
    from OfacXML import xmlsearch
    sanctioned = xmlsearch(addr)

    from FindPrice import price
    convert = price(coin.lower(), currency.lower())

    # print out info
    print('Address: ' + addr)
    print('Total Received: {:.8f} {} ${:,.2f} {}'.format(received, coin.upper(), received * convert, currency.upper()))
    print('Total Sent: {:.8f} {} ${:,.2f} {}'.format(sent, coin.upper(), sent * convert, currency.upper()))
    print('Current Balance: {:.8f} {} ${:,.2f} {}'.format(balance, coin.upper(), balance * convert, currency.upper()))
    print('Total Transactions: ', totaltransactions)

    # print that sanction was found
    if not sanctioned.empty:
        print('!This address was found on a list of OFAC sanctioned addresses!')
        printinfo = input(colored('\nPrint sanction info? (Y/N):\n', 'blue'))
        if printinfo.upper() == "Y" or printinfo.upper() == "YES":
            print(sanctioned)


# test overview function
def overviewtest():
    import time
    address = '1FfmbHfnpaZjKFvyi1okTjJJusN455paPH'
    coin = 'BTC'
    usd = 'USD'
    print('\n{}'.format(coin))
    overview(address, coin, usd)
    time.sleep(1)   # so coingecko api isn't overloaded
    address = '3CDJNfdWX8m2NwuGUV3nhXHXEeLygMXoAj'
    coin = 'LTC'
    print('\n{}'.format(coin))
    overview(address, coin, usd)
    time.sleep(1)
    address = 'XpESxaUmonkq8RaLLp46Brx2K39ggQe226'
    coin = 'DASH'
    print('\n{}'.format(coin))
    overview(address, coin, usd)


overviewtest()
