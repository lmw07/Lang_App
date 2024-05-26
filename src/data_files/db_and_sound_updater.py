import dbmanager
import sound_manager

dbmanager.add_sentences_from_file("sentences_to_add.txt")
count = sound_manager.get_sounds_for_all_sentences()
print(count)