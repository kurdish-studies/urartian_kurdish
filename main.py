from bs4 import BeautifulSoup
import requests
import io

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


def get_lines(file, limit=None):
    word_index = 0
    for line in file.readlines():

        if not limit == None:
            if word_index > limit:
                break
        if tag in line:
            if is_single_break(line, tag):
                if not word_index > limit:
                    print(word_index, limit)
                    print(f"\nWord {word_index + 1}:\n{10 * '-'}")
                    word_index += 1
            else:
                # print(line, end='')
                yield line


def clean_text(file):
    for line in get_lines(file, limit=20):
        line = line.replace("&nbsp;", " ").replace("<br />", "")
        line = line.replace("&gt;", ">").replace("&gt; ", ">").replace(" &gt;", ">")
        line = line.replace("&lt;", "<").replace("&lt; ", "<").replace(" &lt; ", "<")
        yield line


if __name__ == '__main__':
    file = get_data(raw_data)
    for _, line in enumerate(clean_text(file)):
        print(line, end="")
