""" preprocessing.py -- Document Preprocessing Functions
# Created: 1/12/14
# Author: Muhammad Sajawal Javaid (5933252)
# Last Modified: 1/12/14
"""

from exlibraries.porter2 import stem
import sys, os, json

from indexing import addToTable

from utils import DOCUMENTS_CACHE_FILE, TABLE_LIST_CACHE_FILE, STOPWORD_LIST, DOCUMENTS
import utils
from sre_constants import error


### filterStopWordsFromDocs
# Filters out the stop words from the documents in the corpus.
###
def filterDocs(useCache=False):
    global DOCUMENTS, TABLE_LIST
    if(not (useCache and os.path.exists(DOCUMENTS_CACHE_FILE))):
        useCache = False
    if useCache:
        cacheData = open(DOCUMENTS_CACHE_FILE).read()
        DOCUMENTS = json.loads(cacheData)
        cacheData = open(TABLE_LIST_CACHE_FILE).read()
        utils.TABLE_LIST = json.loads(cacheData)
        print(len(utils.TABLE_LIST))
    else:
        for doc in range(len(DOCUMENTS)):
            DOCUMENTS[doc]["D"+str(doc)]['tokens'] = filterData(DOCUMENTS[doc]["D"+str(doc)]['tokens'])
            addToTable("D"+str(doc), DOCUMENTS[doc]["D"+str(doc)]['tokens'])
            sys.stdout.write("\r{0} of {1} documents filtered...".format(doc+1, len(DOCUMENTS)))
            sys.stdout.flush()

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
def filterData(tokens):
    global STOPWORD_LIST
    result = tokens.copy()
    for token in tokens:
        if token in STOPWORD_LIST:
            result.remove(token)
            continue
        try:
            stemmedToken = stemToken(token)
            result.remove(token)
            result.append(stemmedToken)
        except IndexError:
            pass
        except error:
            pass
    result = [word.lower() for word in result]
    return result

### stemWord
# param:
#   word -
#
# Stems a provided word using the Porter2 stemming algorithm.
###
def stemToken(token):
    return stem(token)

if __name__ == "__main__":
    """start_time = time.time()
    populateStopWords()
    print("Stop Word Population Execution Time:", time.time() - start_time)
    populateDocuments()
    print("Document Population Execution Time:", time.time() - start_time)
    print(DOCUMENTS[0]["D0"]['text'])
    filterDocs()
    print(DOCUMENTS[0]["D0"]['text'])
    print("Filter Documents:", time.time() - start_time)"""
