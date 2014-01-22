""" indexing.py -- Data Indexing Functions
# Created: 1/12/14
# Author: Rayan Alsubhi(5461886)
# Last Modified: 1/12/14
"""

from math import log
from utils import getTotalDocuments
#import utils
#declare a TABLE_LIST That holds tokens with their df and tf
TABLE_LIST={}
TOTAL_DOCS = 0

### addToTable
# add the tokens from the token array to the table and update df and the linked list
# param: docNum, token
###
def addToTable(docNum,tokens):
    global TOTAL_DOCS,TABLE_LIST
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
        else:
            index +=1
    result = (tf*TABLE_LIST[token]['idf'])
    return result

### getQueryIDF
# returns the idf of a given query
# param: query
###
def getQueryIDF(query):
    global TABLE_LIST
    print("\nTABLE_LIST:\n",TABLE_LIST,"\n")
    if query in TABLE_LIST:
        return TABLE_LIST[query]['idf']
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
    
        
if __name__ == "__main__":
    '''addToTable('D0',['game','bad','bad'])
    for token in TABLE_LIST: print(token, " >>", TABLE_LIST[token])
    addToTable('D1',['game','home','bad'])
    for token in TABLE_LIST: print(token, " >>", TABLE_LIST[token])
    print(TOTAL_DOCS)
    print(TABLE_LIST)
    for token in TABLE_LIST:
        
        normalizeTF(token)
    for token in TABLE_LIST: print(token, " >>", TABLE_LIST[token])
    print(getWeight('D1','home'))
    addToTable('D0',['new','york','times'])
    addToTable('D1',['new','york','post'])
    addToTable('D2',['los','angeles','times'])
    for token in TABLE_LIST: print(token, " >>", TABLE_LIST[token])
    Qu=['new','new','times']
    print(resultfetching.getSim('D0',Qu))'''
    
    
