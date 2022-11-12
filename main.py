#  Hurro-Urartian-Kurdish from the lexicostatistical viewpoint.

import json

from bs4 import BeautifulSoup
import requests
import io
import re
import pandas as pd
from tabulate import tabulate

raw_data = False
word_index = 0
break_tag = "<br />"


def is_single_break(line, tag):
    # True if the line is not a single break tag or space
    return not len(line) > len(tag) + 1


def get_data(raw_data):
    global file

    # If there is no preprocessed data file then get it from an url or load it from a file
    if raw_data:
        url = "http://landofkarda.blogspot.com/2011/04/hurro-urartian-substratum-in-kurdish-2.html"

        if not open("data.html"):
            file = requests.get(url).text
            with io.open("data.html", "w") as _file:
                _file.write(file)
        else:
            file = open("data.html")

        soup = BeautifulSoup(file, features="html.parser")
        print("the length is: ", len(soup.find_all("br")))

    else:
        file = open("preprocessed.txt")

    return file


def clean_text(line):
    # Please note that I have corrected some inconsistencies manually that were rare cases (less than 5); therefore
    # not worth writing codes

    # Remove and correct redundant characters and signs
    line = line.replace("&nbsp;", " ").replace("<br />", "").replace("\n", "").replace("&nbsp;", " ")
    line = line.replace("&#8204;", "").replace(":", " ")
    line = line.replace("&gt;", ">").replace("&gt; ", ">").replace(" &gt;", ">")
    line = line.replace("&lt;", "<").replace("&lt; ", "<").replace(" &lt; ", "<")
    line = line.lower()
    splitted_line = line.split(" ")
    txt = re.search("[0-9)]*", splitted_line[0].replace(":", ""))
    line = line.replace(f"{txt.group()}", "")
    if len(line) > 2:
        return line


def get_lines(file, break_tag="<br />", limit=None):
    word_index = 0

    for line in file.readlines():
        if not limit == None:
            if word_index > limit:
                break
        if break_tag in line:
            # If it's a single break break_tag then it means the start of a new line; therefore increment the
            # word_index by 1
            if is_single_break(line, break_tag):
                word_index += 1
                yield "\n"

            else:
                cleaned_text = clean_text(line)
                print(cleaned_text)
                if not cleaned_text == None:
                    yield clean_text(line)


def extract_paranthesis(line):
    return re.findall('\(([^)]+)', line)


def extract_language_name(line):
    return line.split(" ")[0]


def parse_raw_text(line):
    for i in extract_paranthesis(line):
        line = line.replace(f"({i})", '')
    line = line.replace(extract_language_name(line), '')
    # print("parsed text: ", line)
    # line = line.replace(extract_language_name(line), '')
    filtered_list = filter(len, line.split(" ")[1:])
    return list(filtered_list)


def export_to(file, langs, to_format="json"):
    dictionary = {}
    idx = 0
    for line in get_lines(file):
        if not line == "\n":
            splitted_line = line.split(" ")

            if to_format == "json":
                to_json(idx, line, dictionary)
            elif to_format == "dataframe":
                to_dataframe(idx, line, dictionary)

            if not splitted_line[0] in langs:
                # txt = re.search("[(]+", splitted_line[0])
                # if txt:
                #     print("txt: ", txt)
                print("not in langs: ", splitted_line[0], line)
        else:
            idx += 1
            # print("\nNew word in the tokenizer")

    return dictionary

def to_dataframe(idx, line, dictionary):
    lang = extract_language_name(line)
    word = parse_raw_text(line)
    definition = extract_paranthesis(line)
    # mux = pd.MultiIndex.from_product([['Start', 'Intermediary', 'End'], ["word", "gloss", "transition"]])
    # sub_columns = []
    temp_data = [
            word,
            definition,
            ""
        ]
    print("temp_data: ", temp_data)
    # temp_df = pd.DataFrame.from_dict(data=temp_data, orient='index', columns=mux)
    if idx in dictionary.keys():
        for item in temp_data:
            dictionary[idx].append(" ".join(item))
    else:
        dictionary.update({idx: []})
        for item in temp_data:
            dictionary[idx].append(" ".join(item))

def to_json(idx, line, dictionary):
    lang = extract_language_name(line)
    word = parse_raw_text(line)
    definition = extract_paranthesis(line)
    if idx in dictionary.keys():
        dictionary[idx].append({
            "lang": lang,
            "word": word,
            "definition": definition
        })
    else:
        dictionary.update({idx: [
            {
                "lang": lang,
                "word": word,
                "definition": definition
            }
        ]})


if __name__ == '__main__':
    langs = ["urartian", "kurdish",  "armenian", "hurrian", "kassite"]
    # langs = ["urartian", "kurdish"]
    data = {
        1: [1, 2, 3, 4, 5, 11],
        2: [1, 2, 3, 4, 5, 11]
    }
    mux = pd.MultiIndex.from_product([langs, ["word", "gloss", "transition"]])
    file = get_data(raw_data)

    word_dict = export_to(file, langs, to_format="dataframe")

    # print(word_dict)

    dataframe = pd.DataFrame.from_dict(word_dict, orient='index', columns=mux)
    with io.open("export.html", "w", encoding='utf8') as html_file:
        html_file.write(dataframe.to_html())

    with open('json_dict.json', 'w', encoding='utf8') as filehandle:
        json.dump(word_dict, filehandle, indent=4, ensure_ascii=False)
