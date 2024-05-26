import datafiles.dbmanager as dbmanager


def getSoundFile(sentenceId : int) -> str:
    return dbmanager.getSentenceSound(sentenceId)[1]

def getMultipleRandomSentencesFromDb(numberToGet : int) ->list:
    return dbmanager.getSentences(numberToGet)

def getOneRandomSentenceFromDb():
    out = dbmanager.getSentences(2)
    return out[0]

#TODO fix so always returns a known sentence
def getOneKnownSentenceFromDb():
    out = dbmanager.getSentences(2)
    return out[0]

def updateSentenceClass(sentenceId :int, learned : bool):
    dbmanager.updateSentenceClass(sentenceId, learned)

#TODO fix
def getSentencesFromWords(wordList) :
    return dbmanager.getSentences(len(wordList) * 5) #PLACEHOLDER
    #for all words in word list check database for 5 sentences that have that word
    #generate the ones you dont have with API call
