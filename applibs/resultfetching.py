""" resultfetching.py -- Query & Result Handling Functions
# Created: 1/12/14
# Author: Rayan Alsubhi & Muhammad Sajawal Javaid (5933252)
# Last Modified: 1/12/14
"""

import utils
from indexing import *

### getSim
# returns the similarity between a given document and a query using the cosine similarity
# param: docNum, query
###
def getSim(docNum, query):
    global TABLE_LIST
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

if __name__ == "__main__":
    global TABLE_LIST
    addToTable('D0',['new','york','times'])
    addToTable('D1',['new','york','post'])
    addToTable('D2',['los','angeles','times'])
    normalizeTFValues()
    calculateIDFValues()
    print("\n\n------------------\n\n")
    print("RESULTFETCHING::TABLE_LIST:",TABLE_LIST)
    print("\n\n------------------\n\n")
    Qu=['new','times']
    simResults = []
    simResults.append({"doc": "D0", "score": getSim('D0',Qu)})
    simResults.append({"doc": "D1", "score": getSim('D1',Qu)})
    simResults.append({"doc": "D2", "score": getSim('D2',Qu)})
    print("RESULTS:", simResults,"\n")
