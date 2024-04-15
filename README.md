# Introduction
This is a personal project I built to help myself learn Norwegian. I was dissatisfied with current free offerings, and so I wanted to build a lightweight language-learning
application for windows that I could use to bolster my language skills, particularly my listening skills.

## Tools Used
This project currently uses SQLite to manage a database of sentences and words. It uses PyQT5 for the GUI, and Google's text-to-speech AI API to generate audio files for each sentence. It is currently written entirely in Python.

## User Manual
When main.py is ran, a random set of sentences is collected from the database. The GUI will display the a randomly picked Norwegian sentence. Each word of the sentence is clickable to reveal the english
translation of that word. Clicking on the translate button reveals the translation for the whole sentence. If the user feels that they knew the sentence, they should click on the green button. 
This causes the sentence to be removed from the current set of working sentences and its database entry is updated to reflect that the user knows it. If the user did not know the sentence, they
should click on the red button, which replaces the sentence with a new one from the working set without removing it.
The "play sound" button plays an AI generated sound file of the norwegian sentence.

## Known Issues
Some of the old sentences have English to Norwegian word mappings that are incorrect. These should be expunged.

## Planned improvements
I would like to make a listening mode, where the user is first exposed only to the sound of the sentence. 
Currently, sound files cannot be generated in the application. This is partially deliberate, as it prevents the user from spamming Google's TTS API and running up charges. In the future,
I would like to include the option to generate and add sentences and their sound files to the database through the GUI.
