import requests
import json

def accountdata():
    # address = input('\nWhat is the address you would like to analyze? \n')
    address = '1NEh2qQaKkxb8DWuPTuFLsxF2gxWeNrvAH'  # hard coded for convenience in early testing
    transactions = input('\nPlease type in the maximum number of transactions you would like to load.\n')

    URL = 'https://blockchain.info/rawaddr/' + address + "?limit=" + transactions
    # grabs json from url and build dictionary
    r = requests.get(URL).json()

    # record basic info on address
    received = (r.get('total_received'))/100000000
    sent = (r.get('total_sent'))/100000000
    balance = (r.get('final_balance'))/100000000
    totaltransactions = r.get('n_tx')

    # print out info
    print('Address: ' + address)
    print('Total Received: ', received)
    print('Total Sent: ', sent)
    print('Current Balance: ', balance)
    print('Total Transactions: ', totaltransactions)


    # rough outline of how transactions are formatted
    # ignores unimportant data
    # "txs":[
    #       {
    #       "fee":
    #       "hash":
    #       "inputs":[
    #               {
    #               "index":
    #               "prev_out": {
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

    # Print out transaction data
    transaction = input('\nWould you like to print out transaction data? (Y/N):\n')
    if transaction.upper() == "Y" or transaction.upper() == "YES":

        # Make list of transactions
        transaction_list = r['txs']
        print(type(transaction_list))

        i=0 # keep track of transaction number

        # Read data from each transaction
        for transaction_data in transaction_list:

            i += 1
            print("\n\nTransaction: ", i)
            print("Transaction Hash ID:", transaction_data['hash'])

            print("\nINPUTS: ")
            # Make list of inputs
            input_list = transaction_data['inputs']

            # Print out data from each input
            for input_data in input_list:
                print("\nInput: ", (input_data['index'] + 1))
                input_data_list = input_data['prev_out']
                print('Address: ', input_data_list['addr'])
                print('Value: ', (input_data_list['value'])/100000000)
                print('Spent: ', input_data_list['spent'])

            print("\nOUTPUTS: ")
            # make list of outputs
            output_list = transaction_data['out']
            j = 0

            # Print out data from each output
            for output_data in output_list:
                j += 1
                print("\nOutput: ", j)
                print('Address: ', output_data['addr'])
                print('Value: ', (output_data['value'])/100000000)
                print('Spent: ', output_data['spent'])


    # prompt to print raw data
    raw = input('\nWould you like to print raw data? (Y/N):\n')
    if raw.upper() == "Y" or raw.upper() == "YES":
        data = json.dumps(r, sort_keys=True, indent=4)
        print('\n\n' + data)

accountdata()