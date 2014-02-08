""" utils.py -- Application Utility Functions
# Created: 1/12/14
# Author: Rayan Alsubhi & Muhammad Sajawal Javaid (5933252)
# Last Modified: 1/12/14
"""
from math import log

STOPWORD_FILE = "../resources/StopWords.txt"
DOCUMENTS_FILE = "../resources/Trec_microblog11.txt"
DOCUMENTS_CACHE_FILE = "./resources/cache/documentsCache.json"
TABLE_LIST_CACHE_FILE = "./resources/cache/tableListCache.json"
TWEET_ID = 0
TEXT_INDEX = 2

""" GLOBAL SYSTEM VARIABLES """

STOPWORD_LIST = []
DOCUMENTS = []
TABLE_LIST = {}
TOTAL_DOCS = 0

""" END GLOBAL SYSTEM VARIABLES """

""" GLOBAL SYSTEM FUNCTIONS """

### populateDocuments
# Reads the corpus file and populates the DOCUMENTS list in the IR system
# which will be used for querying.
###
def populateDocuments(documentsFile=None):
    global DOCUMENTS
    if documentsFile == None: input = open(DOCUMENTS_FILE, "r")
    else: input = open(documentsFile, "r")
    docs = (input.read()).split("\n")
    i = 0
    for doc in docs:
        docInfo = doc.partition("\t")
        if docInfo[TEXT_INDEX]:
            docTokens = docInfo[TEXT_INDEX].split(" ")
            DOCUMENTS.append({"D"+str(i):
                {"id": docInfo[TWEET_ID], "text": docInfo[TEXT_INDEX], "tokens": docTokens}
            })
            i += 1
    input.close()

### populateStopWords
# Reads the English stop words file and populates the STOPWORD_LIST
# global variable.
###
def populateStopWords(stopWordFile=None):
    global STOPWORD_LIST
    if stopWordFile == None: input = open(STOPWORD_FILE, "r")
    else: input = open(stopWordFile, "r")
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

### getTotalDocuments
# Returns the total number of documents in the corpus.
###
def getTotalDocuments():
    global DOCUMENTS
    return len(DOCUMENTS)

### addToTable
# add the tokens from the token array to the table and update df and the linked list
# param: docNum, token
###
def addToTable(docNum=None,tokens=None,useCache=False):
    global TOTAL_DOCS,TABLE_LIST, TABLE_LIST_CACHE_FILE
    
    if useCache:
        print("CACHE DATA GALORE")
        cacheData = open(TABLE_LIST_CACHE_FILE).read()
        TABLE_LIST = json.loads(cacheData)
        return
    
    TOTAL_DOCS+=1
    FOUND = False
    for token in tokens:
        # Check if the token is already in the list
        if token in TABLE_LIST:
            # Check if the document number is already in the list
            index = 0
            for i in TABLE_LIST[token]['doc']:
                if docNum in i:
                    # increment the tf
                    TABLE_LIST[token]['doc'][index][docNum]+=1
                    FOUND = True
                index+=1
            if not FOUND:
                # If not, add the document number to the list and initialize it to 1, also increment df
                TABLE_LIST[token]['doc'].append({docNum:1})
                TABLE_LIST[token]['df']+=1
        else:
            # If Token is not in the dictionary, add it and initialize both df and occurence to 1
            TABLE_LIST[token]={'df':1,'doc':[{docNum :1}]}

def populateTable():
    global TABLE_LIST
    cacheData = open(TABLE_LIST_CACHE_FILE).read()
    TABLE_LIST = json.loads(cacheData)

### normalizeTFValues
# normalize tf for each token by dividing the tf by the maximum occurance in a document
###
def normalizeTFValues():
    global TABLE_LIST
    for token in TABLE_LIST:
        #get the tf values in all documents for the specified token
        tf_list = [(list(i.values()))[0] for i in TABLE_LIST[token]['doc']]
        # get the maximum value of tf
        max_tf = max(tf_list)
        # now divide each value by the maximum value of tf
        index = 0
        for i in (TABLE_LIST[token]['doc']):
            key = (list(i.keys()))[0] #each doc has only one item so we use [0]
            value = (list(i.values()))[0]
            TABLE_LIST[token]['doc'][index][key] = value / max_tf
            index += 1
        
### getWeight
# get the weighted total for a given word in the table for a given document
# param: docNum, token
#
###
def getWeight(docNum,token):
    global TABLE_LIST
    # w_ij = tf_ij x idf_i
    index = 0
    tf = 0
    for i in TABLE_LIST[token]['doc']:
        if docNum in i:
            # increment the tf
            tf = TABLE_LIST[token]['doc'][index][docNum]
            break
        else:
            index +=1
    result = (tf*TABLE_LIST[token]['idf'])
    return result

### getIDFForToken
# returns the idf of a given query
# param: token
###
def getIDFForToken(token):
    global TABLE_LIST
    if token in TABLE_LIST:
        return TABLE_LIST[token]['idf']
    else:
         return 0
    
### calculateIDFValues
# calculates IDF for all words in the index
#
###
def calculateIDFValues():
    global TABLE_LIST, TOTAL_DOCS
    for token in TABLE_LIST:
        idf = log(( TOTAL_DOCS / (TABLE_LIST[token]['df']) ), 2)
        TABLE_LIST[token]['idf'] = idf


### getTableList
#    returns the table List
#
###
def getTableList():
    return TABLE_LIST
    
""" END GLOBAL SYSTEM FUNCTIONS """

if __name__ == "__main__":
    #populateDocuments()
    #populateStopWords()
    #print(DOCUMENTS)
    #print(STOPWORD_LIST)
    addToTable('D0',['new','york','times'])
    addToTable('D1',['new','york','post'])
    addToTable('D2',['los','angeles','times'])
    table_test = getTableList()
    for token in table_test: print(token, " >>", table_test[token])
    Qu=['new','new','times']
    print(" ")