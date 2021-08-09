# Bitcoin-Analyzer
This project was completed in partial fulfilment of the requirements
for a masters degree in cybersecurity at Mercyhurst University.

                          █████████
                          █▄─▀█▀─▄█
                          ██─█▄█─██
                          ▀▄▄▄▀▄▄▄▀

Welcome to the Bitcoin analyzer. This project [will be] capable of finding
bitcoin accounts associated with specific names or emails, and
mapping transactions related to those accounts in a graphical confluence network.



QUICK START:
1.  To begin, ensure you have the proper dependencies installed. (pip install -r requirements.txt)
2.  You may run this program from the terminal or a python console. If run through terminal, please
    change the final line from 'welcome()' to 'main()' as the welcome message is not yet compatible
    with a terminal. You may also need to add quotation marks to your inputs when executing through
    a terminal. (python3 Bitcoin\ Analyzer.txt)
3.  There is an additional python file "BTC2Currency.py" that will currently convert BTC to USD or CAD.
    The program will be capable of EUR and GBP once a selenium package is added to disable the GDPR notice.
    The program will be integrated into the "Bitcoin Analyzer.py" program once it is complete. If you would
    like to run this program separately, it can be run in a python console or in a terminal with the command
    "python3 BTC2Currency.py".



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
1.  Names to search (main menu option 1):
    Not functional yet.

2.  Emails to search (main menu option 2):
    NOTICE: Users may need to remove "&amp..." from links as google appends additional information to links
    1.  mr.xtraf@gmail.com
    2.  carl_alberto@zohomail.com
    3.  lukanvibes001@gmail.com
    4.  stewartrhiannon488@gmail.com

3.  BTC addresses to examine:
    NOTICE: Module not yet completed, will only show most recent transaction.
    1.  1NEh2qQaKkxb8DWuPTuFLsxF2gxWeNrvAH
    2.  3GVpMEso5wdDJxwNPQEXjm2FNj5BcDxrsW
    3.  1PusX7fKJorWWfH9NVrSmvSQr76tBqMknk
    4.  392xnqCXwa4TophjvxChXy9QXNvoNbVUuw
