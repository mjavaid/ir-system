""" utils.py -- Application Utility Functions
# Created: 1/12/14
# Author: Rayan Alsubhi & Muhammad Sajawal Javaid (5933252)
# Last Modified: 1/12/14
"""

DOCUMENTS_FILE = "../resources/Trec_microblog11.txt"
TWEET_ID = 0

""" GLOBAL SYSTEM VARIABLES """

STOPWORD_LIST = [
    "the", "a", "be", "it"
]
DOCUMENTS = []

""" END GLOBAL SYSTEM VARIABLES """

""" GLOBAL SYSTEM FUNCTIONS """

### populateDocuments
# Reads the corpus file and populates the DOCUMENTS list in the IR system
# which will be used for querying.
###
def populateDocuments():
    input = open(DOCUMENTS_FILE, "r")
    docs = (input.read()).split("\n")
    i = 0
    list = []
    for doc in docs:
        docInfo = doc.split()
        if docInfo:
            DOCUMENTS.append({"D"+str(i):{"id": docInfo[TWEET_ID], "text": docInfo[TWEET_ID+1:]}})
            i += 1

""" END GLOBAL SYSTEM FUNCTIONS """

if __name__ == "__main__":
    populateDocuments()
