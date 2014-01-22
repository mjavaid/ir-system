from utils import populateStopWords, populateDocuments
from preprocessing import filterDocs
from indexing import calculateIDFValues, normalizeTFValues

def initialize(STOPWORD_FILE=None, DOCUMENTS_FILE=None):
    print("Populating StopWords...")
    populateStopWords(STOPWORD_FILE)
    print("Done.")
    
    print("Populating Documents...")
    populateDocuments(DOCUMENTS_FILE)
    print("Done.")
    
    print("Filtering Documents...")
    filterDocs()
    print("Done.")
    
    print("Calculating IDF Values...")
    calculateIDFValues()
    print("Done.")
    
    print("Normalizing TF Values...")
    normalizeTFValues()
    print("Done.")
