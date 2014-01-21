""" utils.py -- Application Utility Functions
# Created: 1/12/14
# Author: Rayan Alsubhi & Muhammad Sajawal Javaid (5933252)
# Last Modified: 1/12/14
"""

STOPWORD_FILE = "../resources/StopWords.txt"
DOCUMENTS_FILE = "../resources/Trec_microblog11.txt"
TWEET_ID = 0
TEXT_INDEX = 2

""" GLOBAL SYSTEM VARIABLES """

STOPWORD_LIST = []
DOCUMENTS = []

""" END GLOBAL SYSTEM VARIABLES """

""" GLOBAL SYSTEM FUNCTIONS """

### populateDocuments
# Reads the corpus file and populates the DOCUMENTS list in the IR system
# which will be used for querying.
###
def populateDocuments():
    global DOCUMENTS
    input = open(DOCUMENTS_FILE, "r")
    docs = (input.read()).split("\n")
    i = 0
    for doc in docs:
        docInfo = doc.partition("\t")
        if docInfo[TEXT_INDEX]:
            DOCUMENTS.append({"D"+str(i):{"id": docInfo[TWEET_ID], "text": docInfo[TEXT_INDEX]}})
            i += 1
    input.close()

### populateStopWords
# Reads the English stop words file and populates the STOPWORD_LIST
# global variable.
###
def populateStopWords():
    global STOPWORD_LIST
    input = open(STOPWORD_FILE, "r")
    stopwords = (input.read()).split("\n")
    for stopword in stopwords:
        if stopword != "": STOPWORD_LIST.append(stopword)
    input.close()

### geTtokenTF
# returns the a list of tf for tokens in the query
# It will return a list of occurances, and it checks for duplicates
###
def getTokenTF(query):
    count = []
    uniqueQuery = []
    for item in query:
        if item not in uniqueQuery:
            uniqueQuery.append(item)
            count.append(query.count(item))
    return count
    
""" END GLOBAL SYSTEM FUNCTIONS """

if __name__ == "__main__":
    #populateDocuments()
    #populateStopWords()
    #print(DOCUMENTS)
    #print(STOPWORD_LIST)
    print(" ")