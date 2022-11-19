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
    notes = ""
    final_definition = ""
    if type(text) == list:
        # for item in text:
        #     if str(item).__contains__("cf"):
        #         phrases = item.split(separator)
        #         if len(phrases) > 1:
        #             notes.append(str(*phrases[1:]).replace(". ", "").replace(", ", ""))
        #     if len(notes) > 0:
        #         notes.append(str(*phrases[1:]))
        joined_text = ""


        if len(text) > 1:
            for i in range(len(text)):

                joined_text += ' ' + text[i]
            # joined_text += text[i] + ''
        else:
            joined_text = text
        # st = re.findall("'\[", text)
        text = str(joined_text).replace("']", "").replace("\"]", "").replace("['", "").replace("[\"", "")
    phrases = text.split(separator)
    if len(phrases) > 1:
        notes = str(*phrases[1:]).replace(". ", "").replace(", ", "")
        final_definition = phrases[0]
        # print("final_definition: ", final_definition)
    return notes, final_definition
