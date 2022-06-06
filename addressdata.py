import requests
import json

def accountdata():
    # address = input('\nWhat is the address you would like to analyze? \n')
    address = '1NEh2qQaKkxb8DWuPTuFLsxF2gxWeNrvAH'  # hard coded for convenience in early testing
    transactions = input('\nPlease type in the maximum number of transactions you would like.\n')

    URL = 'https://blockchain.info/rawaddr/' + address + "?limit=" + transactions
    # grabs json from url and build dictionary
    r = requests.get(URL).json()

    # record basic info on address
    received = (r.get('total_received'))/100000000
    sent = (r.get('total_sent'))/100000000
    balance = (r.get('final_balance'))/100000000
    transactions = r.get('n_tx')

    # print out info
    print('Address: ' + address)
    print('Total Received: ', received)
    print('Total Sent: ', sent)
    print('Current Balance: ', balance)
    print('Total Transactions: ', transactions)

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


    # prompt to print raw data
    raw = input('\nWould you like to print raw data? (Y/N):\n')
    if raw.upper() == "Y" or raw.upper() == "YES":
        data = json.dumps(r, sort_keys=True, indent=4)
        print('\n\n' + data)

accountdata()