from requests import get
from datetime import datetime
import pandas as pd
from termcolor import colored

apikey = '8QCQ46WCMF6EC3FBVNTU9Q77XE6QJ6GS9A'
apiurl = "https://api.etherscan.io/api"


def geturl(module, action, address, **kwargs):
    url = apiurl + f"?module={module}&action={action}&address={address}&apikey={apikey}"
    for key, value in kwargs.items():
        url += f"&{key}={value}"
    return url


def getbalance(address):
    balance_url = geturl("account", "balance", address, tag="latest")
    response = get(balance_url)
    data = response.json()
    value = int(data["result"])/1000000000000000000
    return value


def gettransactions(address, maximum):
    if int(maximum) > 10000:
        offset = 10000
    else:
        offset = maximum

    transactions_url = geturl("account", "txlist", address, startblock=0, endblock=99999999, page=1, offset=offset,
                                    sort="asc")
    try:
        response = get(transactions_url)
        data = response.json()["result"]
    except:
        print('Error')
        return

    internal_tx_url = geturl("account", "txlistinternal", address, startblock=0, endblock=99999999, page=1,
                                   offset=offset, sort="asc")
    try:
        response2 = get(internal_tx_url)
        internal = response2.json()["result"]
    except:
        print('Error')
        return

    data.extend(internal)
    data.sort(key=lambda x: int(x['timeStamp']))
    data.reverse()
    data = data[:int(maximum)]

    addr_list = []
    current_balance = getbalance(address)
    i = 0  # keep track of transaction number
    output = pd.DataFrame(columns=['TXindex', 'In', 'Out', 'Value', 'HashID', 'ContractAddress', 'Time'])

    #from addressdata import datadump
    #datadump(data)

    for tx in data:
        i += 1
        addrto = tx['to']
        addrfrom = tx["from"]
        value = int(tx["value"])/1000000000000000000
        txid = tx['hash']
        contractaddress = tx['contractAddress']
        time = datetime.fromtimestamp(int(tx['timeStamp']))

        if addrto == address:
            addr_list.append(addrfrom)
            signedvalue = '+{}'.format(value)

        else:
            addr_list.append(addrto)
            signedvalue = '-{}'.format(value)

        if not contractaddress:
            contractaddress = 'No Address Found'

        if not addrto:
            addrto = 'No Address Found'

        if not addrfrom:
            addrfrom = 'No Address Found'

        index = pd.DataFrame(
            {'TXindex': [i], 'In': [addrfrom], 'Out': [addrto], 'Value': [value], 'HashID': [txid], 'ContractAddress':
                [contractaddress], 'Time': [time]})
        output = pd.concat((output, index), ignore_index=True)

    # identify linked addresses
    from addressdata import addrcount
    linkedaddrs = addrcount(addr_list)
    print('\n', (len(linkedaddrs.index)), 'Potentially linked addresses found.')

    export = input(colored('\nWould you like the transaction data exported as an excel file? (Y/N):\n', 'blue'))

    if export.upper() == "Y" or export.upper() == "YES":

        # Create Excel writer object
        with pd.ExcelWriter(address + ".xlsx") as writer:
            if len(linkedaddrs.index) > 0:
                # Add linked address dataframe as a sheet
                linkedaddrs.to_excel(writer, sheet_name='Linked Addresses', index=True)

            # Add sanction dataframe as a sheet
            from OfacXML import xmlsearch
            sanctioned = xmlsearch(address)
            if not sanctioned.empty:
                sanctioned.to_excel(writer, sheet_name='Sanction Data', index=True)

            # Add transaction dataframe as a sheet
            output.to_excel(writer, sheet_name=("Transaction Data"), index=False)

        print(
            '\nYour file can be found in the same folder in which you saved this program.\n \nThe file is named:\n' +
            address + '.xlsx')


def ETHaccount():

    address = input(colored('\nWhat is the address you would like to analyze? \n', 'blue'))
    if len(address) != 42:
        print('\n Sorry, ETH addresses must be 42 characters.')
    else:
        pass
    if address[0] == '0' and address[1] == 'x':
        pass
    else:
        print('\n Sorry, ETH addresses start with 0x')

    print(colored('\nFetching your results. Please wait...\n', 'yellow'))
    balance = getbalance(address)
    print('Address: ' + address)
    from FindPrice import price
    print('Current Balance: {:.8f} ETH ${:,.2f} USD'.format(balance, price(balance, 'ethereum', 'usd')))

    return address
