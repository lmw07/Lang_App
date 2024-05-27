import dbmanager as dbmanager
from sentence import Sentence
import sound_manager

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



'''
Gets sounds for all sentences in database that do not have a filepath associated with their sound field
Returns the number of changes to the database
'''
def get_sounds_for_all_sentences() -> int:
    count = 0
    soundsToAdd = dbmanager.getAllSentenceIds()
    for id in soundsToAdd:
        tup = dbmanager.getSentenceSound(id)
        text = tup[0]
        if tup[1] == "None":
            filePath = sound_manager.get_sound(id, text)
            dbmanager.updateSentenceSound(id, filePath)
            count += 1
            
    return count
