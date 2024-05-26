import datafiles.dbmanager as dbmanager


def getSoundFile(sentenceId : int) -> str:
    return dbmanager.getSentenceSound(sentenceId)[1]
