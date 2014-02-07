"""  app.py -- Main Application File
# Created: 1/12/14
# Author: Muhammad Sajawal Javaid (5933252)
# Last Modified: 1/12/14
"""

import sys, getopt

sys.path.append('./applibs/')

STOPWORD_FILE = './resources/StopWords.txt'
DOCUMENTS_FILE = './resources/Trec_microblog11.txt'

from applibs.initialize import initialize

from applibs.gui import APPLICATION

def main(argv):
    useCache = False
    try:
        opts, args = getopt.getopt(argv, "c:", ["use-cache="])
    except getopt.GetoptError:
        print("Usage: app.py [-c|--use-cache]")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-c", "--use-cache"):
            useCache = True
    initialize(STOPWORD_FILE, DOCUMENTS_FILE, useCache)
    app = APPLICATION()
    app.mainloop()

if __name__=="__main__":
    main(sys.argv[1:])