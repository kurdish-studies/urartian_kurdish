#  Hurro-Urartian-Kurdish from the lexicostatistical viewpoint.
import pandas as pd

from data.data_loader import load_data
from generator import generate_df, export_to_markdown, export_to_json
from preprocessor.preprocessor import extract_note_from_text


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
        for param in self.get_params():
            if type(self.__getattribute__(param)) == list:
                temp_dict = {}
                for i, item in enumerate(self.__getattribute__(param)):
                    temp_dict.update({i: item})
                self.__setattr__(param, temp_dict)

        doc = {
            "src_lang": self.src_lang,
            "word": self.word,
            "glossary": self.glossary,
            "kurdish_word": self.ku_word,
            "kurdish_glossary": self.kurdish_glossary,
            "regular_sound_changes": self.regular_sound_changes,
            "sporadic_sound_changes": self.sporadic_sound_changes,
            "notes": self.notes
        }
        return doc

    def __call__(self, *args, **kwargs):
        return self.build_dict()

    def __str__(self):
        string_doc = self.build_dict().__str__()
        return string_doc


if __name__ == '__main__':
    main_headers = ["Urartian", "Kurdish", "Hurrian", "Kassite", "Armenian"]
    langs = [item.lower() for item in main_headers]
    sub_headers = ["word", "glossary", "notes"]
    # langs = ["urartian", "kurdish"]
    url = "http://landofkarda.blogspot.com/2011/04/hurro-urartian-substratum-in-kurdish-2.html"

    mux = pd.MultiIndex.from_product([main_headers, sub_headers])
    raw_file = load_data(url, from_url=False)
    # word_dict = export_to(raw_file, langs, to_format="dataframe")
    word_dict = generate_df(raw_file, langs=langs, sub_columns=sub_headers)
    dataframe = pd.DataFrame.from_dict(word_dict, orient='index', columns=mux)
    dataframe.fillna("", inplace=True)
    print(dataframe.head().columns)
    print(80 * '-')
    ur = zip(dataframe['Urartian']['word'], dataframe['Urartian']['glossary'])
    ku = zip(dataframe['Kurdish']['word'], dataframe['Kurdish']['glossary'], dataframe['Kurdish']['notes'])
    ur_ku = zip(ur, ku)
    bidict = {}
    template_doc = {
        "src_lang": "",
        "word": "",
        "glossary": "",
        "ku": ""
    }
    for i, item in enumerate(ur_ku):
        src_lang = item[0]
        tgt_lang = item[1]
        if src_lang[0] and src_lang[1]:
            print(i, src_lang, tgt_lang)

    word = WordTemplate("urartian", "ale", ["he says", "she says"], ["ale", "ئەڵێ"], "he says")()
    print(word)
    # todo: Export json files for the following tables:
    #  Urartian-Kurdish, Hurro-Kurdish, Kasso-Kurdish, and the remaining armenian with all other languages
    #  Also Create
    #  Also use this link: https://glosbe.com/xur/en/qapqar%C5%A1
    # export_to_json(dataframe)
    # export_to_html(dataframe)
    # text = "land, country, field, cf. kurdawari, کوردەواری / warê me وارێ مە armenian agarak has been suggested as an armenian loan from 'awari'. kurdish has even 'garak' with the same meaning"
    # text2 = "build cf, kurdish d>nil"
    # print(extract_note_from_text(text, 'cf'))
    # print(extract_note_from_text(text2, 'cf'))
    export_to_markdown(dataframe, file_name="export.md")
    print(zip(dataframe['Urartian']))
