from bs4 import BeautifulSoup
import pandas as pd
import re
import os


def run():

    #  CONFIG  ---------------------------
    html_file = "oinp_draw.html"
    excel_file_name = "OINP_draws.xlsx"

    #
    dir = os.path.join(os.path.dirname(__file__), html_file)
    with open(dir, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    draws = []
    year = None
    pnp_stream = None

    for section in soup.find_all(["h2", "h3", "table"]):

        if section.name == "h2":  # year
            match = re.search(r"\b(20\d{2})\b", section.get_text(strip=True))
            if match:
                year = int(match.group(0))

        elif section.name == "h3":  # stream type
            pnp_stream = section.get_text(strip=True)

        elif section.name == "table":  # table

            headers = [
                th.get_text(strip=True) for th in section.find("thead").find_all("th")
            ]

            iDate = None
            iNoi = None
            iCrs = None
            iNote = None

            for i, header in enumerate(headers):
                if "Date" in header:
                    iDate = i
                elif "CRS" in header:
                    iCrs = i
                elif "Number" in header:
                    iNoi = i
                elif "Note" in header:
                    iNote = i

            # print(f"{year} date={iDate} noi={iNoi} crs={iCrs} note={iNote}")  # debug

            table_rows = section.find("tbody").find_all("tr")
            for row in table_rows:

                columns = row.find_all("td")

                # date
                date = columns[iDate].get_text(strip=True)

                # NOI
                noi = columns[iNoi].get_text(strip=True)
                noi = int(re.sub(r"\D", "", noi))  # ther was a 371* in 2019

                # CRS
                crs_range = None if iCrs == None else columns[iCrs].get_text(strip=True)
                crs0 = None
                crs1 = None
                if crs_range:
                    crs_range = re.findall(r"\d+", crs_range)
                    crs0 = int(crs_range[0]) if len(crs_range) >= 1 else None
                    crs1 = int(crs_range[1]) if len(crs_range) >= 2 else None

                # note
                if iNote == None:
                    note = None
                    url = None
                else:
                    note_html = str(columns[iNote])
                    note_soup = BeautifulSoup(note_html, "html.parser")
                    note = " ".join(note_soup.stripped_strings)
                    note = re.sub(r"\s{2,}", " ", note)  # remove excessive spaces

                    hyperlink = columns[iNote].find("a")  # url
                    if hyperlink:
                        url = hyperlink.get("href")

                # finally
                draws.append(
                    [
                        year,
                        pnp_stream,
                        date,
                        noi,
                        crs0,
                        crs1,
                        note,
                        url,
                    ]
                )

    # write to excel
    df = pd.DataFrame(
        draws,
        columns=["Year", "Stream", "Date", "NOI", "CRS_0", "CRS_1", "Note", "Note_url"],
    )

    dir = os.path.join(os.path.dirname(__file__), excel_file_name)
    df.to_excel(dir, index=False)

    #
    print(f"Complete! Excel saved: {excel_file_name}")


if __name__ == "__main__":
    run()
