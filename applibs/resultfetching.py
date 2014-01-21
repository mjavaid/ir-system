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
    nominator=0
    denominator=0
    sumOfWij=0
    sumOfWiq=0
    sim=0
    for item in query:
        if item not in uniqueQuery:
            uniqueQuery.append(item)
    tfList=utils.getTokenTF(query)
    for i in range(len(uniqueQuery)):
        print("unique Query:",uniqueQuery[i])
        queryIDF=getQueryIDF(uniqueQuery[i])
        print("QueryIDF: ", queryIDF)
        if not queryIDF == 0:
            print("Query weight: ",queryIDF*(tfList[i]/(max(tfList))))
            print("weight of: ",uniqueQuery[i]," :",getWeight(docNum,item))
            nominator+= (getWeight(docNum,uniqueQuery[i]))*(queryIDF*(tfList[i]/(max(tfList))))
            sumOfWij+=(getWeight(docNum,uniqueQuery[i])*getWeight(docNum,uniqueQuery[i]))
            sumOfWiq+=((queryIDF*(tfList[i]/max(tfList)))*(queryIDF*(tfList[i]/max(tfList))))
    print("Nom:",nominator)
    print("sumWIJ: ", sumOfWij)
    print("sumWIQ: ", sumOfWiq)
    sim= nominator/((sumOfWij*sumOfWiq)**(0.5))
    return sim

if __name__ == "__main__":
    global TABLE_LIST
    addToTable('D0',['new','york','times'])
    addToTable('D1',['new','york','post'])
    addToTable('D2',['los','angeles','times'])
    for token in TABLE_LIST: print(token, " >>", TABLE_LIST[token])
    Qu=['new','new','times']
    print("Simil: ",getSim('D0',Qu))