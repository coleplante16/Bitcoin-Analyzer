from termcolor import colored
import blockcypher as bc
import pandas as pd
import requests
import datetime
key = '398307359db341d5a7f9f31ce32030ef'


def convertbase(coin):
    match coin:
        case 'ETH':
            return 1000000000000000000
        case _:
            return 100000000


def overview(addr, coin, currency):
    if coin.upper() == 'ETH':
        URL = 'https://api.blockcypher.com/v1/eth/main/addrs/' + addr + '/balance'
        r = requests.get(URL).json()
    else:
        r = bc.get_address_overview(addr, coin_symbol=coin.lower(), api_key=key)
    base = convertbase(coin)
    # record basic info on address
    received = (r.get('total_received')) / base    # this conversion value will have to change based on currency
    sent = (r.get('total_sent')) / base            # currently works for BTC, LTC, DASH
    balance = (r.get('final_balance')) / base
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


def addrfull(addr, coin, currency, limit):
    dataframe_list = []  # list of transaction dataframes
    blank = pd.DataFrame({'A': [' '], 'B': [' '], 'C': [' '], 'D': [' ']})  # blank line for spaces data frames

    if coin.upper() == 'ETH':
        URL = 'https://api.blockcypher.com/v1/eth/main/addrs/' + addr + '/full'
        r = requests.get(URL).json()
        eth = True
    else:
        r = bc.get_address_full(addr, coin_symbol=coin.lower(), api_key=key)
        eth = False

    base = convertbase(coin)

    addr_list = []

    txlist = r.get('txs')
    txindex = 0
    for tx in txlist:
        tx_time = tx.get('received')
        if not eth:
            #import dateutil
            #tx_time = dateutil.parser.isoparse(tx_time)
            tx_time = tx_time.replace(tzinfo=None)

        hashid = tx.get('hash')
        addrindex = tx.get('addresses')
        for i in addrindex:
            if i != addr:
                addr_list.append(i)

        count = 0
        input_df = pd.DataFrame({'A': ['Input:'], 'B': ['Address:'], 'C': ['Value:']})
        inputlist = tx.get('inputs')
        for k in inputlist:
            inputaddrlist = k.get('addresses')
            if len(inputaddrlist) > 1:
                input_address = ''.join(inputaddrlist)
                if not eth:
                    for addrin in inputaddrlist:
                        if addrin == addr:
                            result = -k.get('output_value') / base
            else:
                input_address = inputaddrlist[0]
                if not eth:
                    if input_address == addr:
                        result = -k.get('output_value') / base

            input_index = count
            if not eth:
                input_value = (k.get('output_value') / base)
            else:
                input_value = ''

            index = pd.DataFrame({'A': [input_index], 'B': [input_address], 'C': [input_value]})
            input_df = pd.concat((input_df, index), ignore_index=True)
            count += 1

        output_df = pd.DataFrame({'A': ['Output:'], 'B': ['Address:'], 'C': ['Value:']})
        outputlist = tx.get('outputs')
        count = 0
        for output in outputlist:
            outaddrlist = output.get('addresses')
            if len(outaddrlist) > 1:
                outputaddr = ''.join(outaddrlist)
                for addrout in outaddrlist:
                    if addrout == addr:
                        result = output.get('value') / base
            else:
                outputaddr = outaddrlist[0]
                if outputaddr == addr:
                    result = output.get('value') / base

            count += 1
            output_value = (output.get('value')) / base

            index = pd.DataFrame({'A': [count], 'B': [outputaddr], 'C': [output_value]})
            output_df = pd.concat((output_df, index), ignore_index=True)
            count += 1

        # Add basic transaction data to top of that transactions dataframe
        try:
            dataframe_list.append(
                pd.DataFrame(
                    [
                        ['Transaction:', 'Transaction Hash ID:', 'Time of Transaction:',
                         'Amount traded by this address:'], [(txindex + 1), hashid, tx_time, result]
                    ],
                    columns=list('ABCD'), index=['1', '2']
                )
            )
        except UnboundLocalError:
            dataframe_list.append(
                pd.DataFrame(
                    [
                        ['Transaction:', 'Transaction Hash ID:', 'Time of Transaction:',
                         'Amount traded by this address:'], [(txindex + 1), hashid, tx_time, tx.get('total') / base]
                    ],
                    columns=list('ABCD'), index=['1', '2']
                )
            )

        # Add space to data frame before inputs
        dataframe_list[txindex] = pd.concat((dataframe_list[txindex], blank), ignore_index=True)
        # add input frames
        dataframe_list[txindex] = pd.concat((dataframe_list[txindex], input_df), ignore_index=True)
        # Add space to data frame before outputs
        dataframe_list[txindex] = pd.concat((dataframe_list[txindex], blank), ignore_index=True)
        # add output frames
        dataframe_list[txindex] = pd.concat((dataframe_list[txindex], output_df), ignore_index=True)

        txindex += 1

    from addressdata import addrcount
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
    time.sleep(1)
    address = '0x00000000219ab540356cbb839cbe05303d7705fa'
    coin = 'ETH'
    print('\n{}'.format(coin))
    overview(address, coin, usd)

def fulltest():
    import time
    address = '1FfmbHfnpaZjKFvyi1okTjJJusN455paPH'
    crypto = 'BTC'
    usd = 'USD'
    print('\n{}'.format(crypto))
    addrfull(address, crypto, usd, 10)

    time.sleep(1)

    address = '0x00000000219ab540356cbb839cbe05303d7705fa'
    crypto = 'ETH'
    print('\n{}'.format(crypto))
    addrfull(address, crypto, usd, 10)


fulltest()