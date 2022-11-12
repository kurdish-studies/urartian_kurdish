import re


def clean_text(text):
    # Please note that I have corrected some inconsistencies manually that were rare cases (less than 5); therefore
    # not worth writing codes

    # Remove and correct redundant characters and signs
    text = text.replace("&nbsp;", " ").replace("<br />", "").replace("\n", "").replace("&nbsp;", " ")
    text = text.replace("&#8204;", "").replace(":", " ")
    text = text.replace("&gt;", ">").replace("&gt; ", ">").replace(" &gt;", ">")
    text = text.replace("&lt;", "<").replace("&lt; ", "<").replace(" &lt; ", "<")
    text = text.lower()
    splitted_line = text.split(" ")
    txt = re.search("[0-9)]*", splitted_line[0].replace(":", ""))
    text = text.replace(f"{txt.group()}", "")
    if len(text) > 2:
        return text