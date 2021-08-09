from termcolor import colored
import pyyed

def exportCSV(transactionsChart, address):
    export = input(colored('\nWould you like this exported as a csv file? (Y/N)\n', 'blue'))
    if export == 'Y' or 'YES':
        #path = input(colored('Please enter the path for which you would like the file saved:\n'))
        transactionsChart.to_csv(address + '.csv')

    else:
        pass

def export_yEd(address, var4):
    print('Now entering export_yEd')
    yEd = input(colored('\nWould you like a graphical display of these transactions? (Y/N) \n', 'blue'))
    if yEd.upper() == 'Y' or yEd.upper() == 'YES':
        linkChart = pyyed.Graph()
        linkChart.add_node(address, font_family='Dialog', font_size="20", height="100", width='100')
        for i in var4:

# add nodes (addresses) while passing over existing nodes (NEEDS WORK)
# add edges with labels as amount transferred
            for word in i:
                if word == 'From':
                    try:
                        w = i.index(word)
                        w += 1
                        print("\nw:" + str(w))
                        linkChart.add_node((i[w]), font_family='Dialog')
                        x = w+3
                        print('\nx:', +str(x))
                        linkChart.add_node((i[x]), font_family='Dialog')
                        l = w + 1
                        print('\nl:', + str(l))
                        linkChart.add_edge(i[w], i[x], label = l, font_family='Dialog')
                    except:
                        pass

                        try:
                            w = i.index(word)
                            l = w + 1
                            x = w + 4
                            w += 1
                            linkChart.add_node(i[x], font_family='Dialog')
                            linkChart.add_edge(i[w], i[x], label = l)
                        except:
                            l = w + 1
                            x = w + 4
                            w += 1
                            linkChart.add_edge(i[w], i[x], label = l)

        filePath = r'/Users/cole_plante/Desktop/' + str(address) + '.graphml'
        print(filePath)
        linkChart.write_graph(filePath)