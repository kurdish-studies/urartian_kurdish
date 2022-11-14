import io
import json



def export_to_html(dataframe):
    with io.open("export.html", "w", encoding='utf8') as html_file:
        html_file.write(dataframe.to_html())


def export_to_markdown(dataframe, file_name="export.md"):
    with io.open(file_name, "w", encoding='utf8') as md_file:
        md_file.write(dataframe.to_html())


def export_to_json(dataframe):
    with open('json_dict.json', 'w', encoding='utf8') as filehandle:
        json.dump(dataframe, filehandle, indent=4, ensure_ascii=False)