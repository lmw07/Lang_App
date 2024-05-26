import datafiles.dbmanager as dbmanager


def getSoundFile(sentenceId : int) -> str:
    return dbmanager.getSentenceSound(sentenceId)[1]

def getMultipleRandomSentencesFromDb(numberToGet : int, oldFraction = 0) ->list:
    if oldFraction > 1 or oldFraction < 0:
        raise ValueError("oldFraction must be between 0 and 1")
    numberOld = oldFraction * numberToGet
    numberNew = numberToGet - numberOld
    outNew = dbmanager.getRandomSentences(numberNew, 'NEW')
    outOld = dbmanager.getRandomSentences(numberOld, 'OLD')
    if outNew and outOld:
        return outOld + outNew
    if outNew and not outOld:
        return outNew
    if outOld and not outNew:
        return outOld

def getOneRandomSentenceFromDb():
    out = dbmanager.getRandomSentences(1)
    return out[0]


def getOneKnownSentenceFromDb():
    out = dbmanager.getRandomSentences(1, 'OLD')
    return out[0]

def updateSentenceClass(sentenceId :int, learned : bool):
    dbmanager.updateSentenceClass(sentenceId, learned)

#TODO fix
def getSentencesFromWords(wordList) :
    return dbmanager.getRandomSentences(len(wordList) * 5) #PLACEHOLDER
    #for all words in word list check database for 5 sentences that have that word
    #generate the ones you dont have with API call
