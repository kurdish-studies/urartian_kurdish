import io
import json

from main import word_dict


def export_to_html(dataframe):
    with io.open("export.html", "w", encoding='utf8') as html_file:
        html_file.write(dataframe.to_html())


def export_to_markdown(dataframe):
    with io.open("readme.md", "w", encoding='utf8') as md_file:
        md_file.write(dataframe.to_html())


def export_to_json():
    with open('json_dict.json', 'w', encoding='utf8') as filehandle:
        json.dump(word_dict, filehandle, indent=4, ensure_ascii=False)