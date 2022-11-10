from bs4 import BeautifulSoup
import requests
import io
import re

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


def tokenize(file, langs):
    for line in get_lines(file):
        if not line == "\n":
            splitted_line = line.split(" ")

            if not splitted_line[0] in langs:
                # txt = re.search("[(]+", splitted_line[0])
                # if txt:
                #     print("txt: ", txt)
                print("not in langs: ", splitted_line[0], line)
        else:
            print("\nNew word in the tokenizer")


if __name__ == '__main__':
    langs = ["kurdish", "urartian", "hurrian", "armenian", "kassite"]
    file = get_data(raw_data)
    # for _, line in enumerate(clean_text(file)):
    #     print(line, end="")
    tokenize(file, langs)
