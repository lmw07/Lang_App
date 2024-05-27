


'''
Generates an mp3 of a Norwegian sentence with 1 of 4 randomly chosen voices.
'''
def __synthesize_sound_with_google__(text, id : int):
    """Synthesizes speech from the input string of text."""
    from google.cloud import texttospeech
    import random
    #male voice, female voice, female voice, male voice
    voiceList = ["nb-NO-Wavenet-D", "nb-NO-Wavenet-E", "nb-NO-Wavenet-C", "nb-NO-Wavenet-B"]
    voice = random.choice(voiceList)
    


    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(
        language_code="nb-NO",
        name=voice,
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )


    filename = "speechfiles/" + str(id) + ".mp3"
    # The response's audio_content is binary.
    with open(filename, "wb") as out:
        out.write(response.audio_content)
        #print('Audio content written to file "output.mp3"')



def __check_for_sound_in_folder__(id : int) -> bool:
 
    import os
    filename = str(id) + ".mp3"
    for root, dirs, files in os.walk("speechfiles"):
        if filename in files:
            return True
    return False
   
'''
Checks for presence of sound file database. If not found,
creates one.
Returns path to file.
'''
def get_sound(id : int, sentenceText :str) -> bool:
    pathToFile = "speechfiles/" + str(id) + ".mp3"
    if __check_for_sound_in_folder__(id):
        return pathToFile
    else: 
        __synthesize_sound_with_google__(sentenceText, id)
        return pathToFile




