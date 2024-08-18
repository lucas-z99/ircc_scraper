import platform
import requests
import zipfile
import os


def run():

    #  CONFIG  ----------------------------------------
    # choose a version:
    ver_list_human_friendly = "https://googlechromelabs.github.io/chrome-for-testing/latest-patch-versions-per-build.json"
    ver_list_url = "https://googlechromelabs.github.io/chrome-for-testing/latest-patch-versions-per-build-with-downloads.json"
    ver = "127.0.6533"  # MUST be <= than your Chrome's version

    # OS
    os_type = platform.system().lower()
    if os_type == "darwin":
        os_type = "mac-x64" if platform.machine() == "x86_64" else "mac-arm64"
    elif os_type == "windows":
        os_type = "win64"
    else:
        os_type = "linux64"

    # which ver
    respond = requests.get(ver_list_url)
    ver_list = respond.json()
    chrome_driver_list = ver_list["builds"][ver]["downloads"]["chromedriver"]
    download_url = next(
        item["url"] for item in chrome_driver_list if item["platform"] == os_type
    )

    # download
    respond = requests.get(download_url)
    save_dir = os.path.join(os.path.dirname(__file__), "chromedriver.zip")
    with open(save_dir, "wb") as file:
        file.write(respond.content)

    with zipfile.ZipFile(save_dir, "r") as zip_ref:
        zip_ref.extractall(os.path.dirname(__file__))

    os.remove(save_dir)

    #
    print(f"Success! Chromedriver saved to: {save_dir}\n")


if __name__ == "__main__":
    run()
