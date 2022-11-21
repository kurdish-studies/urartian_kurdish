class WordTemplate:
    def __init__(self, src_lang, word, glossary, ku_word, kurdish_glossary, regular_sound_changes="",
                 sporadic_sound_changes="", notes=""):
        self.src_lang = src_lang
        self.word = word
        self.glossary = glossary
        self.ku_word = ku_word
        self.kurdish_glossary = kurdish_glossary
        self.regular_sound_changes = regular_sound_changes
        self.sporadic_sound_changes = sporadic_sound_changes
        self.notes = notes

    def get_params(self):
        return self.__dict__.keys()

    def build_dict(self):

        # convert lists to dictionaries
        for param in self.get_params():
            temp_dict = {}
            retrieved_param = self.__getattribute__(param)
            if type(retrieved_param) == list:
                for i, item in enumerate(self.__getattribute__(param)):
                    temp_dict.update({i: str(item).lower()})
            elif type(retrieved_param) == str:
                if retrieved_param:
                    temp_dict.update({0: str(self.__getattribute__(param)).lower()})

                else:
                    temp_dict.update({})
            self.__setattr__(param, temp_dict)

        doc = {
            "src_lang": str(self.src_lang).lower(),
            "word": str(self.word).lower(),
            "glossary": str(self.glossary).lower(),
            "kurdish_word": str(self.ku_word).lower(),
            "kurdish_glossary": str(self.kurdish_glossary).lower(),
            "regular_sound_changes": str(self.regular_sound_changes).lower(),
            "sporadic_sound_changes": str(self.sporadic_sound_changes).lower(),
            "notes": str(self.notes).lower()
        }
        return doc

    def __call__(self, *args, **kwargs):
        return self.build_dict()

    def __str__(self):
        string_doc = self.build_dict().__str__()
        return string_doc

