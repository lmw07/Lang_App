import google.generativeai as genai
import app.constants as constants
from app.models.sentence import Sentence

'''
Gets one or more random sentences. Number to get must be between 1 and 10 if provided.
Always returns a list
'''
def getRandomSentences(numberToGet = 1):

  if numberToGet < 1 or numberToGet > 10:
    raise ValueError("Number to get must be between 1 and 10")

  genai.configure(api_key=constants.GOOGLE_GEMINI_API_KEY)
  model = genai.GenerativeModel('gemini-1.5-flash')
  if numberToGet > 1:
    prompt = f'I want you to generate {numberToGet} random Norwegian-English sentence pairs.'
    prompt = prompt + '''I also want a mapping between every word and its translation. 
    The Norwegian sentences should be no longer than 100 characters each. Return the response 
    as a JSON of a list of sentences. Do not use Markdown. Here is an example: {[{"Norwegian_sentence": 
    "Han reparerte gamle møbler som hobby", "English_translation": "He repaired old furniture as a hobby", 
    "Word_mapping": {"Han": "He", "reparerte": "repaired", "gamle": "old", "møbler": "furniture", "som": "as",
      "hobby": "a hobby"}},{"Norwegian_sentence": "De sang sammen på en lokal musikkfestival", 
      "English_translation": "They sang together at a local music festival", "Word_mapping": {"De": "They", 
      "sang": "sang", "sammen": "together", "på": "at", "en": "a", "lokal": "local", "musikkfestival": "music festival"}}]}'''
  else:
    prompt = '''I want you to generate a random Norwegian-English sentence pair. 
    I also want a mapping between every word and its translation. The Norwegian sentence 
    should be no longer than 100 characters. Return the response as a JSON. Do not use Markdown.
      Here is an example: {"Norwegian_sentence": "Hun lærte seg å spille gitar gjennom online kurs",
        "English_translation": "She learned to play the guitar through online courses", "Word_mapping":
          {"Hun": "She", "lærte": "learned", "seg": "herself", "å": "to", "spille": "play", "gitar": "guitar",
            "gjennom": "through", "online": "online", "kurs": "courses"}}'''



  response = model.generate_content(prompt)
  if numberToGet == 1:
    out = Sentence.from_json(response.text)
    return [out]
  out = Sentence.list_from_json(response.text)
  return out


'''
Gets a list of sentences that use specific words
'''
def getSentencesWithSpecificWords(wordList :list, numberToGetPerWord = 5):
  numberToGet = numberToGetPerWord * len(wordList)
  if numberToGetPerWord < 1 or numberToGetPerWord > 10:
    raise ValueError("Number to get must be between 1 and 10")
  genai.configure(api_key=constants.GOOGLE_GEMINI_API_KEY)
  model = genai.GenerativeModel('gemini-1.5-flash')

  prompt = f'I want you to generate {numberToGet} Norwegian-English sentence pairs.'
  prompt = prompt + f'Each norwegian sentence should contain at least 1 of the following words {wordList} but may contain more than one.'
  prompt = prompt + '''I also want a mapping between every word and its translation. 
          The Norwegian sentences should be no longer than 100 characters each. 
          Return the response as a JSON of a list of sentences. Do not use Markdown.
          Here is an example of the format of the output: {[{"Norwegian_sentence": "Han reparerte gamle møbler som hobby", 
          "English_translation": "He repaired old furniture as a hobby", 
          "Word_mapping": {"Han": "He", "reparerte": "repaired", "gamle": "old", "møbler": "furniture", 
          "som": "as", "hobby": "a hobby"}},
          {"Norwegian_sentence": "De sang sammen på en lokal musikkfestival", "English_translation": 
          "They sang together at a local music festival", "Word_mapping": {"De": "They", "sang": "sang", 
          "sammen": "together", "på": "at", "en": "a", "lokal": "local", "musikkfestival": "music festival"}}]}'''
  response = model.generate_content(prompt)
  out = Sentence.list_from_json(response.text)
  return out


  
  
  