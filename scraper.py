from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import os
import time


def run():

    #  CONFIG  ------------------------------------
    data_url = "https://www.canada.ca/en/immigration-refugees-citizenship/corporate/mandate/policies-operational-instructions-agreements/ministerial-instructions/express-entry-rounds.html"
    tWait = 1  # if WIFI bad, increase to 5
    chromedriver_file_path = "chromedriver-win64\\chromedriver.exe"
    output_path = "ee_draws"

    #  emulate chrome  ------------------------------------
    print("-> init chrome driver...")
    dir = os.path.join(os.path.dirname(__file__), chromedriver_file_path)
    driver = webdriver.Chrome(service=Service(dir))

    #  browse  ------------------------------------
    print("-> browsing...")
    driver.get(data_url)
    time.sleep(tWait * 3)

    try:  # display more entries per page to fetch faster
        select = Select(driver.find_element(By.NAME, "wb-auto-4_length"))
        max_entry_per_page = select.options[-1]
        select.select_by_visible_text(max_entry_per_page.text)
        print(f"set entry per page: { select.options[-1].text}")
        time.sleep(tWait)
    except Exception as e:
        print("sail to set entry per page, continue as default...")

    #  save  ------------------------------------
    print(f"-> saving pages...")

    save_folder_dir = os.path.join(os.path.dirname(__file__), output_path)
    os.makedirs(save_folder_dir, exist_ok=True)

    iPage = 1

    while True:  # loop through all pages
        print(f"#{iPage}")

        dir = os.path.join(save_folder_dir, f"page_{iPage}.html")
        with open(dir, "w", encoding="utf-8") as file:
            file.write(driver.page_source)

        try:
            next_button = driver.find_element(By.LINK_TEXT, "Next")
            if not next_button:
                break
            if "disabled" in next_button.get_attribute("class"):
                break  # reach end
            next_button.click()
            time.sleep(tWait)
            iPage += 1
        except Exception as e:
            # We reached last page
            # OR
            # Sometimes all entries are loaded in a single page. How convient!
            break

    #
    driver.quit()
    print(f"Complete! All pages saved to: {save_folder_dir}\n")


if __name__ == "__main__":
    run()
