""" preprocessing.py -- Document Preprocessing Functions
# Created: 1/12/14
# Author: Muhammad Sajawal Javaid (5933252)
# Last Modified: 1/12/14
"""

from utils import STOPWORD_LIST, DOCUMENTS
from exlibraries.porter2 import stem
import re
# Temporarily imported for the main method
from utils import populateDocuments, populateStopWords
# Temporarily imported for execution testing
import time
from sre_constants import error


### filterStopWordsFromDocs
# Filters out the stop words from the documents in the corpus.
###
def filterDocs():
    for doc in range(len(DOCUMENTS)):
        DOCUMENTS[doc]["D"+str(doc)]['text'] = filterData(DOCUMENTS[doc]["D"+str(doc)]['text'])

### filterQuery
# param:
#   query -
#
# Filters a query before it is executed.
###
def filterQuery(query):
    return filterData(query)

### filterData
# param:
#   data -
#
# A generic filter function that is used as a helper for other functions.
###
def filterData(data):
    global STOPWORD_LIST
    result = data
    words = result.split(" ")
    for word in words:
        if word in STOPWORD_LIST:
            result = re.sub("\s\s+", " ", re.sub("\\b"+word+"\\b", '', result))
            continue
        try:
            stemmedWord = stemWord(word)
            result = re.sub("\\b"+word+"\\b", stemmedWord, result)
        except IndexError:
            pass
        except error:
            pass
    return result

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
