import app.services.dbmanager as dbmanager
from app.models.sentence import Sentence
import app.services.sound_manager as sound_manager
import app.services.sentence_generator as sentence_generator
import os
from app.constants import SOUND_PATH

def getSoundFile(sentenceId : int) -> str:
    filename = dbmanager.getSentenceSound(sentenceId)[1]
    # Construct the full path safely using os.path.join
    full_path = os.path.join(SOUND_PATH, filename)
    
    # Normalize the path to correct any forward/backward slash issues
    normalized_path = os.path.normpath(full_path)
    
    return normalized_path

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
    
def getNumberOfKnownSentences():
    return dbmanager.getCountKnownSentences()

def getOneRandomSentenceFromDb():
    out = dbmanager.getRandomSentences(1)
    return out[0]


def getOneKnownSentenceFromDb():
    out = dbmanager.getRandomSentences(1, 'OLD')
    return out[0]

def updateSentenceClass(sentenceId :int, learned : bool):
    dbmanager.updateSentenceClass(sentenceId, learned)



def getSentencesFromWords(wordList : list, numberOfSentencesToGet = 5) -> list:
    #return dbmanager.getRandomSentences(len(wordList) * 5) #PLACEHOLDER
    #for all words in word list check database for 5 sentences that have that word
    #generate the ones you dont have with API call
    out = []
    wordsToGenerate = []
    for word in wordList:
        sentences = dbmanager.getSentencesFromWord(word)
        if len(sentences) < numberOfSentencesToGet:
            wordsToGenerate.append(word)
        else:
            out = out + sentences[:5]
    generatedSentences = None
    if len(wordsToGenerate) > 0:
        generatedSentences = sentence_generator.getSentencesWithSpecificWords(wordsToGenerate, numberOfSentencesToGet)
        for sentence in generatedSentences:
            dbmanager.addSentence(sentence)
    if generatedSentences:
        out = out + generatedSentences
    return out



'''
Gets sounds for all sentences in database that do not have a filepath associated with their sound field
Returns the number of changes to the database
'''
#TODO make more efficient by writing special method in dbmanager
def get_sounds_for_all_sentences() -> int:
    count = 0
    soundsToAdd = dbmanager.getAllSentenceIds()
    for id in soundsToAdd:
        tup = dbmanager.getSentenceSound(id)
        text = tup[0]
        if tup[1] == "None":
            sound_manager.get_sound(id, text)
            dbmanager.updateSentenceSound(id, str(id) + '.mp3')
            count += 1
            
    return count
