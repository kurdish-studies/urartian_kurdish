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


def extract_note_from_text(text, separator):
    notes = []
    if type(text) == list:
        # for item in text:
        #     if str(item).__contains__("cf"):
        #         phrases = item.split(separator)
        #         if len(phrases) > 1:
        #             notes.append(str(*phrases[1:]).replace(". ", "").replace(", ", ""))
        #     if len(notes) > 0:
        #         notes.append(str(*phrases[1:]))
        joined_text = ""

        # todo: correctly join list items and then extract the notes
        if len(text) > 1:
            for item in text:
                joined_text += item + ' '
        else:
            joined_text = text
        text = str(joined_text).replace("']", "").replace("\"]", "")
    phrases = text.split(separator)
    if len(phrases) > 1:
        notes.append(str(*phrases[1:]).replace(". ", "").replace(", ", ""))
    # for phrase in phrases:
    #     if str(phrase).__contains__(separator):
    #         notes.append(phrase)

    return notes
