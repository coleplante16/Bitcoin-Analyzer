import requests
import json
import datetime
import pandas as pd
from termcolor import colored
from FindPrice import btctousd


def BTCaccount(address):
    if len(address) < 26:
        print('\n Sorry, that wasn\'t quite long enough.')
        from account import account
        account('BTC')
    else:
        pass
    if address[0] == 1 or 3:
        pass
    elif address[0] == 'b' and address[1] == 'c' and address[2] == '1':
        pass
    else:
        print('/n Sorry, Bitcoin addresses start with either 1, 3, or bc1.')
        account('BTC')

    print(colored('\nFetching your results. Please wait...\n', 'yellow'))
    r = getdata(address)
    printaccountdata(address, r)

    return address


# accepts address and dict of data
# record and print basic info
def printaccountdata(address, r):
    # record basic info on address
    received = (r.get('total_received')) / 100000000
    sent = (r.get('total_sent')) / 100000000
    balance = (r.get('final_balance')) / 100000000
    totaltransactions = r.get('n_tx')
    # sanctioned = ofaccheck(address)

    # check for sanctions
    from OfacXML import xmlsearch
    sanctioned = xmlsearch(address)

    coin = 'btc'
    currency = 'usd'
    from FindPrice import price
    convert = price(coin.lower(), currency.lower())

    # print out info
    print('Address: ' + address)
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

    return r


# Print out transaction data
def accounttransactions(r, txs, addr):
    # rough outline of how transactions are formatted
    # ignores unimportant data
    # "txs":[
    #       {
    #       "fee":
    #       "hash":
    #       "inputs":
    #               [
    #               {
    #               "index":
    #               "prev_out":
    #                   {
    #                   "addr": (address)
    #                   "spent":
    #                   "value": (in satoshis)
    #                   }
    #               }
    #               {
    #                   next input
    #               }
    #               ]
    #       "out": [
    #               {
    #               "addr": (address)
    #               "spent":
    #               "value": (in satoshis)
    #               }
    #               {
    #                other outputs
    #               }
    #              ]
    #       "result": (amount sent or received by given address)
    #       "time": (unix time)
    #       }
    #       {
    #        next transaction
    #       }
    #      ]
    #
    printall = input(colored('\nPrint data for each transaction? (Y/N):\n', 'blue'))
    if printall.upper() == "Y" or printall.upper() == "YES":
        printbasic = True
        printio = input(colored('\nPrint inputs and outputs of each transaction? (Y/N):\n', 'blue'))
        if printio.upper() == "Y" or printio.upper() == "YES":
            printtf = True
        else:
            printtf = False
    else:
        printbasic = False
        printtf = False
    # Make list of transactions
    addr_list = []
    transaction_list = r['txs']
    keyerror = False
    error_list = []
    i = 0  # keep track of transaction number
    dataframe_list = []  # list of transaction dataframes
    blank = pd.DataFrame({'A': [' '], 'B': [' '], 'C': [' '], 'D': [' ']})  # blank line for spaces data frames

    # Read data from each transaction
    for transaction_data in transaction_list:

        # Collect basic transaction data
        hashid = transaction_data['hash']
        tx_time = datetime.datetime.fromtimestamp(transaction_data['time'])
        result = (transaction_data['result']) / 100000000

        # Add basic transaction data to top of that transactions dataframe
        dataframe_list.append(
            pd.DataFrame(
                [
                    ['Transaction:', 'Transaction Hash ID:', 'Time of Transaction:',
                     'Amount traded by this address:'], [(i + 1), hashid, tx_time, result]
                ],
                columns=list('ABCD'), index=['1', '2']
            )
        )

        # Add space to data frame before inputs
        dataframe_list[i] = pd.concat((dataframe_list[i], blank), ignore_index=True)

        if printbasic:
            # Print basic data
            print("\n\nTransaction: ", (i + 1))
            print("Transaction Hash ID:", hashid)
            print("Time of Transaction: ", tx_time)
            print("Amount traded by this address: {:.8f} BTC ${:,.2f} USD".format(result, btctousd(result)))

        if printtf:
            print("\nINPUTS: ")
        # Make list of inputs
        input_list = transaction_data['inputs']

        index = pd.DataFrame({'A': ['Input:'], 'B': ['Address:'], 'C': ['Value:'], 'D': ['Spent:']})
        dataframe_list[i] = pd.concat((dataframe_list[i], index), ignore_index=True)

        # Collect and print out data from each input
        for input_data in input_list:
            input_data_list = input_data['prev_out']

            # Collect input data
            input_index = (input_data['index'] + 1)
            input_address = input_data_list['addr']
            input_value = -(input_data_list['value']) / 100000000
            input_spent = input_data_list['spent']

            if input_address != addr:
                addr_list.append(input_address)

            # Add input data to dataframe
            index = pd.DataFrame({'A': [input_index], 'B': [input_address], 'C': [input_value], 'D': [input_spent]})
            dataframe_list[i] = pd.concat((dataframe_list[i], index), ignore_index=True)

            if printtf:
                # Print input data to dataframe
                print("\nInput: ", input_index)
                print('Address: ', input_address)
                print('Value: {:.8f} BTC ${:,.2f} USD'.format(input_value, btctousd(input_value)))
                print('Spent: ', input_spent)

        # add output header to dataframe
        dataframe_list[i] = pd.concat((dataframe_list[i], blank), ignore_index=True)
        index = pd.DataFrame({'A': ['Output:'], 'B': ['Address:'], 'C': ['Value:'], 'D': ['Spent:']})
        dataframe_list[i] = pd.concat((dataframe_list[i], index), ignore_index=True)

        if printtf:
            print("\nOUTPUTS: ")

        # make list of outputs
        output_list = transaction_data['out']
        output_index = 0

        # Collect and print data from each output
        for output_data in output_list:
            output_index += 1

            # Collect output data
            try:
                output_address = output_data['addr']
            except KeyError:
                output_address = 'error'
                keyerror = True
                error_list.append('Transaction: {} Output: {}'.format(i, output_index))

            output_value = output_data['value'] / 100000000
            output_spent = output_data['spent']

            if keyerror:    # do not include "error"
                pass
            elif output_address != addr:
                addr_list.append(output_address)

            # Add output data tp dataframe
            index = pd.DataFrame({'A': [output_index], 'B': [output_address], 'C': [output_value], 'D': [output_spent]})
            dataframe_list[i] = pd.concat((dataframe_list[i], index), ignore_index=True)

            if printtf:
                # Print output data
                print("\nOutput: ", output_index)
                print('Address: ', output_address)
                print('Value: {:.8f} BTC ${:,.2f} USD'.format(output_value, btctousd(output_value)))
                print('Spent: ', output_spent)

        i += 1

    if keyerror:
        print('\nError occurred, could not find address for: ')
        print(error_list)

    # make dataframe of linked addresses
    linkedaddrs = addrcount(addr_list)
    print('\n', (len(linkedaddrs.index)), 'Potentially linked addresses found.')

    # Prompt user to export transactions
    export = input(colored('\nWould you like the transaction data exported as an excel file? (Y/N):\n', 'blue'))

    if export.upper() == "Y" or export.upper() == "YES":
        i = 0

        # Create Excel writer object
        with pd.ExcelWriter(addr + ".xlsx") as writer:
            i = 0
            if len(linkedaddrs.index) > 0:
                # Add linked address dataframe as a sheet
                linkedaddrs.to_excel(writer, sheet_name='Linked Addresses', index=True)

            from OfacXML import xmlsearch
            sanctioned = xmlsearch(addr)
            if not sanctioned.empty:
                sanctioned.to_excel(writer, sheet_name='Sanction Data', index=True)

            # Add each transaction dataframe as a sheet
            for tx in dataframe_list:
                i += 1
                tx.to_excel(writer, sheet_name=("Transaction %d" % i), index=False)

        print(
            '\nYour file can be found in the same folder in which you saved this program.\n \nThe file is named:\n' +
            addr + '.xlsx')
    
    #from Untitled.ipynb import buildgraph
    #graph = buildgraph(addr, addrdict)
    #graph.show()
    return addr_list


