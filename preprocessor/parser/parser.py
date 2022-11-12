import re

from preprocessor.parser.utility import is_single_break
from preprocessor import clean_text


def get_lines(file, break_tag="<br />", limit=None):
    word_index = 0

    for line in file.readlines():
        if not limit == None:
            if word_index > limit:
                break
        if break_tag in line:
            # If it's a single break break_tag then it means the start of a new text; therefore increment the
            # word_index by 1
            if is_single_break(line, break_tag):
                word_index += 1
                yield "\n"

            else:
                cleaned_text = clean_text(line)
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
    # text = text.replace(extract_language_name(text), '')
    filtered_list = filter(len, line.split(" ")[1:])
    return list(filtered_list)