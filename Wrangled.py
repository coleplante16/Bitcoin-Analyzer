from termcolor import colored
import requests
from bs4 import BeautifulSoup
import re
import pandas
import pyyed
import numpy

def Wrangled(transactions3, transactions, address):
    for i in transactions3:
            transactions += i

# Remove HTML notation
    transactions4 = []
    for i in transactions:
        i = re.sub('<.+?>', ' ', i)
        i = re.sub(',', '', i)


        i = ' '.join(i.split())
        transactions4.append(i)

# Split into list and remove extra characters
    var1 = []
    for i in transactions4:
        var1 += list(i.split(' '))
    try:
        var1.remove('[')
        var1.remove(']')
    except:
        pass

# Only grab transactional information
    var2 = []
    for item in var1:
        if len(item) > 2:
            var2.append(item)


#
    indices = [i for i, x in enumerate(var2) if x == "Hash"]
    indices2 = []
    indices2 = indices[1:]
    indices2.append(len(var2))


    var3 = []
    counter1 = 0
    for x in range(len(indices)):
        var3 += [var2[indices[counter1]: indices2[counter1]]]
        counter1 += 1


# Remove extra information
    var4 = []
    for i in var3:
        last = (len(i) - 1)
        first = last - 17
        del i[first:last]
        del i[4]
        if 'Load' in i:
            last1 = (len(i) - 3)
            first1 = last1 - 5
            del i[first1:last1]
        var4.append(i)

    for subList in var4:
        position = 0
        length = len(subList)
        for word in subList:
            position = position + 1
            if word == 'BTC' and position < length:
                subList.insert(position, 'To')

# Made Data Frame for Display
    column_names2 = []
    rows = []
    for i in var4:
        column_names2 += i[::2]
        rows += i[1::2]
    #rows.append()
    transactionsChart = pandas.DataFrame(rows, column_names2)
    print(transactionsChart)


#Export as CSV
    from export import exportCSV
    exportCSV(transactionsChart, address)


#Export as Graphical Confluence Network
    from export import export_yEd
    export_yEd(address, var4,)