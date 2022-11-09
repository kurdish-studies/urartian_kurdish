from bs4 import BeautifulSoup
import requests
import io
import re

raw_data = False
word_index = 0
tag = "<br />"


def is_single_break(line, tag):
    return not len(line) > len(tag) + 1


def get_data(raw_data):
    global file
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


def get_lines(file, langs, limit=None):
    word_index = 0

    for line in file.readlines():

        if not limit == None:
            if word_index > limit:
                break
        if tag in line:
            if is_single_break(line, tag):
                # print(word_index, limit)
                # print(f"\nWord {word_index + 1}:\n{10 * '-'}")
                word_index += 1

            else:
                yield line


def clean_text(file, langs):

    # Please note that I have corrected some inconsistencies manually that were rare cases (less than 5); therefore
    # not worth writing codes

    line_set = set()
    temp_line = ""
    for line in get_lines(file, langs, limit=None):
        # Remove and correct redundant characters and signs
        line = line.replace("&nbsp;", " ").replace("<br />", "").replace("\n", "").replace("&nbsp;", " ")
        line = line.replace("&#8204;", "")
        line = line.replace("&gt;", ">").replace("&gt; ", ">").replace(" &gt;", ">")
        line = line.replace("&lt;", "<").replace("&lt; ", "<").replace(" &lt; ", "<")
        line = line.lower()
        splitted_line = line.split(" ")
        txt = re.search("[0-9)]*", splitted_line[0].replace(":", ""))
        line = line.replace(f"{txt.group()}", "")

        # Correct words and sentences that are separated from their main lines

        if len(line) > 2:
            yield line


def tokenize(file, langs):
    for line in clean_text(file, langs):

        splitted_line = line.split(" ")

        if not splitted_line[0].replace(":", "") in langs:
            # txt = re.search("[(]+", splitted_line[0])
            # if txt:
            #     print("txt: ", txt)
            print("not in langs: ", splitted_line[0], line)


if __name__ == '__main__':
    langs = ["kurdish", "urartian", "hurrian", "armenian", "kassite"]
    file = get_data(raw_data)
    # for _, line in enumerate(clean_text(file)):
    #     print(line, end="")
    tokenize(file, langs)
