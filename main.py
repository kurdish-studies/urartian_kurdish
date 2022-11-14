#  Hurro-Urartian-Kurdish from the lexicostatistical viewpoint.
import pandas as pd

from data.data_loader import load_data
from generator import generate_df, export_to_markdown, export_to_json


if __name__ == '__main__':
    langs = ["urartian", "kurdish", "armenian", "hurrian", "kassite"]
    main_headers = ["Urartian", "Kurdish", "Hurrian", "Kassite", "Armenian"]
    sub_headers = ["word", "glossary", "notes"]
    # langs = ["urartian", "kurdish"]
    url = "http://landofkarda.blogspot.com/2011/04/hurro-urartian-substratum-in-kurdish-2.html"

    mux = pd.MultiIndex.from_product([main_headers, sub_headers])
    raw_file = load_data(url, from_url=False)
    print(mux)
    # word_dict = export_to(raw_file, langs, to_format="dataframe")
    word_dict = generate_df(raw_file, langs, sub_columns=sub_headers)

    dataframe = pd.DataFrame.from_dict(word_dict, orient='index', columns=mux)
    dataframe.fillna("", inplace=True)

    # export_to_json()
    # export_to_html(dataframe)
    export_to_markdown(dataframe, file_name="export.md")

