#  Hurro-Urartian-Kurdish from the lexicostatistical viewpoint.
import pandas as pd

from data.data_loader import load_data
from generator import generate_df, export_to_markdown, export_to_json
from preprocessor.preprocessor import extract_note_from_text

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
    ur_ku = zip(dataframe['Urartian']['word'], dataframe['Kurdish']['word'])

    for i, item in enumerate(zip(dataframe['Urartian']['word'], dataframe['Kurdish']['word'])):
        print(i, item)

    # export_to_json(dataframe)
    # export_to_html(dataframe)
    # text = "land, country, field, cf. kurdawari, کوردەواری / warê me وارێ مە armenian agarak has been suggested as an armenian loan from 'awari'. kurdish has even 'garak' with the same meaning"
    # text2 = "build cf, kurdish d>nil"
    # print(extract_note_from_text(text, 'cf'))
    # print(extract_note_from_text(text2, 'cf'))
    export_to_markdown(dataframe, file_name="export.md")
    print(zip(dataframe['Urartian']))