# dump all recorded data
def datadump(r):
    data = json.dumps(r, sort_keys=True, indent=4)
    print('\n\n' + data)


# grabs json from url and build dictionary
# with no transactions
def getdata(address):
    URL = 'https://blockchain.info/rawaddr/' + address + "?limit=0"
    r = requests.get(URL).json()
    return r


# grabs json from url and build dictionary
# with specified number of transactions
def gettransactions(address, transactions):
    URL = 'https://blockchain.info/rawaddr/' + address + "?limit=" + transactions
    r = requests.get(URL).json()
    return r


# dump all data for a single transaction
def transactiondump():
    hashid = input(colored('\nWhat is the tx hash id you would like to analyze? \n', 'blue'))
    URL = 'https://blockchain.info/rawtx/'+ hashid
    r = requests.get(URL).json()
    datadump(r)


# accepts list of addresses
# returns dataframe with times each address appears
def addrcount(addrs):
    count = {}
    for i in addrs:
        if addrs.count(i) > 1:
            count[i] = addrs.count(i)
    table = pd.DataFrame.from_dict(count, orient='index', columns=['Count'])
    table.sort_values(by=['Count'], ascending=False, inplace=True)
    return table


# uses cryptofac api to test if an address has been sanctioned
# could be expanded to check up to 25 addresses at once
# NOT ACCURATE AND MISSES SOME ADDRESSES
#
# accepts
#   a crypto address
#       accepted currencies
#           (BTC, ETH, LTC, ZEC, BSV, DASH, BCH, XMR, BTG, ETC, XVG, USDT, XRP)
# returns
#   T/F of if address has been sanctioned
#   Associated Entity of the sanction
def ofaccheck(addr):
    URL = 'https://cryptofac.org/api/?q=' + addr
    r = (requests.get(URL)).json()

    if r[0]['match']:
        out = [r[0]['match'], r[0]['entity']]
    else:
        out = [r[0]['match']]
    return out

