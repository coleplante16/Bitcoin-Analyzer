from termcolor import colored
import requests
from bs4 import BeautifulSoup
import re
import pandas
import pyyed
import numpy


# prompt user for address
# print out basic address data
def account(coin):
    approved = False
    while not approved:
        address = input(colored('\nWhat is the address you would like to analyze? \n', 'blue'))
        match coin:
            case 'ETH':
                if len(address) != 42:
                    print('\n Sorry, ETH addresses must be 42 characters.')
                    approved = False
                elif address[0] != '0' and address[1] != 'x':
                    print('\n Sorry, ETH addresses start with 0x')
                    approved = False
                else:
                    approved = True

            case 'BTC':
                # get overview from blockchain.com
                from addressdata import BTCaccount
                return BTCaccount(address)

            case 'LTC':
                if len(address) == 26 or len(address) == 33 or len(address) == 34:
                    approved = True
                else:
                    print('\n Sorry, that wasn\'t a valid address.')
                    approved = False

                if address[0] == 'L' or address[0] == 'M' or address[0] == '3':
                    approved = True
                else:
                    print('\n Sorry, Litecoin addresses start with either an M, L, or 3.')
                    approved = False

            case 'DASH':
                if len(address) != 34:
                    print('\n Sorry, that wasn\'t a valid address.')
                    approved = False
                elif address[0] != 'X':
                    print('/n Sorry, DASH addresses start with an uppercase X.')
                    approved = False
                else:
                    approved = True

    print(colored('\nFetching your results. Please wait...\n', 'yellow'))
    # Eth, LTC, and DASH get overview from block cypher
    from BlockCypher import overview
    overview(address, coin, 'USD')
    return address


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
        # still collect data for eth and btc from respective apis
        # able to collect more transactions in less api calls
        if coin == 'ETH' or coin == 'BTC':
            currencyTX(address, end, coin)
        else:
            from BlockCypher import addrfull
            addrfull(address, coin, 'USD', end)
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


# prompt user for cryptocurrency they are investigating
def choosecurrency():
    crypto = input(colored(
        '\nPlease type in the type of cryptocurrency you would like to investigate. '
        '(Bitcoin/BTC, Ethereum/ETH, Litecoin/LTC, DASH)\n',
        'blue'))

    coin = crypto.upper()
    match coin:
        case 'BTC':
            coin = 'BTC'
        case 'XBT':
            coin = 'BTC'
        case 'BITCOIN':
            coin = 'BTC'
        case 'ETHEREUM':
            # from Etherscan import ETHaccount
            # addr = ETHaccount()
            coin = 'ETH'
        case 'ETH':
            # from Etherscan import ETHaccount
            # addr = ETHaccount()
            coin = 'ETH'
        case 'LITECOIN':
            coin = 'LTC'
        case 'LTC':
            coin = 'LTC'
        case 'NEO':
            print('Not implemented yet')
            choosecurrency()
        case 'DASH':
            coin = 'DASH'
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

    addr = account(coin)
    accountmenu(addr, coin)


# collect transactions from blockchain.com api or etherscan api
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
    return
