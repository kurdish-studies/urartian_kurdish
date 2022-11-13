import io

import requests
from bs4 import BeautifulSoup


def load_data(url, from_url=False):
    # global raw_file

    # If there is no preprocessed data raw_file then get it from an url or load it from a raw_file
    if from_url:

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