import os
import subprocess


this_folder = os.path.dirname(__file__)

print(">>> Checking chromedriver...")
dir = os.path.join(this_folder, "setup_chromedriver.py")
subprocess.run(["python", dir], check=True)

print(">>> Scraping...")
dir = os.path.join(this_folder, "scraper.py")
subprocess.run(["python", dir], check=True)

print(">>> Parsing data...")
dir = os.path.join(this_folder, "parser.py")
subprocess.run(["python", dir], check=True)
