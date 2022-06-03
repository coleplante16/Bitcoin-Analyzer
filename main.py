from termcolor import colored
import requests
from bs4 import BeautifulSoup
import re
import pandas
import pyyed
import numpy
import os
import sys
from os.path import dirname


# Main Menu
def main():
    print(colored('\nPlease select an option from the list below:', 'green'))
    print(colored('1. Find an account based on a person\'s username using Sherlock', 'red'))
    print(colored('2. Find an account based on a person\'s email', 'yellow'))
    print(colored('3. Analyze an account you already know', 'yellow'))
    print('4. Quit\n')

    choice = int(input((colored('Enter your choice: \n', 'blue'))))

    if choice == 1:
        user = input(colored('\nPlease enter the username you believe is linked to a bitcoin account:\n', 'blue'))
        print('')
        
#Enter path to sherlock.py here
        script_descriptor = open('sherlock/sherlock/sherlock.py')
        
        sherlock = script_descriptor.read()
        sys.argv = [sherlock, user]
        exec(sherlock)
        
    elif choice == 2:
        from EmailSearch import acctEmail
        acctEmail()

    elif choice == 3:
        from account import account
        account()

    elif choice == 4:
        quit()

    else:
        print('Sorry, you entered an invalid option.\n')
        prompt = input(colored('Would you like to try again? (Y/N): \n', 'blue'))
        if prompt.upper() == "Y" or prompt.upper() == "YES":
            main()
        else:
            quit()


def welcome():
    logo = colored('█████████', 'green')
    logo1 = colored('█▄─▀█▀─▄█', 'green')
    logo2 = colored('██─█▄█─██', 'green')
    logo3 = colored('▀▄▄▄▀▄▄▄▀', 'green')
    logo = logo.center(70, ' ')
    logo1 = logo1.center(70,' ')
    logo2 = logo2.center(70,' ')
    logo3 = logo3.center(70,' ')
    print(colored('This project was completed in partial fulfilment of the requirements \nfor a masters degree in Cybersecurity at Mercyhurst University.\n', 'green'))
    print(logo)
    print(logo1)
    print(logo2)
    print(logo3)
    print(colored('\nWelcome to the Bitcoin analyzer. This project is capable of finding \nbitcoin accounts associated with specific names or emails, and \nmapping transactions related to those accounts.', 'green'))
    main()


welcome()
