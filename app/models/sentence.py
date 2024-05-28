import json

class Sentence:
    def __init__(self, norwegian, english, word_map, id = None):
        """
        Initializes the Sentence object with Norwegian sentence, English translation,
        and a dictionary of word mappings from Norwegian to English.
        """
        self.norwegian = norwegian
        self.english = english
        self.word_map = word_map
        self.id = id

    @classmethod
    def from_json(cls, json_str):
        """
        Class method to instantiate from a JSON string.
        :param json_str: JSON string containing norwegian, english, and word_mapping.
        :return: Sentence object
        """
        try:
            data = json.loads(json_str)
            return cls(data['Norwegian_sentence'], data['English_translation'], data['Word_mapping'])
        except json.decoder.JSONDecodeError as e:
            print(e.msg)
            print(json_str)

    @classmethod
    def list_from_json(cls, json_str):
        """
        Class method to create a list of Sentence objects from a JSON string
        containing multiple Sentence data.
        :param json_str: JSON string containing an array of Sentence data.
        :return: List of Sentence objects
        """
        try:
            sentences = json.loads(json_str)
            return [cls(s['Norwegian_sentence'], s['English_translation'], s['Word_mapping']) for s in sentences]
        except json.decoder.JSONDecodeError as e:
            print(e.msg)
            print(json_str)