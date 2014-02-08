""" resultfetching.py -- Query & Result Handling Functions
# Created: 1/12/14
# Author: Rayan Alsubhi & Muhammad Sajawal Javaid (5933252)
# Last Modified: 1/12/14
"""

print("in resultfetching")

import utils
#from utils import TABLE_LIST
#from indexing import *
from utils import *
### getSim
# returns the similarity between a given document and a query using the cosine similarity
# param: docNum, query
###
def getSim(docNum, query):
    #global TABLE_LIST
    uniqueQuery= []
    numerator, denominator, sumOfWij, sumOfWiq, sim = 0.0, 0, 0, 0, 0
    for item in query:
        if item not in uniqueQuery:
            uniqueQuery.append(item)
    tfList=utils.getTokenTF(query)
    for i in range(len(uniqueQuery)):
        tokenIDF=getIDFForToken(uniqueQuery[i])
        if not tokenIDF == 0:
            docTokenWeight = getWeight(docNum,uniqueQuery[i])
            queryTokenWeight = tokenIDF * (0.5 + (0.5 * ( tfList[i] / (max(tfList)) )))
            numerator += docTokenWeight * queryTokenWeight
            sumOfWij += docTokenWeight * docTokenWeight
            sumOfWiq += queryTokenWeight * queryTokenWeight
    denominator = ( sumOfWij * sumOfWiq ) ** (0.5)
    if not denominator == 0: sim = numerator / denominator
    return sim

### getDocsForTokens
# Returns all the documents for the list of tokens.
###
def getDocsForTokens(tokens):
    #global TABLE_LIST
    table = utils.getTableList()
    #print(table, " || ", tokens)
    docs = []
    for token in tokens:
        if token in table:
            for doc in table[token]['doc']:
                docs.append((list(doc.keys()))[0])
    return docs

if __name__ == "__main__":
    
    utils.addToTable('D0',['new','york','times'])
    utils.addToTable('D1',['new','york','post'])
    utils.addToTable('D2',['los','angeles','times'])
    utils.normalizeTFValues()
    utils.calculateIDFValues()
    print("\n\n------------------\n\n")
    print("RESULTFETCHING::TABLE_LIST:",utils.getTableList())
    print("\n\n------------------\n\n")
    Qu=['new','times']
    simResults = []
    simResults.append({"doc": "D0", "score": getSim('D0',Qu)})
    simResults.append({"doc": "D1", "score": getSim('D1',Qu)})
    simResults.append({"doc": "D2", "score": getSim('D2',Qu)})
    print("RESULTS:", simResults,"\n")
    print(getDocsForTokens(['times']))
