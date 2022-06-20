from lxml import etree as et
import re
import pandas as pd
import ftplib


def xmlpull():
    sdn = ftplib.FTP("ofacftp.treas.gov")
    sdn.login("anonymous", "password")

    sdn.cwd('/fac_delim/')
    try:
        sdn.retrbinary("RETR " + 'sdn.xml', open('sdn.xml', 'wb').write)
    except:
        print("Error")
    sdn.quit()


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

    if foundentry:
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

        print(output)

    else:
        output = pd.DataFrame({'A': []})

    return output

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