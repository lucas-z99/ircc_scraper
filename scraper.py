from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import os
import time


#  SETUP  ------------------------------------
tWait = 2  # if WIFI indeed bad, increase to 5 sec
chromedriver_exe = "chromedriver-win64\\chromedriver.exe"  # .exe file
save_to_folder = "saved_html"

#  emulate chrome  ------------------------------------
# chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run in headless mode (no browser UI)

dir = os.path.join(os.path.dirname(__file__), chromedriver_exe)
service = Service(dir)
# driver = webdriver.Chrome(service=service, options=chrome_options)
driver = webdriver.Chrome(service=service)

#  browse  ------------------------------------
print("\nbrowsing...\n")
driver.get(
    "https://www.canada.ca/en/immigration-refugees-citizenship/corporate/mandate/policies-operational-instructions-agreements/ministerial-instructions/express-entry-rounds.html"
)
time.sleep(tWait)

try:  # to fetch faster, display max lines of entry per page
    select = Select(driver.find_element(By.NAME, "wb-auto-4_length"))
    max_entry_per_page = select.options[-1]
    select.select_by_visible_text(max_entry_per_page.text)
    time.sleep(tWait)
except Exception as e:
    print("\nCannot display max lines of entries. Continue as default...\n")

#  save  ------------------------------------
save_folder_dir = os.path.join(os.path.dirname(__file__), save_to_folder)
os.makedirs(save_folder_dir, exist_ok=True)

iPage = 1

while True:  # loop through all pages
    print(f"saving page #{iPage}")

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
print(f"Complete! All pages saved to {save_folder_dir}\n")
