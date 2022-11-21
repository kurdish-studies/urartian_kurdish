import io
import json
import os


def export_to_html(dataframe):
    with io.open("export.html", "w", encoding='utf8') as html_file:
        html_file.write(dataframe.to_html())


def export_to_markdown(dataframe, file_name="export.md"):
    with io.open(file_name, "w", encoding='utf8') as md_file:
        md_file.write(dataframe.to_html())


def export_to_json(data, file_name="default", dir="output/json"):
    path = f"{dir}/{file_name}.json"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf8') as filehandle:
        json.dump(data, filehandle, indent=4, ensure_ascii=False)

def serialize_dataframe(dataframe, src, tgt):
    pass