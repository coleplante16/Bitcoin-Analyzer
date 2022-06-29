from termcolor import colored
import requests
from bs4 import BeautifulSoup
import re
import pandas
import pyyed
import numpy


# Prompt user for what they would like to do next
def accountmenu(address, coin):

    print(colored('\nWhat would you like to do next?', 'green'))
    print('1. Search for this account online')
    print('2. Gather this account\'s transactions')
    print('3. Find a different account')
    print('4. Main Menu')
    print('5. Quit')
    choice = input(colored('\nPlease enter your choice (1-5):\n', 'blue'))

    if choice == '1':
        print(address)
        URL = 'https://www.allprivatekeys.com/btc/' + address
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, 'html5lib')
        acctInfo = str(soup.find_all('div', attrs={'class': 'media text-muted pt-3'}))
        potentialLink = (re.findall(r'(https?://\S+)', acctInfo)) + (re.findall(r'(https?://\S+)', acctInfo))
        if not potentialLink:
            print('Sorry, we couldn\'t find the account mentioned anywhere...')
            # quit()
            choosecurrency()
        potentialLinkstr = ''
        for i in potentialLink:
            potentialLinkstr += i
        potentialLinkstr = potentialLinkstr.replace("</a><br/>", ' ')
        potentialLinkstr = potentialLinkstr.replace('"', ' ')

        # Make List and Display Search Results
        potentialLink = list(potentialLinkstr.split(' '))
        print('\nResults:\n \n', potentialLink)

        # Export as CSV
        export = input(colored('\nWould you like this exported as a csv file? (Y/N):\n', 'blue'))
        if export.upper() == "Y" or export.upper == "YES":
            dict = {'Bitcoin address found on the following sites:': potentialLink}
            df = pandas.DataFrame(dict)
            df.to_csv(address + '.csv')
            print(
                '\nYour potential links can be found in the same folder in which you saved this program.\n \nThe file is named:\n',
                address + '.csv')
            print(colored(
                '\nBe Sure to note the poster\'s account or username, \nthey may be the one who owns the bitcoin account',
                'red'))

        accountmenu(address, coin)

    elif choice == '2':

        end = input(
             colored('\nPlease type in the maximum number of transactions you would like to load.\n', 'blue'))

        print(colored('\nFetching your results. Please wait...', 'yellow'))
        currencyTX(address, end, coin)

        accountmenu(address, coin)

        # from Wrangled import Wrangled
        # Wrangled(transactions3, transactions, address)

    elif choice == '3':
        choosecurrency()

    elif choice == '4':
        from main import main
        main()

    elif choice == '5':
        quit()

    else:
        print('\n \nSorry, that wasn\'t a choice. Please try again')
        accountmenu(address, coin)

def choosecurrency():
    crypto = input(colored(
        '\nPlease type in the type of cryptocurrency you would like to investigate. (Bitcoin/BTC or Ethereum/ETH)\n',
        'blue'))

    coin = crypto.upper()
    match coin:
        case 'BTC':
            from addressdata import BTCaccount
            addr = BTCaccount()
        case 'XBT':
            from addressdata import BTCaccount
            addr = BTCaccount()
            coin = 'BTC'
        case 'BITCOIN':
            from addressdata import BTCaccount
            addr = BTCaccount()
            coin = 'BTC'
        case 'ETHEREUM':
            from Etherscan import ETHaccount
            addr = ETHaccount()
            coin = 'ETH'
        case 'ETH':
            from Etherscan import ETHaccount
            addr = ETHaccount()
        case 'LITECOIN':
            print('Not implemented yet')
            choosecurrency()
        case 'LTC':
            print('Not implemented yet')
            choosecurrency()
        case 'NEO':
            print('Not implemented yet')
            choosecurrency()
        case 'DASH':
            print('Not implemented yet')
            choosecurrency()
        case 'RIPPLE':
            print('Not implemented yet')
            choosecurrency()
        case 'IOTA':
            print('Not implemented yet')
            choosecurrency()
        case 'MIOTA':
            print('Not implemented yet')
            choosecurrency()
        case 'MONERO':
            print('Not implemented yet')
            choosecurrency()
        case 'XMR':
            print('Not implemented yet')
            choosecurrency()
        case 'PETRO':
            print('Not implemented yet')
            choosecurrency()
        case 'PTR':
            print('Not implemented yet')
            choosecurrency()
        case _:
            print('Sorry, that was an invalid option')
            choosecurrency()

    accountmenu(addr, coin)


def currencyTX(addr, maximum, coin):
    match coin.upper():
        case 'BTC':
            from addressdata import gettransactions
            from addressdata import accounttransactions
            r = gettransactions(addr, maximum)
            accounttransactions(r, maximum, addr)
        case 'ETH':
            from Etherscan import gettransactions
            gettransactions(addr, maximum)
        case _:
            print('Error')

    print(coin)

    return
