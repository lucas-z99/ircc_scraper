import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os


def run():

    #  CONFIG  ---------------------------
    url = "https://www.ontario.ca/page/oinp-express-entry-notifications-interest"
    file_name = "oinp_draw.html"

    #
    print("checking OINP...")
    response = requests.get(url)

    if response.status_code == 200:

        soup = BeautifulSoup(response.text, "html.parser")

        for a in soup.find_all("a", href=True):  # note hyperlink
            a["href"] = urljoin(url, a["href"])

        # save
        dir = os.path.join(os.path.dirname(__file__), file_name)
        with open(dir, "w", encoding="utf-8") as file:
            file.write(str(soup))

        print(f"Complete! OINP save to {file_name}")
    else:
        print("Error: cannot load OINP website")

        


if __name__ == "__main__":
    run()
