from termcolor import colored
import requests
from bs4 import BeautifulSoup
import re
import pandas
import pyyed
import numpy
#import hibpwned


def acctEmail():

    # Search for Email mentions
    email = input(colored('\nPlease enter the email address you believe is linked to a bitcoin address:\n', 'blue'))
    URL = 'https://www.google.com/search?q=' + email + 'Bitcoin'
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')
    acctInfo = str(soup.find_all('div', attrs={'class': 'kCrYT'}))
    potentialAcct = (re.findall(r'(https?://\S+)', acctInfo)) + (re.findall(r'(https?://\S+)', acctInfo))

    # Remove Extraneous Characters
    potentialAcctstr = ''
    for i in potentialAcct:
        potentialAcctstr += i
    potentialAcctstr = potentialAcctstr.replace("><h3", ' ')
    potentialAcctstr = potentialAcctstr.replace("'", '')
    potentialAcctstr = potentialAcctstr.replace('"', '')
    potentialAcctstr = potentialAcctstr.replace('<>span', ' ')


    # Make List and Display Search Results
    potentialAcct = list(potentialAcctstr.split(' '))
    #print('\nResults: \n \n', potentialAcct)


    leakedList =[]
#    leakedAcct = hibpwned.Pwned(email, 'bitcoinSearcher', '77d8edaa3f4547b8bd90a6ad85ae8ded')
#    leaked = leakedAcct.searchAllBreaches()
#    for i in leaked:
#        leakedList.append((i.get('Domain')))


    print('\nResults:\n \n', potentialAcct)
    print('\n This email was also found on data leaks associated with the following websites:', leakedList)

    export = input(colored('\nWould you like this exported as a csv file? (Y/N):\n', 'blue'))

    if export.upper == "Y" or export.upper == "YES":
        print(export.upper())
        dict = {'Bitcoin address found on the following sites:': potentialAcct}
        df = pandas.DataFrame(dict)
        df.to_csv(email + '.csv')

        print(
            '\nYour potential links can be found in the same folder in which you saved this program.\n \nThe file is named:\n' +
            email + '.csv')
        print(colored(
            '\nNOTICE:\nBe Sure to note the poster\'s account or username, \nthey may be the one who owns the bitcoin account.',
            'red'))

    else:
        pass

    # Search Through Links for BTC Account
    search = input(colored('\nWould you like to scan these pages for potential Bitcoin accounts? (Y/N):\n', 'blue'))
    potentialBTC = []
    potentialBTCList = []
    if search.upper() == "Y" or search.upper() == "YES":
        print(colored('\nFetching your results...', 'yellow'))
        for i in potentialAcct:
            try:
                URL = i
                r = requests.get(URL)
                soup = BeautifulSoup(r.content, 'html5lib')
                # print(soup.prettify())
                variable = soup.get_text()

                for i in variable:
                    if ((i[0] == '1') or (i[0] == '3')) and len(i) < 34 and len(i) > 26:
                        if ('O' in i) or ('I' in i) or ('l' in i):
                            pass
                        else:
                            potentialBTC.append(i)

            except:
                continue
        if not potentialBTCList:
            print('\nSorry, nothing matched the required parameters of a bitcoin address on these pages.')
        else:
            print('\n', potentialBTCList)

    else:
        quit()

    print((colored('\nWhat would you like to do next?\n', 'blue')))
    print(colored('1. Transaction lookup', 'blue'))
    print(colored('2. Main Menu', 'blue'))
    print(colored('3. Quit', 'blue'))
    next = input(colored('Please select an option.'))
    if next == '1':
        from account import account
        account()
    elif next == '2':
        from main import main
        main()
    elif next == '3':
        quit()
    else:
        print('Sorry, that wasn\'t a valid option, please try again')
        acctEmail()