""" preprocessing.py -- Document Preprocessing Functions
# Created: 1/12/14
# Author: Muhammad Sajawal Javaid (5933252)
# Last Modified: 1/12/14
"""

from utils import STOPWORD_LIST, DOCUMENTS
from utils import populateDocuments, populateStopWords

### filterStopWordsFromDocs
# Filters out the stop words from the documents in the corpus.
###
def filterStopWordsFromDocs():
    #global STOPWORD_LIST, DOCUMENTS
    i = 0
    for doc in range(len(DOCUMENTS)):
        for stopword in STOPWORD_LIST:
            if stopword in DOCUMENTS[doc]["D"+str(i)]['text']:
                DOCUMENTS[doc]["D"+str(i)]['text'].remove(stopword)
        i += 1

if __name__ == "__main__":
    populateStopWords()
    populateDocuments()
    print(len(STOPWORD_LIST))
    print(DOCUMENTS[0]['D0']['text'])
    filterStopWordsFromDocs()
    print(DOCUMENTS[0]['D0']['text'])
