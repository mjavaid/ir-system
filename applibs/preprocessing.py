""" preprocessing.py -- Document Preprocessing Functions
# Created: 1/12/14
# Author: Muhammad Sajawal Javaid (5933252)
# Last Modified: 1/12/14
"""

from utils import STOPWORD_LIST, DOCUMENTS
from exlibraries.porter2 import stem
# Temporarily imported for the main method
from utils import populateDocuments, populateStopWords
# Temporarily imported for execution testing
import time


### filterStopWordsFromDocs
# Filters out the stop words from the documents in the corpus.
###
def filterDocs():
    for doc in range(len(DOCUMENTS)):
        words = DOCUMENTS[doc]["D"+str(doc)]['text'].split(" ")
        for word in words:
            try:
                stemmedWord = stemWord(word)
                DOCUMENTS[doc]["D"+str(doc)]['text'] = DOCUMENTS[doc]["D"+str(doc)]['text'].replace(" "+word+" ", " "+stemmedWord+" ")
            except IndexError:
                pass
            if word in STOPWORD_LIST:
                DOCUMENTS[doc]["D"+str(doc)]['text'] = DOCUMENTS[doc]["D"+str(doc)]['text'].replace(" "+word+" ", " ")

### stemWord
# param:
#   word -
#
# Stems a provided word using the Porter2 stemming algorithm.
###
def stemWord(word):
    return stem(word)

if __name__ == "__main__":
    start_time = time.time()
    populateStopWords()
    print("Stop Word Population Execution Time:", time.time() - start_time)
    populateDocuments()
    print("Document Population Execution Time:", time.time() - start_time)
    print(DOCUMENTS[0]["D0"]['text'])
    filterDocs()
    print(DOCUMENTS[0]["D0"]['text'])
    print("Filter Documents:", time.time() - start_time)
