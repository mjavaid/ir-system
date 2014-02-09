from utils import populateStopWords, populateDocuments
from preprocessing import filterDocs
from indexing import calculateIDFValues, normalizeTFValues

def initialize(STOPWORD_FILE=None, DOCUMENTS_FILE=None, useCache=False):
    print("Populating StopWords...")
    populateStopWords(STOPWORD_FILE)
    print("Done.")
    
    print("Populating Documents...")
    populateDocuments(DOCUMENTS_FILE)
    print("Done.")
    
    print("Filtering Documents...")
    filterDocs(useCache)
    print("Done.")
    
    if not useCache:
        print("Calculating IDF Values...")
        calculateIDFValues()
        print("Done.")
    
    if not useCache:
        print("Normalizing TF Values...")
        normalizeTFValues()
        print("Done.")
