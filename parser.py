from bs4 import BeautifulSoup
import os
import pandas  # for excel
import re


def run():

    #  CONFIG  ----------------------------------------
    data_folder = "ee_draws"
    excel_file_name = "EE_draws.xlsx"  # save to excel

    #  load  ----------------------------------------
    parent = os.path.join(os.path.dirname(__file__), data_folder)
    excel_data = []

    for child in os.listdir(parent):

        if not child.endswith(".html"):  # only html
            continue

        _path = os.path.join(parent, child)
        with open(_path, "r", encoding="utf-8") as f:
            html = f.read()

        # parse data
        soup = BeautifulSoup(html, "html.parser")
        selection = soup.find_all("tr")

        index_list = set()

        for row in selection[1:]:  # skip header
            cols = row.find_all("td")
            if len(cols) == 5:

                index = cols[0].text.strip()
                if index == "":
                    continue
                if index in index_list:
                    print(f"Skip duplicate index {index} in {child}")
                    continue
                if index.isdigit():
                    index = int(index)

                date = cols[1].get("data-order").strip()
                round_type = cols[2].text.strip()
                iv = cols[3].text.strip()
                invitations = int(cols[3].text.strip().replace(",", ""))
                score = int(cols[4].text.strip())
                # url = cols[0].find("a")["href"]
                # hyperlink = f'=HYPERLINK("{url}", "Link")'

                excel_data.append([index, date, round_type, invitations, score])
                # print(
                #     f"{index}\t{date}\t{round_type}\t{invitations}\t{score}"
                # )  # debug

    #  excel  ----------------------------------------
    df = pandas.DataFrame(
        excel_data,
        columns=["#", "Date", "Round Type", "Invitations", "CRS"],
    )

    # sort int/string mixture, thanks to 91a/91b
    def sort_key(index):
        match = re.match(r"(\d+)([a-zA-Z]*)", str(index))
        if match:
            num_part = int(match.group(1))
            alpha_part = match.group(2)
            return (num_part, alpha_part)
        else:
            return (float("inf"), index)  # go to the end

    df["SortKey"] = df["#"].apply(sort_key)
    df = df.sort_values(by="SortKey", ascending=False).drop(columns=["SortKey"])

    # to excel date format
    df["Date"] = pandas.to_datetime(df["Date"])

    dir = os.path.join(os.path.dirname(__file__), excel_file_name)
    df.to_excel(dir, index=False)

    print(f"\nSuccess! Excel saved: {excel_file_name}\n")


if __name__ == "__main__":
    run()
