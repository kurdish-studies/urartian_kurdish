import io

import requests
from bs4 import BeautifulSoup


def load_data(from_url=False):
    # global raw_file

    # If there is no preprocessed data raw_file then get it from an url or load it from a raw_file
    if from_url:
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