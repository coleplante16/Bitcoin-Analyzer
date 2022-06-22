from lxml import etree as et
import numpy as np
import re
import pandas as pd
import ftplib


# downloads sdn list as sdn.xml
def xmlpull():
    sdn = ftplib.FTP("ofacftp.treas.gov")
    sdn.login("anonymous", "password")

    sdn.cwd('/fac_delim/')
    try:
        sdn.retrbinary("RETR " + 'sdn.xml', open('sdn.xml', 'wb').write)
    except:
        print("Error")
    sdn.quit()


# Searches output.xml for a given address
# if found creates a dataframe of important info
# else returns empty dataframe
# accepts
#   address
# returns
#   dataframe
def xmlsearch(addr):
    tree = et.parse('output.xml')
    root = tree.getroot()
    xmlns = "http://tempuri.org/sdnList.xsd"

    for entry in root:
        addressfound = False
        for k in entry:
            if k.tag == '{%s}sdnType' % xmlns:
                #print(k.text)
                if k.text == 'Individual':
                    individual = True
                else:
                    individual = False

            if k.tag == '{%s}idList' % xmlns:
                for child in k:
                    if re.search('Digital Currency Address', child[1].text):
                        if child[2].text == addr:
                            print('found')
                            foundentry = entry

    if foundentry is not None:
        # output = pd.DataFrame([['Tag:', 'Text:']],columns=list('AB'), index=['1'])
        output = pd.DataFrame(columns=['Tag', 'Text'])
        for k in foundentry:
            if k.tag == '{%s}firstName' % xmlns:
                index = pd.DataFrame({'Tag': ['firstName'], 'Text': [k.text]})
                output = pd.concat((output, index), ignore_index=True)

            if k.tag == '{%s}lastName' % xmlns:
                index = pd.DataFrame({'Tag': ['lastName'], 'Text': [k.text]})
                output = pd.concat((output, index), ignore_index=True)

            if k.tag == '{%s}sdnType' % xmlns:
                index = pd.DataFrame({'Tag': ['sdnType'], 'Text': [k.text]})
                output = pd.concat((output, index), ignore_index=True)

            if k.tag == '{%s}programList' % xmlns:
                for i in k:
                    index = pd.DataFrame({'Tag': ['program'], 'Text': [i.text]})
                    output = pd.concat((output, index), ignore_index=True)

            if k.tag == '{%s}idList' % xmlns:
                for i in k:
                    index = pd.DataFrame({'Tag': [i[1].text], 'Text': [i[2].text]})
                    output = pd.concat((output, index), ignore_index=True)

    else:
        output = pd.DataFrame({'A': []})

    return output


# parse through sdnlist
# creates new file of all sanctions with crypto addresses
def xmlparse():
    tree = et.parse('sdn.xml')
    xmlns = "http://tempuri.org/sdnList.xsd"
    root = tree.getroot()

    export = et.Element("entries")

    for entry in root:
        addressfound = False
        for k in entry:
            if k.tag == '{%s}idList' % xmlns:
                for child in k:
                    if re.search('Digital Currency Address', child[1].text):
                        addressfound = True
        if addressfound:
            export.append(entry)

    et.ElementTree(export).write('output.xml', pretty_print=True, xml_declaration=True, encoding="utf-8")


# accepts
#   sanction info dataframe
# returns
#   dataframe of just addresses
def addresssort(sanctiondf):
    addresses = np.where(sanctiondf['Tag'].str.contains('Digital Currency Address*'))
    addressdf = sanctiondf.iloc[addresses]
    addressdf.sort_index(inplace=True, ignore_index=True)
    # print(addressdf)
    return addressdf


# accepts
#   sanction info dataframe
# returns
#   dataframe of just Bitcoin addresses
def addressBTC(sanctiondf):
    return addressType(sanctiondf, 'XBT')


# accepts
#   sanction info dataframe
#   currency id
# returns
#   dataframe of just addresses for the selected currency
def addressType(sanctiondf, currency):
    addresses = np.where(sanctiondf['Tag'].str.contains('*{}'.format(currency)))
    addressdf = sanctiondf.iloc[addresses]
    addressdf.sort_index(inplace=True, ignore_index=True)
    # print(addressdf)
    return addressdf


def acceptedCurrencies(cryptoid):
    v = True
    currencies = pd.DataFrame({
        'Currency': ['Bitcoin', 'Ethereum', 'Litecoin', 'Neo', 'Dash', 'Ripple', 'Iota', 'Monero', 'Petro'],
        'ID': ['XBT', 'ETH', 'LTC', 'NEO', 'DASH', 'XRP', 'MIOTA', 'XMR', 'PTR']})

    if (currencies['ID'].str.contains(cryptoid)).any():
        return True
    else:
        if v:
            print('ID not found, acceepted IDs:')
            print(currencies)
        return False