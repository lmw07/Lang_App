# Introduction
This is a personal project I built to help myself learn Norwegian. I was dissatisfied with current free offerings  
and so I wanted to build a lightweight language-learning application for Windows that I could use to bolster my  
 language skills, particularly my listening skills.

## Tools Used
This project currently uses SQLite to manage a database of sentences and words. It uses PyQT5 for the GUI, and  
Google's text-to-speech AI API to generate audio files for each sentence. It uses Google's Gemini API to generate   
sentences on demand. It is currently written entirely in Python.

## User Manual
The application has 3 modes. Mode selection is available from the startup page and from the menubar at the top of the GUI.  
The startup page also displays the number of sentences that the user has learned.    

### Regular Mode
Regular mode incorporates both listening and reading. On startup, a list of random sentences is retrieved from the database.   
By default, the size of the retrieved set is 20 and it is 25% learned sentences and 75% novel or unlearned sentences. These  
settings can be modified in the constants or settings file. There are two progress buttons, one to indicate that you knew the   
sentence and one to indicate that you didn't. These update the 'learned' status of the word in the dictionary as well as progressing  
the application forward. If you want to see the definition of the whole sentence, you can click the 'translate' button. Conversely,  
to see the definition of a single word, you can click on that word in the original sentence.

### Listening Mode
Listening mode plays the sound of the sentence before showing the text of the sentence. The 'learned' status of the sentence  
is not affected in listening mode. It only picks sentences that are marked 'learned'. 

### Targeted Mode
In targeted mode, the user can click on words that they don't know. This will add these words to a queue displayed at the  
bottom of the page. If this queue has words in it when 'continue' is clicked, the sentence is updated to "not learned".  
The converse is also true. Words in the queue are used to generate the next sentences to display. By default, for every  
word that the user does not know, 5 sentences containing that word are generated. Ideally, these are pulled from the   
database, but if enough suitable sentences cannot be found in the database then they are generated with AI.

## Known Issues
 - Some sentences have English to Norwegian word mappings that are incorrect or have incorrect sounds  
 associated with them. This occurs because AI has trouble associating some words (e.g. 'i gar' is two  
words but it maps to the English word "yesterday"). These should be expunged. 
- Sentences that are too long can crash the GUI. This is currently solved by limiting the length of the sentences  
generated by AI.

## Planned improvements
- Addition of a button to report incorrect sentences and sounds. This would trigger the deletion and regeneration  
of the offending item.
- Addition of an ANKI-style spaced repetition mode. This would require each sentence to have information about the  
last time it was viewed stored for retrieval.
- Inclusion of sound in targeted mode. Currently, targeted mode has no sound since sound is generated separately  
from sentence text.