"""  app.py -- Main Application File
# Created: 1/12/14
# Author: Muhammad Sajawal Javaid (5933252)
# Last Modified: 1/12/14
"""

import sys

sys.path.append('./applibs/')

STOPWORD_FILE = './resources/StopWords.txt'
DOCUMENTS_FILE = './resources/Trec_microblog11.txt'

from applibs.initialize import initialize

from applibs.gui import APPLICATION

if __name__=="__main__":
    initialize(STOPWORD_FILE, DOCUMENTS_FILE)
    app = APPLICATION()
    app.mainloop()
