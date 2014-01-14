""" indexing.py -- Data Indexing Functions
# Created: 1/12/14
# Author: Rayan Alsubhi(5461886)
# Last Modified: 1/12/14
"""

#declare a TABLE_LIST That holds tokens with their df and tf
TABLE_LIST={}

### addToTable
# add the tokens from the token array to the table and update df and the linked list
# param: docNum, token
###
def addToTable(docNum,tokenArr):
    for token in tokenArr:  
        # Check if the token is already in the list
        if token in TABLE_LIST:
            # If True, increment df
            TABLE_LIST[token]['df']+=1
            # Check if the document number is already in the list
            
            index = 0
            for i in TABLE_LIST[token]['doc']:
                if docNum in i:
                    # increment the tf
                    TABLE_LIST[token]['doc'][index][docNum]+=1
                else:
                    # If not, add the document number to the list and initialize it to 1
                    TABLE_LIST[token]['doc'].append({docNum:1})
                    break
                index+=1
        else:
            # If Token is not in the dictionary, add it and initialize both df and occurence to 1
            TABLE_LIST[token]={'df':1,'doc':[{docNum :1}]}
        
if __name__ == "__main__":
    addToTable('D0',['game','bad','bad'])
    addToTable('D1',['game','home','bad'])
    for token in TABLE_LIST: print(token, " >>", TABLE_LIST[token])
