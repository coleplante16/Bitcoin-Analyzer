from termcolor import colored
import requests
from bs4 import BeautifulSoup
import re
import pandas
import pyyed
import numpy




def account():


    address = input(colored('\nWhat is the address you would like to analyze? \n', 'blue'))
    if len(address) < 26:
        print('\n Sorry, that wasn\'t quite long enough.')
    else:
        pass
    # if len(address) > 34:
    #    print('\n Sorry, that was too many characters')
    # else:
    #    pass
    if address[0] == 1 or 3:
        pass
    else:
        print('/n Sorry, Bitcoin addresses start with either a 1 or a 3.')
    # for i in address:
    #    if i in ['O', 'I', 'l']:
    #        print('Sorry, Bitcoin addresses cannot contain the letters O, I, or l')
    #    else:
    #        pass
    print(colored('\nFetching your results. Please wait...\n', 'yellow'))

    # Search for transactions

    # Grab Account Information
    URL = 'https://www.blockchain.com/btc/address/' + address
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')
    acctInfo = str(soup.find('span', attrs={'class': 'sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP u3ufsr-0 eQTRKC'}))

    # Clean Up Account Information
    acctInfo = re.sub('<.+?>', '', acctInfo)
    acct = [float(acct) for acct in str.split(acctInfo) if acct.isdigit()]
    print(acctInfo)
    print('\n')

    # Grab Most Recent Transaction
    lastTrans = str(soup.find('div', attrs={'class': 'sc-19pxzmk-0 dVzTcW'}))

    # Clean up Most Recent Transaction
    lastTrans = re.sub('<.+?>', ' ', lastTrans)
    lastTrans = ' '.join(lastTrans.split())
    lastTrans = list(lastTrans.split(' '))

    # Present Most Recent Transaction as a Table
    column_names = ['To', 'Amount', 'Currency']
    lastTrans = pandas.DataFrame(lastTrans, column_names)
    print('The most recent transaction was to:\n(if', address, 'sent currency, \"Amount\" shows as negative)\n', lastTrans)

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
            account()
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
                account.address + '.csv')
            print(colored(
                '\nBe Sure to note the poster\'s account or username, \nthey may be the one who owns the bitcoin account',
                'red'))
        else:
            quit()


    elif choice == '2':
        end = input(
            colored('\nPlease type in the maximum number of transactions you would like (multiples of 5).\n', 'blue'))
        end = (int(end) / 5)

        print(colored('\nFetching your results. Please wait...', 'yellow'))
        pages = numpy.arange(1, end, 1)
        transactions3 = []
        transactions = []

        for page in pages:
            URL1 = 'https://www.blockchain.com/btc/address/' + address + '?page=' + str(page)
            r1 = requests.get(URL1)
            soup1 = BeautifulSoup(r1.content, 'html5lib')
            transactions1 = str(soup1.findAll('div', attrs={'class': 'sc-1fp9csv-0 koYsLf'}))

            transactions2 = (transactions1.split('<div class ="sc-1fp9csv-0 koYsLf"'))
            transactions3.append(transactions2)
            print('\n', round(5 * page, 1), 'transactions gathered')

        from Wrangled import Wrangled
        Wrangled(transactions3, transactions, address)

    elif choice == '3':
        account()

    elif choice == '4':
        from main import main
        main()

    elif choice == '5':
        quit()

    else:
     print('\n \nSorry, that wasn\'t a choice. Please try again')



account()