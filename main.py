#  Hurro-Urartian-Kurdish from the lexicostatistical viewpoint.
import json

import pandas as pd

from data.data_loader import load_data
from generator import generate_df, export_to_markdown, export_to_json
from utils.templates import WordTemplate

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

    TARGET_LANGUAGE = "Kurdish"
    for language in main_headers:
        if not language == TARGET_LANGUAGE:
            print(language)
            src_language = zip(dataframe[language]['word'], dataframe[language]['glossary'])
            tgt_language = zip(dataframe[TARGET_LANGUAGE]['word'], dataframe[TARGET_LANGUAGE]['glossary'],
                               dataframe[TARGET_LANGUAGE]['notes'])
    ur = zip(dataframe['Urartian']['word'], dataframe['Urartian']['glossary'])
    ku = zip(dataframe['Kurdish']['word'], dataframe['Kurdish']['glossary'], dataframe['Kurdish']['notes'])
    ur_ku = zip(ur, ku)
    lang_dict = {}
    index = 0
    for i, item in enumerate(ur_ku):
        src_lang = item[0]
        tgt_lang = item[1]
        if src_lang[0] and src_lang[1]:
            word = WordTemplate("urartian", src_lang[0], src_lang[1], tgt_lang[0], tgt_lang[1], notes=tgt_lang[2])()
            lang_dict.update({index: word})
            index += 1
    export_to_json(lang_dict)
    word = WordTemplate("urartian", "ale", ["he says", "she says"], ["ale", "ئەڵێ"], "he says")()
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
