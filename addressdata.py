import requests
import json
import datetime
import pandas as pd
from termcolor import colored


# accepts address and dict of data
# record and print basic info
def printaccountdata(address, r):
    # record basic info on address
    received = (r.get('total_received')) / 100000000
    sent = (r.get('total_sent')) / 100000000
    balance = (r.get('final_balance')) / 100000000
    totaltransactions = r.get('n_tx')

    # print out info
    print('Address: ' + address)
    print('Total Received: %.8f' % received)
    print('Total Sent: %.8f' % sent)
    print('Current Balance: %.8f' % balance)
    print('Total Transactions: ', totaltransactions)

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
    dataframe_list = [] # list of transaction dataframes
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
            print("Amount traded by this address: %.8f" % float(result))

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
            input_value = (input_data_list['value']) / 100000000
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
                print('Value: %.8f' % float(input_value))
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
                print('Value: %.8f' % float(output_value))
                print('Spent: ', output_spent)

        i += 1

    if keyerror:
        print('\nError occurred, could not find address for: ')
        print(error_list)

    linkedaddrs = addrcount(addr_list)
    print('\n', (len(linkedaddrs.index)), ' Potentially linked addresses found.')

    # Prompt user to export transactions
    export = input(colored('\nWould you like the transaction data exported as an excel file? (Y/N):\n', 'blue'))

    if export.upper() == "Y" or export.upper() == "YES":
        i = 0

        # Create Excel writer object
        with pd.ExcelWriter(addr + ".xlsx") as writer:
            i = 0
            linkedaddrs.to_excel(writer, sheet_name='Linked Addresses', index=True)
            # Add each transaction dataframe as a sheet
            for tx in dataframe_list:
                i += 1
                tx.to_excel(writer, sheet_name=("Transaction %d" % i), index=False)

        print(
            '\nYour file can be found in the same folder in which you saved this program.\n \nThe file is named:\n' +
            addr + '.xlsx')

    return


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
