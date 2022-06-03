from termcolor import colored
import pyyed

def exportCSV(transactionsChart, address):
    export = input(colored('\nWould you like this exported as a csv file? (Y/N)\n', 'blue'))
    if export.upper == "Y" or export.upper == "YES":
        #path = input(colored('Please enter the path for which you would like the file saved:\n'))
        transactionsChart.to_csv(address + '.csv')
        print('\nexported as ', address, '.csv')
    else:
        pass

def export_yEd(address, var4):
    print('Now entering export_yEd')
    yEd = input(colored('\nWould you like a graphical display of these transactions? (Y/N) \n', 'blue'))
    if yEd.upper() == "Y" or yEd.upper() == "YES":
        linkChart = pyyed.Graph()
        linkChart.add_node(address, font_family='Dialog', font_size="20", height="100", width='100')
        for i in var4:

# add nodes (addresses) while passing over existing nodes (NEEDS WORK)
# add edges with labels as amount transferred
            for word in i:
#insert scratch14 if necessary
                if word == 'From':
                    sendAcctNoIndex = i.index(word)
                    sendAcctNoIndex += 1
                    sendAcctNo = i[sendAcctNoIndex]
                    amtSpentIndex = i.index(word)
                    amtSpentIndex += 2
                    amtSpent = i[amtSpentIndex]
                if word == 'To':
                    try:
                        receiveAcctNoIndex = i.index(word)
                        receiveAcctNoIndex += 1
                        receiveAcctNo = i[receiveAcctNoIndex]
                    except:
                        pass
                    try:
                        amtSentindex = i.index(word)
                        amtSentindex += 2
                        amtSent = i[amtSentindex]
                    except:
                        pass
                    try:
                        linkChart.add_node(str(sendAcctNo) + '\nSpent: ' + str(amtSpent), font_family='Dialog')
                        linkChart.add_node(str(receiveAcctNo), font_family='Dialog')
                        linkChart.add_edge(str(sendAcctNo), str(receiveAcctNo), label=str(amtSent))
                    except RuntimeWarning:
                        try:
                            linkChart.add_node(receiveAcctNo, font_family='Dialog')
                            linkChart.add_edge(str(sendAcctNo), str(receiveAcctNo), label=str(amtSent))
                        except RuntimeWarning:
                            try:
                                linkChart.add_node(str(sendAcctNo) + '\nSpent: ' + str(amtSpent), font_family='Dialog')
                                linkChart.add_edge(str(sendAcctNo), str(receiveAcctNo), label=str(amtSent))
                            except RuntimeWarning:
                                try:
                                    linkChart.add_edge(str(sendAcctNo), str(receiveAcctNo), label=str(amtSent))
                                except RuntimeWarning:
                                    pass


        linkChart.write_graph(address, + '.graphml')

    else:
        print(colored('\nWhat would you like to do next?', 'green'))
        print('1. Search for this account online.')
        print('2. Find a different account.')
        print('3. Main Menu')
        print('4. Quit')
        choice = input(colored('\nPlease enter your choice (1-4):\n', 'blue'))
        if choice == '1':
            print(address)
            URL = 'https://www.allprivatekeys.com/btc/' + address + '#pills-Forum'
            r = requests.get(URL)
            soup = BeautifulSoup(r.content, 'html5lib')
            acctInfo = str(soup.find_all('div', attrs={'class': 'media text-muted pt-3'}))
            potentialLink = (re.findall(r'(https?://\S+)', acctInfo)) + (re.findall(r'(https?://\S+)', acctInfo))
            if not potentialLink:
                print('Sorry, we couldn\'t find the account mentioned anywhere...')
                quit()
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
            if export.upper() == "Y" or export.upper() == "YES":
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
            from account import account
            account()

        elif choice == '3':
            from main import main
            main()

        elif choice == '4':
            quit()

        else:
            print(colored('Sorry, that wasn\'t an option... quitting now.', 'red'))