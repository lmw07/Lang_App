import datafiles.dbmanager as dbmanager


def getSoundFile(sentenceId : int) -> str:
    return dbmanager.getSentenceSound(sentenceId)[1]

def getRandomSentencesFromDb(numberToGet : int) ->list:
    return dbmanager.getSentences(numberToGet)
