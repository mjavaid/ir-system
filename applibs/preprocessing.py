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
        for word in DOCUMENTS[doc]["D"+str(doc)]['text']:
            try:
                stemmedWord = stemWord(word)
                DOCUMENTS[doc]["D"+str(doc)]['text'].remove(word)
            except IndexError:
                print(doc)
                stemmedWord = word
            DOCUMENTS[doc]["D"+str(doc)]['text'].append(stemmedWord)
        for stopword in STOPWORD_LIST:
            if stopword in DOCUMENTS[doc]["D"+str(doc)]['text']:
                DOCUMENTS[doc]["D"+str(doc)]['text'].remove(stopword)

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
    print(DOCUMENTS[39813]["D39813"]['text'])
    filterDocs()
    print(DOCUMENTS[39813]["D39813"]['text'])
    print("Filter Documents:", time.time() - start_time)
