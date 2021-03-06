This project [will be] capable of finding
bitcoin accounts associated with specific names or emails, and
mapping transactions related to those accounts in a graphical confluence network.


Cloning the repository:
    git clone https://github.com/coleplante16/Bitcoin-Analyzer/.git

QUICK START:
1.  To begin, ensure you have the proper dependencies installed. (pip install -r requirements.txt). 
    You will also need to download yEd if you would like to view the graphical confluence networks 
    of transactions.
2.  If you would like to use sherlock within this program, you will need to add the path to the 
    sherlock folder to the main file (lines 26-28).
3.  You may run this program from the terminal or a python console. If run through terminal, please
    change the final line from 'welcome()' to 'main()' as the welcome message is not yet compatible
    with a terminal. You may also need to add quotation marks to your inputs when executing through
    a terminal. (python3 Bitcoin\ Analyzer.txt)



Color Code:
Below you will find a list of text colors and their meanings:
1.  Blue: 
    User input prompt. 
    Links also appear blue.
3.  Yellow:
        Main menu: Partially complete option.
        While executing program: Fetching results, please wait.
3.  Green: informational text
4.  Red:
        Main menu: unavailable option.
        While executing program: Notice to user.



EXAMPLE USES:
1.  Usernames to search (main menu option 1):
    Powered by the Sherlock Project (https://github.com/sherlock-project/sherlock). Please see the user license in the Sherlock folder.
    
2.  Emails to search (main menu option 2):
    NOTICE: If you wish to use the haveibeenpwned functionality, please purchase a API key from https://haveibeenpwned.com/API/Key
    
    1.  mr.xtraf@gmail.com
    2.  carl_alberto@zohomail.com
    3.  lukanvibes001@gmail.com
    4.  stewartrhiannon488@gmail.com

3.  BTC addresses to examine:
           
    1.  1NEh2qQaKkxb8DWuPTuFLsxF2gxWeNrvAH
    2.  3GVpMEso5wdDJxwNPQEXjm2FNj5BcDxrsW
    3.  1PusX7fKJorWWfH9NVrSmvSQr76tBqMknk
    4.  392xnqCXwa4TophjvxChXy9QXNvoNbVUuw
